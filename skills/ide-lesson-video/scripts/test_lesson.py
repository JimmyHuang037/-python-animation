"""Regression checks; configure the two font environment variables before running."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

import imageio_ffmpeg
import numpy as np

from lesson_audio import SAMPLE_RATE, AUDIO_FILTER, compare_samples, decode_audio

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / 'assets' / 'list-demo'
FONT_PATHS = [os.environ.get(name, '') for name in ('IDE_VIDEO_CODE_FONT', 'IDE_VIDEO_UI_FONT')]
HAVE_FONTS = all(Path(path).is_file() for path in FONT_PATHS)


class FinalAudioTests(unittest.TestCase):
    def setUp(self):
        t = np.arange(SAMPLE_RATE * 3) / SAMPLE_RATE
        self.expected = .1 * np.sin(2 * np.pi * 440 * t)

    def test_small_codec_error_is_allowed(self):
        result = compare_samples(self.expected * .99, self.expected)
        self.assertTrue(result['final_audio_verified'])

    def test_silence_and_missing_typing_window_are_rejected(self):
        for start, end in [(0, len(self.expected)), (SAMPLE_RATE, SAMPLE_RATE * 2)]:
            actual = self.expected.copy()
            actual[start:end] = 0
            with self.assertRaisesRegex(AssertionError, 'differs from the mix'):
                compare_samples(actual, self.expected)

    def test_unexpected_sound_and_duration_are_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'Unexpected sound'):
            compare_samples(self.expected, np.zeros_like(self.expected))
        with self.assertRaisesRegex(AssertionError, 'duration'):
            compare_samples(self.expected[:-2048], self.expected)

    def test_fractional_video_duration_preserves_audio_tail(self):
        samples = 304 * SAMPLE_RATE // 30
        track = np.zeros(samples, dtype='<i2')
        track[:len(self.expected)] = np.round(self.expected * 32767).astype('<i2')
        track[-4800:] = track[:4800]
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / 'mix.wav'
            with wave.open(str(audio), 'wb') as wav:
                wav.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
                wav.writeframes(track.tobytes())
            decoded = decode_audio(imageio_ffmpeg.get_ffmpeg_exe(), audio,
                                   samples / SAMPLE_RATE, AUDIO_FILTER)
            self.assertEqual(len(decoded), samples)
            self.assertTrue(np.any(decoded[-3200:]))

    def test_video_without_audio_is_rejected(self):
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / 'silent.mp4'
            subprocess.run([ffmpeg, '-v', 'error', '-f', 'lavfi', '-i', 'color=s=16x16',
                            '-t', '0.1', '-an', str(video)], check=True, capture_output=True)
            with self.assertRaisesRegex(ValueError, 'required audio track'):
                decode_audio(ffmpeg, video, .1)


@unittest.skipUnless(HAVE_FONTS, 'Set IDE_VIDEO_CODE_FONT and IDE_VIDEO_UI_FONT')
class TimingAndAnnotationTests(unittest.TestCase):
    def preflight(self, change):
        lesson = json.loads((ASSETS / 'lesson.json').read_text())
        for stage in lesson['stages']:
            for key in ('source', 'audio'):
                stage[key] = str(ASSETS / stage[key])
        change(lesson)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'lesson.json'
            path.write_text(json.dumps(lesson))
            return subprocess.run([sys.executable, str(HERE / 'render_lesson.py'),
                                   '--lesson', str(path), '--output', str(Path(directory) / 'lesson.mp4'),
                                   '--preflight'], capture_output=True, text=True)

    def test_default_and_four_second_wait(self):
        default = self.preflight(lambda lesson: lesson.pop('timing'))
        self.assertEqual(default.returncode, 0, default.stderr)
        configured = self.preflight(lambda lesson: lesson['timing'].update(after_typing=4))
        self.assertEqual(configured.returncode, 0, configured.stderr)
        self.assertEqual(json.loads(configured.stdout)['frames'] - json.loads(default.stdout)['frames'], 18)

    def test_short_wait_requires_no_annotations(self):
        rejected = self.preflight(lambda lesson: lesson['timing'].update(after_typing=1))
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('at least 3.8 seconds', rejected.stderr)

        def without_annotations(lesson):
            lesson['timing']['after_typing'] = 1
            for stage in lesson['stages']:
                stage.pop('annotations')

        accepted = self.preflight(without_annotations)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)

    def test_connector_is_transparent_at_entrance_and_exit(self):
        import lesson_style as style
        stage = dict(annotations=[dict(row=0, text='注释')], circle_frame=0,
                     bubble_frame=30, bubble_end_frame=72,
                     bubble_exit_frame=100, bubble_exit_end_frame=136)
        state = dict(lines=['print(1)'], row=0, col=8)
        background = style.BASE.copy()
        for frame in (30, 136):
            rendered = background.copy()
            style._draw_annotations(rendered, 0, state, [stage], frame)
            self.assertTrue(np.array_equal(np.array(rendered), np.array(background)), frame)
        visible = background.copy()
        style._draw_annotations(visible, 0, state, [stage], 72)
        self.assertFalse(np.array_equal(np.array(visible), np.array(background)))


if __name__ == '__main__':
    unittest.main()
