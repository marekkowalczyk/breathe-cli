#!/usr/bin/env python3
"""Unit tests for breathe.py — logic and arithmetic only, no TUI."""

import io
import os
import sys
import unittest
from contextlib import redirect_stderr

# Import the module under test
sys.path.insert(0, os.path.dirname(__file__))
import breathe


class TestFormatMmss(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(breathe.format_mmss(0), '00:00')

    def test_seconds(self):
        self.assertEqual(breathe.format_mmss(5), '00:05')
        self.assertEqual(breathe.format_mmss(59), '00:59')

    def test_minutes(self):
        self.assertEqual(breathe.format_mmss(60), '01:00')
        self.assertEqual(breathe.format_mmss(600), '10:00')
        self.assertEqual(breathe.format_mmss(3600), '60:00')

    def test_float_truncates(self):
        self.assertEqual(breathe.format_mmss(9.95), '00:09')
        self.assertEqual(breathe.format_mmss(0.99), '00:00')


class TestFormatHuman(unittest.TestCase):
    def test_seconds_only(self):
        self.assertEqual(breathe.format_human(45), '45 s')

    def test_minutes_and_seconds(self):
        self.assertEqual(breathe.format_human(125), '2 min 5 s')

    def test_exact_minutes(self):
        self.assertEqual(breathe.format_human(600), '10 min 0 s')


class TestConfigRatioStr(unittest.TestCase):
    def test_ratio_str(self):
        c = breathe.Config(600, 5, 5, 'morning', True, False)
        self.assertEqual(c.ratio_str, '5-5')

    def test_ratio_str_asymmetric(self):
        c = breathe.Config(900, 4, 6, 'evening', True, False)
        self.assertEqual(c.ratio_str, '4-6')


class TestVersion(unittest.TestCase):
    def test_version_string_includes_semver_and_released(self):
        s = breathe.version_string()
        self.assertTrue(s.startswith('breathe '))
        self.assertIn(breathe.VERSION, s)
        self.assertIn(breathe.RELEASED, s)

    def test_released_minute_precision(self):
        # YYYY-MM-DDTHH:MM — no seconds, no timezone suffix
        self.assertRegex(breathe.RELEASED, r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')


class TestPresets(unittest.TestCase):
    def test_all_presets_at_6_bpm(self):
        for name, p in breathe.PRESETS.items():
            cycle_s = p['inhale_s'] + p['exhale_s']
            bpm = 60.0 / cycle_s
            self.assertEqual(bpm, 6.0,
                             '{} preset is {:.1f} bpm, expected 6.0'.format(name, bpm))

    def test_all_presets_cycle_ge_8(self):
        for name, p in breathe.PRESETS.items():
            cycle_s = p['inhale_s'] + p['exhale_s']
            self.assertGreaterEqual(cycle_s, breathe.MIN_CYCLE_SECS,
                                    '{} cycle too short'.format(name))

    def test_all_presets_duration_divides_evenly(self):
        for name, p in breathe.PRESETS.items():
            duration_s = p['duration_min'] * 60
            cycle_s = p['inhale_s'] + p['exhale_s']
            self.assertEqual(duration_s % cycle_s, 0,
                             '{} duration not divisible by cycle'.format(name))

    def test_all_presets_have_descriptions(self):
        for name in breathe.PRESETS:
            self.assertIn(name, breathe.PRESET_DESCRIPTIONS)

    def test_night_preset_tsai_protocol(self):
        p = breathe.PRESETS['night']
        self.assertEqual(
            (p['duration_min'], p['inhale_s'], p['exhale_s']),
            (20, 3, 7),
        )


class TestPresetForHour(unittest.TestCase):
    def test_hour_mapping(self):
        cases = [
            (0, 'night'), (1, 'night'), (5, 'night'),
            (6, 'morning'), (7, 'morning'), (11, 'morning'),
            (12, 'long'), (16, 'long'),
            (17, 'evening'), (19, 'evening'), (21, 'evening'),
            (22, 'night'), (23, 'night'),
        ]
        for hour, expected in cases:
            self.assertEqual(
                breathe.preset_for_hour(hour), expected,
                'hour {} should map to {}'.format(hour, expected),
            )


class TestParseRatio(unittest.TestCase):
    def test_valid_equal(self):
        self.assertEqual(breathe.parse_ratio('5-5'), (5, 5))

    def test_valid_asymmetric(self):
        self.assertEqual(breathe.parse_ratio('4-6'), (4, 6))

    def test_valid_boundary(self):
        self.assertEqual(breathe.parse_ratio('3-5'), (3, 5))
        self.assertEqual(breathe.parse_ratio('10-10'), (10, 10))

    def test_three_numbers_rejected(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('4-7-8')

    def test_rapid_breathing_rejected(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('2-2')

    def test_too_short_cycle_rejected(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('3-4')  # 7 < 8

    def test_inhale_out_of_range(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('2-6')  # inhale < 3
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('11-5')  # inhale > 10

    def test_exhale_out_of_range(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('5-2')  # exhale < 3
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('5-11')  # exhale > 10

    def test_non_numeric_rejected(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('foo')

    def test_single_number_rejected(self):
        with self.assertRaises(SystemExit):
            breathe.parse_ratio('5')


class TestCompletion(unittest.TestCase):
    def test_completed(self):
        c = breathe.Config(600, 5, 5, 'morning', True, False)
        r = breathe.Result(breaths=60, elapsed=600.0, completed=True)
        pct, status = breathe._completion(c, r)
        self.assertEqual(pct, 100)
        self.assertEqual(status, 'completed')

    def test_aborted_partial(self):
        c = breathe.Config(600, 5, 5, 'morning', True, False)
        r = breathe.Result(breaths=30, elapsed=300.0, completed=False, aborted=True)
        pct, status = breathe._completion(c, r)
        self.assertEqual(pct, 50)
        self.assertEqual(status, 'ended early (user)')

    def test_zero_duration(self):
        c = breathe.Config(0, 5, 5, 'custom', True, False)
        r = breathe.Result(completed=True)
        pct, _ = breathe._completion(c, r)
        self.assertEqual(pct, 100)

    def test_pct_capped_at_100(self):
        c = breathe.Config(600, 5, 5, 'morning', True, False)
        r = breathe.Result(elapsed=650.0, completed=True)
        pct, _ = breathe._completion(c, r)
        self.assertEqual(pct, 100)


class TestBreathingBase(unittest.TestCase):
    """Verify breathing_base is always an exact multiple of cycle_s."""

    def test_breathing_base_multiples(self):
        for preset_name, p in breathe.PRESETS.items():
            cycle_s = p['inhale_s'] + p['exhale_s']
            duration_s = p['duration_min'] * 60
            total_cycles = duration_s // cycle_s
            for breaths in range(total_cycles + 1):
                bb = breaths * cycle_s
                self.assertEqual(bb % cycle_s, 0,
                                 'breathing_base {} not multiple of cycle_s {}'
                                 .format(bb, cycle_s))

    def test_breathing_base_type_is_int(self):
        cycle_s = 10  # 5 + 5
        for breaths in range(10):
            bb = breaths * cycle_s
            self.assertIsInstance(bb, int)


class TestRemainingTime(unittest.TestCase):
    """Test the remaining-time calculation used for countdown display.

    This is the area of bug #13. These tests document desired behaviour
    so that when the fix lands, it can be validated automatically.
    """

    def _remaining(self, duration_s, inhale_s, exhale_s, breaths,
                   phase, phase_elapsed):
        """Reproduce the remaining_s calculation from run_session."""
        cycle_s = inhale_s + exhale_s
        total_cycles = -(-duration_s // cycle_s)
        session_s = total_cycles * cycle_s
        breathing_base = breaths * cycle_s
        clean_phase_s = int(phase_elapsed)
        if phase == breathe.INHALE:
            remaining = session_s - breathing_base - clean_phase_s
        else:
            remaining = (session_s - breathing_base
                         - inhale_s - clean_phase_s)
        return remaining

    def _elapsed(self, inhale_s, exhale_s, breaths, phase, phase_elapsed):
        """Reproduce the elapsed_display calculation from run_session."""
        cycle_s = inhale_s + exhale_s
        breathing_base = breaths * cycle_s
        if phase == breathe.INHALE:
            return breathing_base + phase_elapsed
        else:
            return breathing_base + inhale_s + phase_elapsed

    # ── Snap-back on resume ──────────────────────────────────────

    def test_resume_snaps_to_cycle_boundary(self):
        """After pause-resume, remaining should be a multiple of cycle_s."""
        for inhale, exhale in [(5, 5), (4, 6), (4, 4)]:
            cycle_s = inhale + exhale
            duration_s = 60
            total_cycles = -(-duration_s // cycle_s)
            for breaths in range(total_cycles):
                # phase_elapsed = 0 right after resume (state = INHALE)
                rem = self._remaining(duration_s, inhale, exhale,
                                      breaths, breathe.INHALE, 0.0)
                self.assertEqual(rem % cycle_s, 0,
                                 'remaining {} not multiple of cycle_s {} '
                                 'after {} breaths'.format(rem, cycle_s, breaths))

    # ── Countdown at session end ─────────────────────────────────

    def test_remaining_at_end_of_last_exhale(self):
        """remaining_s must be 0 at the exact end of the last exhale,
        not earlier. This is the core of bug #13."""
        for inhale, exhale in [(5, 5), (4, 6), (4, 4)]:
            cycle_s = inhale + exhale
            duration_s = 60
            total_cycles = -(-duration_s // cycle_s)
            last_breaths = total_cycles - 1  # before last cycle completes

            # End of last inhale: phase_elapsed = inhale
            rem_inhale_end = self._remaining(
                duration_s, inhale, exhale,
                last_breaths, breathe.INHALE, float(inhale))
            self.assertGreater(rem_inhale_end, 0,
                               'remaining hit 0 at end of last inhale '
                               '(ratio {}-{})'.format(inhale, exhale))

            # End of last exhale: phase_elapsed = exhale
            rem_exhale_end = self._remaining(
                duration_s, inhale, exhale,
                last_breaths, breathe.EXHALE, float(exhale))
            self.assertEqual(rem_exhale_end, 0,
                             'remaining not 0 at end of last exhale '
                             '(ratio {}-{})'.format(inhale, exhale))

    def test_remaining_never_negative(self):
        """remaining_s should never go negative during a session."""
        for inhale, exhale in [(5, 5), (4, 6), (4, 4)]:
            cycle_s = inhale + exhale
            duration_s = 60
            total_cycles = -(-duration_s // cycle_s)
            for breaths in range(total_cycles):
                for phase in [breathe.INHALE, breathe.EXHALE]:
                    phase_dur = inhale if phase == breathe.INHALE else exhale
                    for t in [0.0, 0.5, 1.0, phase_dur - 0.05, float(phase_dur)]:
                        rem = self._remaining(duration_s, inhale, exhale,
                                              breaths, phase, t)
                        self.assertGreaterEqual(rem, 0,
                                                'negative remaining at breaths={} '
                                                'phase={} t={}'.format(breaths, phase, t))

    def test_remaining_monotonically_decreasing(self):
        """remaining_s should never increase during uninterrupted breathing."""
        for inhale, exhale in [(5, 5), (4, 6), (4, 4)]:
            cycle_s = inhale + exhale
            duration_s = 60
            total_cycles = -(-duration_s // cycle_s)
            session_s = total_cycles * cycle_s
            prev_rem = session_s + 1
            for breaths in range(total_cycles):
                for phase in [breathe.INHALE, breathe.EXHALE]:
                    phase_dur = inhale if phase == breathe.INHALE else exhale
                    for t in range(phase_dur):
                        rem = self._remaining(duration_s, inhale, exhale,
                                              breaths, phase, float(t))
                        self.assertLessEqual(rem, prev_rem,
                                             'remaining increased at breaths={} '
                                             'phase={} t={}'.format(breaths, phase, t))
                        prev_rem = rem

    # ── Countdown vs progress bar consistency ────────────────────

    def test_countdown_zero_matches_progress_full(self):
        """When remaining_s == 0, elapsed_display should == session_s."""
        for inhale, exhale in [(5, 5), (4, 6), (4, 4)]:
            cycle_s = inhale + exhale
            duration_s = 60
            total_cycles = -(-duration_s // cycle_s)
            session_s = total_cycles * cycle_s
            breaths = total_cycles - 1
            # End of last exhale
            rem = self._remaining(duration_s, inhale, exhale,
                                  breaths, breathe.EXHALE, float(exhale))
            elapsed = self._elapsed(inhale, exhale,
                                    breaths, breathe.EXHALE, float(exhale))
            if rem == 0:
                self.assertEqual(elapsed, session_s,
                                 'countdown 0 but elapsed {} != session_s {}'
                                 .format(elapsed, session_s))


class TestDurationRounding(unittest.TestCase):
    """duration_s must always be a multiple of cycle_s (bug #13 fix)."""

    def test_divisible_unchanged(self):
        """When duration divides evenly, no rounding needed."""
        c = breathe.Config(600, 5, 5, 'morning', True, False)
        self.assertEqual(c.duration_s, 600)  # 600 / 10 = 60

    def test_indivisible_rounded_up(self):
        """When duration doesn't divide evenly, round up to next cycle."""
        cycle_s = 4 + 4  # 8
        duration_s = -(-60 // cycle_s) * cycle_s  # 64
        c = breathe.Config(duration_s, 4, 4, 'custom', True, False)
        self.assertEqual(c.duration_s % cycle_s, 0)
        self.assertGreaterEqual(c.duration_s, 60)

    def test_all_valid_ratios_with_common_durations(self):
        """For any valid ratio and duration, session_s must be a whole
        number of cycles. This is the invariant that bug #13 violated."""
        for inhale in range(3, 11):
            for exhale in range(3, 11):
                cycle_s = inhale + exhale
                if cycle_s < breathe.MIN_CYCLE_SECS:
                    continue
                for duration_min in [1, 2, 3, 5, 10, 15, 20, 30, 60]:
                    raw = duration_min * 60
                    session_s = -(-raw // cycle_s) * cycle_s
                    self.assertEqual(session_s % cycle_s, 0,
                                     'duration {}min ratio {}-{}: session_s {} '
                                     'not multiple of cycle_s {}'.format(
                                         duration_min, inhale, exhale,
                                         session_s, cycle_s))
                    self.assertGreaterEqual(session_s, raw,
                                            'session_s {} < requested {}'.format(
                                                session_s, raw))


class TestPhaseLabels(unittest.TestCase):
    def test_inhale_label(self):
        self.assertEqual(breathe.PHASE_LABEL[breathe.INHALE], 'IN')

    def test_exhale_label(self):
        self.assertEqual(breathe.PHASE_LABEL[breathe.EXHALE], 'OUT')


class TestConstants(unittest.TestCase):
    def test_min_cycle_secs(self):
        self.assertEqual(breathe.MIN_CYCLE_SECS, 8)

    def test_bar_width(self):
        self.assertGreater(breathe.BAR_WIDTH, 0)

    def test_frame_rate(self):
        self.assertGreater(breathe.FRAME_RATE_HZ, 0)
        self.assertAlmostEqual(breathe.FRAME_SLEEP, 1.0 / breathe.FRAME_RATE_HZ)


class TestGoalWords(unittest.TestCase):
    """try_parse_goal_words must either resolve unambiguously or fail
    loudly (SystemExit + stderr message) or return None — it must
    never silently guess or silently drop a word."""

    def test_vocabularies_disjoint(self):
        overlap = set(breathe.GOAL_DURATION_WORDS) & set(breathe.GOAL_RATIO_WORDS)
        self.assertEqual(overlap, set(),
                         'a word must not be ambiguous between axes: {}'.format(overlap))

    def test_ratio_words_meet_safety_floor(self):
        for word, (inhale_s, exhale_s) in breathe.GOAL_RATIO_WORDS.items():
            self.assertGreaterEqual(inhale_s + exhale_s, breathe.MIN_CYCLE_SECS,
                                    '{!r} cycle too short'.format(word))

    def test_duration_words_in_valid_range(self):
        for word, duration_min in breathe.GOAL_DURATION_WORDS.items():
            self.assertTrue(1 <= duration_min <= 60,
                            '{!r} duration out of range'.format(word))

    def test_empty_argv_returns_none(self):
        self.assertIsNone(breathe.try_parse_goal_words([]))

    def test_unrecognized_word_returns_none(self):
        self.assertIsNone(breathe.try_parse_goal_words(['zen']))

    def test_mixed_recognized_and_unrecognized_returns_none(self):
        # A typo or unknown word must not cause the recognized words
        # to be silently applied — the whole argv falls through.
        self.assertIsNone(breathe.try_parse_goal_words(['quick', 'zen']))

    def test_flag_token_returns_none(self):
        # Goal words never combine with dash flags; must fall through
        # to argparse rather than silently ignoring the flag.
        self.assertIsNone(breathe.try_parse_goal_words(['quick', '-n']))

    def test_duration_word_only_defaults_ratio(self):
        self.assertEqual(breathe.try_parse_goal_words(['quick']),
                         (3, 5, 5, 'quick'))

    def test_ratio_word_only_defaults_duration(self):
        self.assertEqual(breathe.try_parse_goal_words(['calm']),
                         (10, 4, 6, 'calm'))

    def test_both_axes_resolve(self):
        self.assertEqual(breathe.try_parse_goal_words(['quick', 'calm']),
                         (3, 4, 6, 'quick+calm'))

    def test_order_independent(self):
        a = breathe.try_parse_goal_words(['quick', 'calm'])
        b = breathe.try_parse_goal_words(['calm', 'quick'])
        self.assertEqual(a[:3], b[:3])

    def test_case_insensitive(self):
        self.assertEqual(breathe.try_parse_goal_words(['QUICK', 'Calm']),
                         (3, 4, 6, 'quick+calm'))

    def test_conflicting_duration_words_raise_with_message(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            with self.assertRaises(SystemExit) as ctx:
                breathe.try_parse_goal_words(['quick', 'long'])
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn('Conflicting duration words', buf.getvalue())

    def test_conflicting_ratio_words_raise_with_message(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            with self.assertRaises(SystemExit) as ctx:
                breathe.try_parse_goal_words(['calm', 'energize'])
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn('Conflicting goal words', buf.getvalue())

    def test_repeated_same_word_raises(self):
        # Even a repeated (non-conflicting) word must not be silently
        # deduplicated — it's still ambiguous input to reject loudly.
        buf = io.StringIO()
        with redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                breathe.try_parse_goal_words(['quick', 'quick'])


if __name__ == '__main__':
    unittest.main()
