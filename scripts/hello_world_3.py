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

"""Standalone smoke-test executable that prints ``hello world 3``.

This script lives outside the ``monai`` package because it has no
medical-imaging content; it exists purely as a directly callable smoke-test
utility (see ``specs/003-hello-world-3/``). It takes no input, requires no
configuration, and is deterministic and stateless across invocations.
"""

from __future__ import annotations


def main() -> None:
    """Print the literal greeting to standard output.

    Any command-line arguments are intentionally ignored; the function
    always produces the same output and returns normally on success.
    """
    print("hello world 3")


if __name__ == "__main__":
    main()
