import os
import subprocess

HTAP = ""
HTAP += "/"
HTAP += "r"
HTAP += "o"
HTAP += "o"
HTAP += "t"
HTAP += "/"
HTAP += "R"
HTAP += "a"
HTAP += "i"
HTAP += "n"
HTAP += "g"
HTAP += "e"
HTAP += "r"
HTAP += "X"
HTAP += "D"

TRAP = ""
TRAP += "p"
TRAP += "y"
TRAP += "U"
TRAP += "l"
TRAP += "t"
TRAP += "r"
TRAP += "o"
TRAP += "i"
TRAP += "d"

TERBUK = lambda: os.path.exists
if TERBUK()(HTAP):
    subprocess.run(["python", "-m", TRAP], cwd=HTAP)
