"""Check the encoded soundtrack against the mix used by the renderer."""
import subprocess

import numpy as np

# Reset loudnorm/resampler timestamps before the encoder's duration limit.
AUDIO_FILTER = 'loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,asetpts=N/SR/TB'
SAMPLE_RATE = 48000



def decode_audio(ffmpeg, path, duration, filters=None):
    command = [ffmpeg, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-vn']
    if filters:
        command += ['-af', filters]
    command += ['-t', str(duration), '-ar', str(SAMPLE_RATE), '-ac', '1', '-f', 'f32le', '-']
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise ValueError('Cannot decode the required audio track: ' + result.stderr.decode('utf-8', errors='replace'))
    return np.frombuffer(result.stdout, dtype='<f4')


def compare_samples(actual, expected):
    # AAC can pad the final packet by up to 1023 samples. MP4 normally trims it.
    assert len(actual) and len(expected) and abs(len(actual) - len(expected)) <= 1023, 'Final audio duration differs from the mix'
    length = min(len(actual), len(expected))
    actual, expected = actual[:length].astype(np.float64), expected[:length].astype(np.float64)
    assert np.isfinite(actual).all() and np.isfinite(expected).all(), 'Invalid audio samples'
    window_errors = []
    for start in range(0, length, SAMPLE_RATE):
        reference = expected[start:start + SAMPLE_RATE]
        decoded = actual[start:start + SAMPLE_RATE]
        energy = float(np.mean(reference ** 2))
        error = float(np.mean((decoded - reference) ** 2))
        if energy > 1e-10:
            # At 192 kbps the provided sample measures < 0.03 NRMSE; allow
            # codec differences while rejecting lost speech or typing windows.
            nrmse = (error / energy) ** .5
            assert nrmse < .15, f'Final audio differs from the mix at {start / SAMPLE_RATE:g}s (NRMSE {nrmse:.3f})'
            window_errors.append(nrmse)
        else:
            assert error < 1e-6, f'Unexpected sound at {start / SAMPLE_RATE:g}s'
    return dict(final_audio_verified=True, final_audio_max_window_nrmse=max(window_errors, default=0.0))


def verify_final_audio(ffmpeg, video, mix, duration):
    actual = decode_audio(ffmpeg, video, duration)
    expected = decode_audio(ffmpeg, mix, duration, AUDIO_FILTER)
    assert abs(len(expected) - round(duration * SAMPLE_RATE)) <= 1, 'Mix duration differs from the video'
    return compare_samples(actual, expected)
