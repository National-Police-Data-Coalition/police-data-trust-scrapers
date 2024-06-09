import shutil
from pathlib import PosixPath


def delete_and_recreate_directory(directory: PosixPath) -> None:
    if directory.exists():
        shutil.rmtree(directory)

    directory.mkdir(parents=True, exist_ok=True)
