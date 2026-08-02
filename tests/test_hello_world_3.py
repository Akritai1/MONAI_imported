# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Black-box CLI tests for ``scripts/hello_world_3.py``.

These tests invoke the script as a subprocess (never importing it directly)
so that they validate the actual externally observable "executable" contract
described in ``specs/003-hello-world-3/contracts/cli-contract.md``, rather
than any implementation detail.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "hello_world_3.py"
EXPECTED_OUTPUT = "hello world 3"
ALLOWED_STDOUT = (EXPECTED_OUTPUT, EXPECTED_OUTPUT + "\n")


def _minimal_env() -> dict[str, str]:
    """Build a minimal environment with no feature-specific configuration.

    Only the bare essentials required by the OS/interpreter to start a
    process at all are kept, to validate that no special setup is needed.
    """
    env = {"PATH": os.environ.get("PATH", "")}
    if os.name == "nt":
        system_root = os.environ.get("SystemRoot") or os.environ.get("SYSTEMROOT")
        if system_root:
            env["SystemRoot"] = system_root
    return env


def run_script(args: list[str] | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Invoke the executable as a subprocess and return the completed process."""
    cmd = [sys.executable, str(SCRIPT_PATH), *(args or [])]
    return subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5, env=env)


class TestHelloWorld3(unittest.TestCase):
    """Covers User Story 1: run the executable and see the greeting."""

    def test_prints_hello_world_3_and_exits_success(self):
        result = run_script()
        self.assertIn(result.stdout, ALLOWED_STDOUT)
        self.assertEqual(result.returncode, 0)

    def test_requires_no_input_or_configuration(self):
        start = time.monotonic()
        result = run_script()
        elapsed = time.monotonic() - start
        self.assertEqual(result.returncode, 0)
        self.assertLess(elapsed, 1.0)


class TestHelloWorld3Automation(unittest.TestCase):
    """Covers User Story 2: call the executable repeatedly or from scripts/automation."""

    def test_repeated_invocations_are_deterministic(self):
        outputs = []
        for _ in range(100):
            result = run_script()
            self.assertEqual(result.returncode, 0)
            outputs.append(result.stdout)
        self.assertTrue(all(output == outputs[0] for output in outputs))
        self.assertIn(outputs[0], ALLOWED_STDOUT)

    def test_runs_noninteractively_with_redirected_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "out.txt"
            with open(out_path, "w", encoding="utf-8") as out_file:
                result = subprocess.run(
                    [sys.executable, str(SCRIPT_PATH)],
                    stdin=subprocess.DEVNULL,
                    stdout=out_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5,
                )
            self.assertEqual(result.returncode, 0)
            self.assertIn(out_path.read_text(encoding="utf-8"), ALLOWED_STDOUT)

    def test_extra_arguments_are_ignored(self):
        result = run_script(args=["--unexpected-flag", "some-value", "positional-arg"])
        self.assertIn(result.stdout, ALLOWED_STDOUT)
        self.assertEqual(result.returncode, 0)

    def test_concurrent_invocations_do_not_interfere(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_script) for _ in range(5)]
            results = [future.result() for future in futures]
        for result in results:
            self.assertIn(result.stdout, ALLOWED_STDOUT)
            self.assertEqual(result.returncode, 0)


class TestHelloWorld3Discoverability(unittest.TestCase):
    """Covers User Story 3: discover how to call the executable."""

    def test_callable_directly_by_path_with_no_setup(self):
        result = run_script(env=_minimal_env())
        self.assertIn(result.stdout, ALLOWED_STDOUT)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
