import os
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        "APP.py",
        "ENTIDADES.py",
        "CAMPOS.py",
        "ENUMS.py",
        "RELACIONAMENTOS.py",
        "OPTIONS.py",
        "JOIN_JDLS.py",
        "FIX_COMPLETE_JDL.py"
    ]

    for script in scripts:
        script_path = os.path.join(base_dir, script)
        print(f"Running {script_path} ...")
        subprocess.run(["python", script_path], check=True)
        print(f"Finished {script_path}\n")

    print("All scripts executed successfully!")

if __name__ == "__main__":
    main()
