from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

base = None
executables = [Executable("main.py", base=base)]
packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name = "lord-thingworx",
    options = options,
    version = "0.0.1",
    description = "Interface Lord and ThingWorx",
    executables = executables
)