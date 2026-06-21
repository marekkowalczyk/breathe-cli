#!/usr/bin/env python3
"""Breathe CLI — paced breathing for HFrEF vagal training."""

import argparse
import os
import signal
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass

if os.name != 'nt':
    import select
    import termios
    import tty


# ── Constants ────────────────────────────────────────────────────────

VERSION = '1.9'

PRESETS = {
    'balanced': {'duration_min': 10, 'inhale_s': 5, 'exhale_s': 5},
    'calm': {'duration_min': 15, 'inhale_s': 4, 'exhale_s': 6},
    'extended':    {'duration_min': 20, 'inhale_s': 4, 'exhale_s': 6},
}

PRESET_DESCRIPTIONS = {'balanced': 'Equal ratio, neutral baseline',
                       'calm': 'Exhale-weighted, parasympathetic emphasis',
                       'extended': 'Full dose, Bernardi protocol'}

SOUND_INHALE = '/System/Library/Sounds/Tink.aiff'
SOUND_EXHALE = '/System/Library/Sounds/Pop.aiff'
AFPLAY       = '/usr/bin/afplay'
AFPLAY_VOL   = '0.3'

# Windows Audio
WIN_SOUND_INHALE = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'ding.wav')
WIN_SOUND_EXHALE = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'notify.wav')

# Linux Audio. Players probed in order; the first on PATH wins. Sounds default
# to the freedesktop theme. All overridable via --sound-player and the
# BREATHE_SOUND_PLAYER / BREATHE_SOUND_INHALE / BREATHE_SOUND_EXHALE env vars.
LINUX_PLAYERS = ('paplay', 'pw-play', 'aplay', 'ffplay', 'cvlc')
LINUX_PLAYER_ARGS = {
    'ffplay': ('-nodisp', '-autoexit', '-loglevel', 'quiet'),
    'cvlc': ('--play-and-exit',),
}
LINUX_SOUND_DIR    = '/usr/share/sounds/freedesktop/stereo'
LINUX_SOUND_INHALE = os.path.join(LINUX_SOUND_DIR, 'message.oga')
LINUX_SOUND_EXHALE = os.path.join(LINUX_SOUND_DIR, 'complete.oga')

# Resolved (player, inhale_path, exhale_path) once check_audio() picks 'linux'.
_LINUX_AUDIO = None


LOG_FILE   = os.path.expanduser('~/.breathe_log.csv')
LOG_HEADER = 'date,time,preset,ratio,duration_target_s,duration_actual_s,breaths,completion_pct,status'

BAR_WIDTH      = 30
FRAME_RATE_HZ  = 20
FRAME_SLEEP    = 1.0 / FRAME_RATE_HZ
COUNTDOWN_SECS = 3
MIN_TERM_WIDTH = 40
MIN_CYCLE_SECS = 8

ANSI_CLEAR    = '\033[2J\033[H'
ANSI_HIDE_CUR = '\033[?25l'
ANSI_SHOW_CUR = '\033[?25h'
ANSI_RESET    = '\033[0m'
ANSI_DIM      = '\033[2m'
ANSI_CYAN     = '\033[36m'
ANSI_GREEN    = '\033[32m'
ANSI_CLR_LINE = '\033[K'

INHALE, EXHALE, PAUSED = 'INHALE', 'EXHALE', 'PAUSED'
PHASE_LABEL = {INHALE: 'IN', EXHALE: 'OUT'}

