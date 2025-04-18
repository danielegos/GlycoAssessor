import os

def collect_add_data_args(base_dir):
    args = []
    for root, dirs, files in os.walk(base_dir):
        for name in dirs:
            if name in ["__pycache__", "build", "dist"]:
                continue
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, base_dir)
            args.append(f'--add-data "{rel_path};{rel_path}"')
    return args

args = collect_add_data_args(".")

print("pyinstaller --onefile --noconsole --icon=Assets/tsg_lab_logo.ico GlycoAssessor.py ^")
for a in args:
    print("  " + a + " ^")
