import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import wave

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]


class PrepareRegression(unittest.TestCase):
    def test_fresh_workspace_prepares_all_stages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ['studio/list-demo/editor-settings.json',
                             'studio/list-concat-demo/lesson.py']:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((REPO / relative).read_bytes())
            audio = root / 'build/docker/list-concat-demo/audio'
            audio.mkdir(parents=True)
            for index in range(1, 4):
                with wave.open(str(audio / f'{index:02}.audio'), 'wb') as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(16000)
                    wav.writeframes(b'\x00\x00' * 16000)
            # Relocate only the container mount root; execute the original logic.
            source = (HERE / 'prepare_v2.py').read_text().replace(
                "ROOT = Path('/workspace')", f'ROOT = Path({str(root)!r})')
            script = root / 'prepare_v2.py'
            script.write_text(source)
            result = subprocess.run(['python3', str(script)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads((root / 'build/docker/list-concat-demo/v2/timeline.json').read_text())
            self.assertEqual(len(plan['stages']), 3)
            for stage in plan['stages']:
                file = Path(plan['workspace']) / stage['file']
                self.assertEqual(file.read_text(), stage['source'])
                actual = subprocess.run(['python3', str(file)], capture_output=True, text=True)
                self.assertEqual(actual.returncode, 0, actual.stderr)
                self.assertEqual(actual.stdout, stage['expected_stdout'])
            self.assertFalse((root / 'build/docker/list-concat-demo/workspace').exists())


if __name__ == '__main__':
    unittest.main()