SAFETY_TEXT = """\
Breathe CLI \u2014 safety notes
\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

This app paces slow breathing at 6 breaths per minute for vagal tone
support. It is a habit tool, not a medical device.

STOP THE SESSION IMMEDIATELY if you experience:

  \u2022 Lightheadedness or dizziness \u2014 you may be breathing too deeply.
    Reduce depth, not rate. If it persists, stop.
  \u2022 Palpitations \u2014 stop, note the time, mention at your next
    cardiology visit.
  \u2022 Tingling in hands or face \u2014 hyperventilation signal. Stop,
    return to normal breathing.

This app deliberately does NOT support:
  \u2022 Breath retention (kumbhaka) of any length
  \u2022 Rapid breathing (kapalbhati, bhastrika, Wim Hof patterns)
  \u2022 Total breath cycles shorter than 8 seconds

Press q or Ctrl+C to end any session. Exit is always immediate.

DISCLAIMER: This app is not a medical device. It does not diagnose,
treat, or prevent any condition. Consult your physician before starting
a breathing practice, especially with a cardiac or respiratory condition.
Use at your own risk. The author assumes no liability for any adverse
effects. By using this app you acknowledge and accept these terms.

For the clinical evidence behind these constraints, see README.md."""

@dataclass
class Config:
    duration_s: int
    inhale_s: int
    exhale_s: int
    preset_name: str       # 'balanced', 'calm', 'extended', or 'custom'
    sound_enabled: bool
    quiet: bool
    sound_player: str = None   # Linux player override (--sound-player)

    @property
    def ratio_str(self):
        return '{}-{}'.format(self.inhale_s, self.exhale_s)

@dataclass
class Result:
    breaths: int = 0
    elapsed: float = 0.0
    completed: bool = False
    aborted: bool = False

@dataclass
class Layout:
    width: int
    height: int
    header_row: int
    phase_row: int
    bar_row: int
    progress_row: int
    footer_row: int
    minimal: bool
    use_colour: bool
    use_unicode: bool

def supports_colour():
    if os.environ.get('NO_COLOR'):
        return False
    return sys.stdout.isatty()

def supports_unicode():
    enc = getattr(sys.stdout, 'encoding', '') or ''
    return 'utf' in enc.lower()

def format_mmss(seconds):
    m, s = divmod(int(seconds), 60)
    return '{:02d}:{:02d}'.format(m, s)

def format_human(seconds):
    m, s = divmod(int(seconds), 60)
    if m > 0:
        return '{} min {} s'.format(m, s)
    return '{} s'.format(s)

def compute_layout():
    size = shutil.get_terminal_size((80, 24))
    w, h = size.columns, size.lines
    minimal = w < MIN_TERM_WIDTH
    mid = h // 2
    return Layout(
        width=w, height=h,
        header_row=max(mid - 4, 1),
        phase_row=max(mid - 1, 3),
        bar_row=max(mid + 1, 5),
        progress_row=max(mid + 3, 7),
        footer_row=min(mid + 5, h),
        minimal=minimal,
        use_colour=supports_colour(),
        use_unicode=supports_unicode(),
    )

def setup_windows_console():
    if os.name == 'nt':
        try:
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.windll.kernel32
            hOut = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            if hOut and hOut != -1:
                mode = wintypes.DWORD()
                if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
                    # 0x0004: ENABLE_VIRTUAL_TERMINAL_PROCESSING
                    kernel32.SetConsoleMode(hOut, mode.value | 0x0004)
        except Exception:
            try:
                os.system('')
            except Exception:
                pass

def resolve_linux_audio(environ, which, override=None):
    """Resolve (player, inhale_path, exhale_path) for Linux, or None for bell.

    Player comes from override (--sound-player), then BREATHE_SOUND_PLAYER, then
    the first LINUX_PLAYERS entry on PATH. Sound paths come from
    BREATHE_SOUND_INHALE / BREATHE_SOUND_EXHALE, else the freedesktop defaults.
    Returns None (caller falls back to bell) if no player or sound file is found.
    """
    player = override or environ.get('BREATHE_SOUND_PLAYER')
    if player:
        if not which(player):
            return None
    else:
        player = next((p for p in LINUX_PLAYERS if which(p)), None)
        if not player:
            return None
    inhale = environ.get('BREATHE_SOUND_INHALE', LINUX_SOUND_INHALE)
    exhale = environ.get('BREATHE_SOUND_EXHALE', LINUX_SOUND_EXHALE)
    if not (os.path.isfile(inhale) and os.path.isfile(exhale)):
        return None
    return (player, inhale, exhale)

