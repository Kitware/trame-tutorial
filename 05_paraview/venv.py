import os
import site
import sys

if "--venv" in sys.argv:
    # Code taken from virutal-env::bin/active_this.py
    venv_path = sys.argv[sys.argv.index("--venv") + 1]
    bin_dir = os.path.abspath(os.path.join(venv_path, "bin"))
    base = bin_dir[: -len("bin") - 1]
    os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
    os.environ["VIRTUAL_ENV"] = base
    prev_length = len(sys.path)
    python_libs = os.path.join(base, f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages")
    path = os.path.realpath(os.path.join(bin_dir, python_libs))
    site.addsitedir(python_libs.decode("utf-8") if "" else python_libs)
    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]
    sys.real_prefix = sys.prefix
    sys.prefix = base
