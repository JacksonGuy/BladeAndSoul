import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python36\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Pokemon: Blade and Soul",
    options={"build_exe": {"packages":["pygame"],
    "include_files":["abilities.py","chaos.py","header1.py"]}},
    executables = executables,
    version="1.2.0"
)