def check_audio(quiet, sound_player=None):
    """Init audio subsystem. Returns 'winsound', 'afplay', 'linux', or 'bell'."""
    global _LINUX_AUDIO
    if os.name == 'nt':
        try:
            import winsound
            if os.path.isfile(WIN_SOUND_INHALE) and os.path.isfile(WIN_SOUND_EXHALE):
                return 'winsound'
        except ImportError:
            pass
    elif sys.platform == 'darwin':
        if (os.path.isfile(AFPLAY) and os.access(AFPLAY, os.X_OK)
                and os.path.isfile(SOUND_INHALE)
                and os.path.isfile(SOUND_EXHALE)):
            return 'afplay'
    else:
        resolved = resolve_linux_audio(os.environ, shutil.which, sound_player)
        if resolved:
            _LINUX_AUDIO = resolved
            return 'linux'
    if not quiet:
        sys.stderr.write('audio unavailable: falling back to terminal bell\n')
    return 'bell'

def play_sound(phase, audio_mode):
    if audio_mode == 'winsound':
        try:
            import winsound
            path = WIN_SOUND_INHALE if phase == INHALE else WIN_SOUND_EXHALE
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass
    elif audio_mode == 'afplay':
        path = SOUND_INHALE if phase == INHALE else SOUND_EXHALE
        try:
            subprocess.Popen(
                [AFPLAY, '-v', AFPLAY_VOL, path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass
    elif audio_mode == 'linux':
        if _LINUX_AUDIO is None:
            return
        player, inhale, exhale = _LINUX_AUDIO
        path = inhale if phase == INHALE else exhale
        extra = LINUX_PLAYER_ARGS.get(os.path.basename(player), ())
        try:
            subprocess.Popen(
                [player, *extra, path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass
    elif audio_mode == 'bell':
        sys.stdout.write('\a')
        sys.stdout.flush()

def setup_raw_tty():
    if not sys.stdin.isatty():
        return None
    if os.name == 'nt':
        return None
    try:
        old = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return old
    except termios.error:
        return None

def restore_tty(old_settings):
    if os.name == 'nt':
        return
    if old_settings is not None:
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except termios.error:
            pass

def poll_key():
    if not sys.stdin.isatty():
        return None
    if os.name == 'nt':
        import msvcrt
        try:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b'\x03':  # Ctrl+C
                    _abort[0] = True
                    return 'q'
                if ch in (b'\x00', b'\xe0'):
                    msvcrt.getch()  # read secondary byte
                    return None
                try:
                    return ch.decode('utf-8', errors='ignore')
                except Exception:
                    return None
        except Exception:
            pass
        return None
    else:
        try:
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if r:
                return sys.stdin.read(1)
        except (OSError, ValueError):
            pass
        return None

def move_to(row, col):
    sys.stdout.write('\033[{};{}H'.format(row, col))

def draw_header(layout, config, remaining_s, paused, muted):
    move_to(layout.header_row, 1)
    sys.stdout.write(ANSI_CLR_LINE)
    parts = []
    if paused:
        parts.append('\u2016' if layout.use_unicode else 'P')
    if muted:
        parts.append('\U0001f507' if layout.use_unicode else 'M')
    if not parts:
        parts.append('\u25cf' if layout.use_unicode else '*')
    indicator = ' '.join(parts)
    line = '  {} \u00b7 {} \u00b7 {}   [{}]'.format(
        config.preset_name, config.ratio_str,
        format_mmss(remaining_s),
        indicator,
    )
    sys.stdout.write(line)

def draw_phase(layout, phase):
    move_to(layout.phase_row, 1)
    sys.stdout.write(ANSI_CLR_LINE)
    label = PHASE_LABEL.get(phase, phase)
    if layout.use_colour:
        colour = ANSI_CYAN if phase == INHALE else ANSI_GREEN
        styled = colour + label + ANSI_RESET
    else:
        styled = label
    if layout.minimal:
        sys.stdout.write('  ' + styled)
    else:
        pad = (layout.width - len(label)) // 2
        sys.stdout.write(' ' * pad + styled)

def draw_bar(layout, progress, phase):
    move_to(layout.bar_row, 1)
    sys.stdout.write(ANSI_CLR_LINE)
    if phase == INHALE:
        filled = round(progress * BAR_WIDTH)
    else:
        filled = round((1.0 - progress) * BAR_WIDTH)
    filled = max(0, min(BAR_WIDTH, filled))
    empty = BAR_WIDTH - filled
    if layout.use_unicode:
        bar = '\u2588' * filled + '\u2591' * empty
    else:
        bar = '#' * filled + '-' * empty
    if layout.minimal:
        sys.stdout.write('  ' + bar)
    else:
        pad = (layout.width - BAR_WIDTH) // 2
        sys.stdout.write(' ' * pad + bar)

def draw_progress(layout, config, elapsed):
    move_to(layout.progress_row, 1)
    sys.stdout.write(ANSI_CLR_LINE)
    cycle_s = config.inhale_s + config.exhale_s
    frac = min(1.0, elapsed / config.duration_s) if config.duration_s > 0 else 1.0
    filled = round(frac * BAR_WIDTH)
    filled = max(0, min(BAR_WIDTH, filled))
    empty = BAR_WIDTH - filled
    if layout.use_unicode:
        bar = '\u2501' * filled + '\u2500' * empty
    else:
        bar = '=' * filled + '-' * empty
    if layout.use_colour:
        bar = ANSI_DIM + bar + ANSI_RESET
    if layout.minimal:
        sys.stdout.write('  ' + bar)
    else:
        pad = (layout.width - BAR_WIDTH) // 2
        sys.stdout.write(' ' * pad + bar)

def draw_footer(layout, paused):
    move_to(layout.footer_row, 1)
    sys.stdout.write(ANSI_CLR_LINE)
    if paused:
        text = 'space resume \u00b7 q quit'
    else:
        text = 'space pause \u00b7 s mute \u00b7 q quit'
    if layout.use_colour:
        text = ANSI_DIM + text + ANSI_RESET
    sys.stdout.write('  ' + text)

def render_frame(layout, config, elapsed, remaining_s, phase, progress,
                 paused, muted):
    draw_header(layout, config, remaining_s, paused, muted)
    draw_phase(layout, phase)
    draw_bar(layout, progress, phase)
    draw_progress(layout, config, elapsed)
    draw_footer(layout, paused)
    sys.stdout.flush()

_abort = [False]

def _sigint_handler(signum, frame):
    _abort[0] = True

def run_countdown(layout, config):
    """Run the 3-second settle countdown. Returns False if aborted."""
    for i in range(COUNTDOWN_SECS, 0, -1):
        if _abort[0]:
            return False
        move_to(layout.phase_row, 1)
        sys.stdout.write(ANSI_CLR_LINE)
        label = str(i)
        if layout.minimal:
            sys.stdout.write('  ' + label)
        else:
            pad = (layout.width - len(label)) // 2
            sys.stdout.write(' ' * pad + label)
        draw_header(layout, config, config.duration_s, False, False)
        draw_bar(layout, 0.0, INHALE)
        draw_footer(layout, False)
        sys.stdout.flush()
        for _ in range(FRAME_RATE_HZ):
            if _abort[0]:
                return False
            key = poll_key()
            if key == 'q':
                return False
            time.sleep(FRAME_SLEEP)
    return True

def run_session(config, result):
    is_tty = sys.stdout.isatty() and sys.stdin.isatty()

    # ── Non-TTY path ─────────────────────────────────────────────
    if not is_tty:
        if not config.quiet:
            sys.stderr.write('Warning: not a TTY, running without animation.\n')
        start = time.monotonic()
        cycle_s = config.inhale_s + config.exhale_s
        try:
            time.sleep(config.duration_s)
            result.completed = True
        except KeyboardInterrupt:
            result.aborted = True
        result.elapsed = min(time.monotonic() - start, float(config.duration_s))
        result.breaths = int(result.elapsed // cycle_s)
        return

    setup_windows_console()
    audio_mode = (check_audio(config.quiet, config.sound_player)
                  if config.sound_enabled else 'none')
    layout = compute_layout()
    if layout.minimal and not config.quiet:
        sys.stderr.write('Warning: terminal narrow, running in minimal mode.\n')

    old_termios = setup_raw_tty()
    old_sigint = signal.signal(signal.SIGINT, _sigint_handler)
    _abort[0] = False

    muted = not config.sound_enabled

    try:
        sys.stdout.write(ANSI_HIDE_CUR)
        sys.stdout.write(ANSI_CLEAR)
        sys.stdout.flush()

        if not run_countdown(layout, config):
            result.aborted = True
            return

        cycle_s = config.inhale_s + config.exhale_s
        state = INHALE
        phase_start_wall = time.monotonic()
        breathing_base = 0.0

        if not muted and audio_mode != 'none':
            play_sound(INHALE, audio_mode)

        while True:
            now = time.monotonic()

            # ── PAUSED ──────────────────────────────────────
            if state == PAUSED:
                if _abort[0]:
                    result.aborted = True
                    break
                key = poll_key()
                if key == 'q':
                    result.aborted = True
                    break
                elif key == ' ':
                    if breathing_base >= config.duration_s:
                        render_frame(layout, config, config.duration_s, 0,
                                     EXHALE, 1.0, False, muted)
                        time.sleep(0.4)
                        result.completed = True
                        break
                    state = INHALE
                    phase_start_wall = now
                    if not muted and audio_mode != 'none':
                        play_sound(INHALE, audio_mode)
                elif key == 's':
                    muted = not muted
                if state == PAUSED:
                    render_frame(layout, config, paused_elapsed,
                                 paused_remaining, paused_phase,
                                 paused_progress, True, muted)
                    time.sleep(FRAME_SLEEP)
                    continue
                # Resume: fall through to active code

            # ── INHALE / EXHALE ─────────────────────────────
            if _abort[0]:
                result.aborted = True
                break

            phase_dur = (config.inhale_s if state == INHALE
                         else config.exhale_s)
            phase_elapsed = now - phase_start_wall
            progress = phase_elapsed / phase_dur

            # Phase transition
            if progress >= 1.0:
                if state == INHALE:
                    phase_start_wall += config.inhale_s
                    state = EXHALE
                    if not muted and audio_mode != 'none':
                        play_sound(EXHALE, audio_mode)
                else:
                    result.breaths += 1
                    breathing_base = result.breaths * cycle_s
                    if breathing_base >= config.duration_s:
                        render_frame(layout, config, config.duration_s, 0,
                                     EXHALE, 1.0, False, muted)
                        time.sleep(0.4)
                        result.completed = True
                        break
                    phase_start_wall += config.exhale_s
                    state = INHALE
                    if not muted and audio_mode != 'none':
                        play_sound(INHALE, audio_mode)
                # Recalculate for the new phase so the render below
                # shows the correct label and bar on the same frame
                # the sound fires (no stale-frame flicker).
                phase_dur = (config.inhale_s if state == INHALE
                             else config.exhale_s)
                phase_elapsed = now - phase_start_wall
                progress = phase_elapsed / phase_dur

            # Countdown: integer seconds remaining based on actual
            # session length (which is always a multiple of cycle_s).
            clean_phase_s = int(phase_elapsed)
            if state == INHALE:
                elapsed_display = breathing_base + phase_elapsed
                remaining_s = (config.duration_s - breathing_base
                               - clean_phase_s)
            else:
                elapsed_display = (breathing_base + config.inhale_s
                                   + phase_elapsed)
                remaining_s = (config.duration_s - breathing_base
                               - config.inhale_s - clean_phase_s)

            key = poll_key()
            if key == 'q':
                result.aborted = True
                break
            elif key == ' ':
                paused_phase = state
                paused_progress = progress
                paused_elapsed = elapsed_display
                paused_remaining = remaining_s
                state = PAUSED
                render_frame(layout, config, paused_elapsed,
                             paused_remaining, paused_phase,
                             paused_progress, True, muted)
                time.sleep(FRAME_SLEEP)
                continue
            elif key == 's':
                muted = not muted

            render_frame(layout, config, elapsed_display, remaining_s,
                         state, progress, False, muted)
            time.sleep(FRAME_SLEEP)

        result.elapsed = breathing_base

    finally:
        sys.stdout.write(ANSI_SHOW_CUR)
        sys.stdout.write(ANSI_RESET)
        move_to(layout.footer_row + 2, 1)
        sys.stdout.flush()
        restore_tty(old_termios)
        signal.signal(signal.SIGINT, old_sigint)

def _completion(config, result):
    pct = min(100, int(result.elapsed / config.duration_s * 100)) if config.duration_s > 0 else 100
    status = 'completed' if result.completed else 'ended early (user)'
    return pct, status

def print_summary(config, result):
    label = config.preset_name if config.preset_name != 'custom' else 'custom'
    target = '{} min ({}, {})'.format(config.duration_s // 60, label, config.ratio_str)
    pct, status = _completion(config, result)
    print('Session summary')
    print('\u2500' * 15)
    print('Target:    {}'.format(target))
    print('Completed: {} ({}%)'.format(format_human(result.elapsed), pct))
    print('Breaths:   {} full cycles'.format(result.breaths))
    print('Status:    {}'.format(status))

def log_session(config, result, session_start_time):
    """Append one CSV row to ~/.breathe_log.csv. Never raises."""
    try:
        write_header = not os.path.isfile(LOG_FILE)
        with open(LOG_FILE, 'a') as f:
            if write_header:
                f.write(LOG_HEADER + '\n')
            pct, status = _completion(config, result)
            row = '{},{},{},{},{},{},{},{},{}'.format(
                time.strftime('%Y-%m-%d', session_start_time),
                time.strftime('%H:%M:%S', session_start_time),
                config.preset_name,
                config.ratio_str,
                config.duration_s,
                int(result.elapsed),
                result.breaths,
                pct,
                status,
            )
            f.write(row + '\n')
    except OSError as e:
        sys.stderr.write('Warning: could not write session log: {}\n'.format(e))

def print_log_path():
    if os.path.isfile(LOG_FILE):
        print(LOG_FILE)
    else:
        print('{} (no sessions logged yet)'.format(LOG_FILE))

def print_safety():
    print(SAFETY_TEXT)

def print_presets():
    print('Available presets:\n')
    fmt = '  {:<10} {:>8}   {:<20} {}'
    print(fmt.format('Name', 'Duration', 'Ratio (in-ex)', 'Target use'))
    print(fmt.format('\u2500' * 10, '\u2500' * 8, '\u2500' * 20, '\u2500' * 24))
    for name, p in PRESETS.items():
        bpm = 60.0 / (p['inhale_s'] + p['exhale_s'])
        ratio = '{}s-{}s ({:.0f} bpm)'.format(p['inhale_s'], p['exhale_s'], bpm)
        print(fmt.format(name, '{} min'.format(p['duration_min']),
                         ratio, PRESET_DESCRIPTIONS[name]))

def _die(msg):
    sys.stderr.write('Error: ' + msg + '\n')
    sys.exit(1)

def parse_ratio(ratio_str):
    _fmt_err = 'Ratio must be in the form `inhale-exhale` (e.g. `5-5` or `4-6`).'
    parts = ratio_str.split('-')
    if len(parts) > 2:
        _die('Three-number ratios imply a breath hold. '
             'This app does not support breath retention. See `breathe --safety`.')
    if len(parts) != 2:
        _die(_fmt_err)
    try:
        inhale, exhale = int(parts[0]), int(parts[1])
    except ValueError:
        _die(_fmt_err)
    if inhale + exhale < MIN_CYCLE_SECS:
        _die('Total breath cycle must be \u2265 8 seconds (no rapid breathing).')
    if not (3 <= inhale <= 10):
        _die('Inhale must be 3\u201310 seconds.')
    if not (3 <= exhale <= 10):
        _die('Exhale must be 3\u201310 seconds.')
    if exhale > 2 * inhale:
        _die('Exhale must not exceed twice the inhale (no clinical evidence'
             ' for extreme ratios). See README.md for details.')
    return inhale, exhale

def build_parser():
    parser = argparse.ArgumentParser(
        prog='breathe',
        description='Paced breathing for HFrEF vagal training.',
        epilog='Example: breathe --preset balanced',
    )
    parser.add_argument('--version', action='version',
                        version='breathe {}'.format(VERSION))
    parser.add_argument('--safety', action='store_true',
                        help='Show safety information and exit')
    parser.add_argument('--list-presets', action='store_true',
                        help='Show available presets and exit')
    parser.add_argument('--preset', '-p', choices=list(PRESETS.keys()),
                        help='Use a named preset (balanced, calm, extended)')
    parser.add_argument('--duration', '-d', type=int, metavar='MINUTES',
                        help='Session duration in minutes (1\u201360, default: 10)')
    parser.add_argument('--ratio', '-r', metavar='IN-EX',
                        help='Breath ratio as inhale-exhale (e.g. 5-5 or 4-6)')
    parser.add_argument('--no-sound', '-n', action='store_true',
                        help='Disable audio cues')
    parser.add_argument('--sound-player', metavar='CMD',
                        help='Linux audio player command (default: auto-detect)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress startup warnings')
    parser.add_argument('--log', action='store_true',
                        help='Show log file path and exit')
    parser.add_argument('--no-log', action='store_true',
                        help='Suppress session logging for this run')
    return parser

def main():
    if sys.version_info < (3, 7):
        sys.stderr.write('Error: breathe requires Python 3.7+\n')
        sys.exit(1)

    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass


    parser = build_parser()
    args = parser.parse_args()

    if args.safety:
        print_safety()
        sys.exit(0)

    if args.log:
        print_log_path()
        sys.exit(0)

    if args.list_presets:
        print_presets()
        sys.exit(0)

    # Build config from args
    if args.preset:
        if args.duration is not None or args.ratio is not None:
            _die('--preset cannot be combined with --duration or --ratio.')
        p = PRESETS[args.preset]
        inhale_s, exhale_s = p['inhale_s'], p['exhale_s']
        duration_min = p['duration_min']
        preset_name = args.preset
    elif args.duration is not None or args.ratio is not None:
        inhale_s, exhale_s = 5, 5
        duration_min = 10
        preset_name = 'custom'
        if args.ratio:
            inhale_s, exhale_s = parse_ratio(args.ratio)
        if args.duration is not None:
            duration_min = args.duration
    else:
        # No args: auto-select preset by time of day
        hour = time.localtime().tm_hour
        if hour < 12:
            preset_name = 'balanced'
        elif hour < 17:
            preset_name = 'extended'
        else:
            preset_name = 'calm'
        p = PRESETS[preset_name]
        inhale_s, exhale_s = p['inhale_s'], p['exhale_s']
        duration_min = p['duration_min']

    if not (1 <= duration_min <= 60):
        _die('Duration must be 1\u201360 minutes.')

    # Round duration up to a whole number of breath cycles so that
    # the countdown, progress bar, and session end are all in sync.
    cycle_s = inhale_s + exhale_s
    duration_s = -(-duration_min * 60 // cycle_s) * cycle_s

    config = Config(
        duration_s=duration_s,
        inhale_s=inhale_s,
        exhale_s=exhale_s,
        preset_name=preset_name,
        sound_enabled=not args.no_sound,
        quiet=args.quiet,
        sound_player=args.sound_player,
    )

    result = Result()
    exc_info = None
    session_start_time = time.localtime()

    try:
        run_session(config, result)
    except KeyboardInterrupt:
        result.aborted = True
    except Exception:
        exc_info = sys.exc_info()

    print_summary(config, result)

    if not args.no_log:
        log_session(config, result, session_start_time)

    if exc_info is not None:
        import traceback
        traceback.print_exception(*exc_info)
        sys.exit(1)

if __name__ == '__main__':
    main()
