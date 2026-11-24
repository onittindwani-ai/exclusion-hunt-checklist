"""Puts the tools folder on the path for the tests. Offline, standard library only."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
