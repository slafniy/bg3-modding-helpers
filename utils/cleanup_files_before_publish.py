import argparse
from pathlib import Path

GITIGNORE_FILE = ".gitignore"

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--path', help='Project folder path', required=True)

    args = arg_parser.parse_args()

    safe_to_remove = []

    with (Path(args.path) / GITIGNORE_FILE).open() as gitignore_file:
        is_safe_to_remove_block = False
        for line in gitignore_file.readlines():
            if line.startswith("# SAFETOREMOVE_START"):
                is_safe_to_remove_block = True
                continue
            if line.startswith("# SAFETOREMOVE_END"):
                is_safe_to_remove_block = False
            if is_safe_to_remove_block:
                safe_to_remove.append(line[:-1])

    safe_to_remove_resolved = set()
    for path in safe_to_remove:
        resolved = Path(f'{args.path}{path}').resolve()
        safe_to_remove_resolved.add(resolved)

    print('Safe to remove file list from .gitignore:')
    [print(f) for f in safe_to_remove_resolved]

    for file_to_remove in safe_to_remove_resolved:
        if file_to_remove.exists():
            print(f'Removing {file_to_remove}')
            file_to_remove.unlink()
        else:
            print(f'{file_to_remove} does not exist')
