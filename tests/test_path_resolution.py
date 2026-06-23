import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path


class FlappyBirdEnvPathResolutionTests(unittest.TestCase):
    def test_config_is_loaded_from_repo_root_when_cwd_changes(self):
        repo_root = Path(__file__).resolve().parents[1]
        original_cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                sys.modules.pop("ai.flappybird_env", None)
                import ai.flappybird_env as env_module

                self.assertEqual(env_module.CONFIG.get("screen_width"), 423)
                self.assertEqual(env_module.CONFIG.get("pipe_gap"), 150)
                self.assertEqual(env_module.CONFIG.get("epsilon_decay"), 0.95)
            finally:
                os.chdir(original_cwd)
                sys.modules.pop("ai.flappybird_env", None)


if __name__ == "__main__":
    unittest.main()
