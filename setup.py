import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Pokemon: Blade and Soul",
    options={"build_exe": {"packages":["pygame"],
    "include_files":["abilities.py","chaos.py","header1.py"]}},
    executables = executables,
    version="1.0.0"
)
