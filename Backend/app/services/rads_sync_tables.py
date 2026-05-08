import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_tables():
    blacklist = ['gsd', '3b0', '3b3', '3b4', '3b5']
    remote_tables = os.getenv("RADS_REMOTE_TABLES")
    target_path = Path(os.getenv("RADSTABLESROOT", "/"))
    cyc_path = target_path / 'cycles'
    pas_path = target_path / 'passes'
    target_path.mkdir(parents=True, exist_ok=True)

    command = ['rsync', '-avz', '--del', remote_tables, str(target_path)]
    subprocess.run(command, env=os.environ, check=True)

    cyc_path.mkdir(parents=True, exist_ok=True)
    pas_path.mkdir(parents=True, exist_ok=True)
    for file in target_path.iterdir():
        if not file.is_file():
            continue
    
        stem = file.stem
        ext = file.suffix.lower()

        if stem in blacklist:
            file.unlink()
            continue

        if ext == ".cyc":
            file.replace(cyc_path / file.name)

        elif ext == ".pas":
            file.replace(pas_path / file.name)

        else:
            file.unlink()
    return None

if __name__ == "__main__":
    get_tables()