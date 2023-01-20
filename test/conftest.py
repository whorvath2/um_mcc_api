import os
import sys

# add the parent directory to the path per noqa: E402
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
