"""manual_kernels.py --- Hand-authored side-by-side kernels.

KERNELS[key][approach_index] = {"py": ..., "cpp": ...} overrides the
auto-harvested kernel from harvest.py. Written by hand so every row is
brace-balanced, boilerplate-free and matched line-for-line across languages.
"""

import json
from pathlib import Path

KERNELS = json.loads(Path(__file__).with_name("kernels.json").read_text())
