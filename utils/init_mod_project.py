import argparse

from pathlib import Path
from typing import List

DEFAULT_DATA_PATH = r'C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data'
JUNCTION_TARGETS = [
    'Mods',
    'Editor/Mods',
    'Projects',
    'Public'
]

class _Runner:
    def __init__(self, arguments):
        self.arguments = arguments

        self.data_folder: Path = self.ensure_data_folder()
        self.mod_name: str = self.ensure_mod_name()
        self.mod_folders: List[Path] = self.ensure_mod_folders()
        self.project_folder: Path = self.ensure_project_folder()

    def get_orig_mod_folders(self, data_path: Path):
        pass


    def ensure_data_folder(self) -> Path:
        p_data_path = Path(self.arguments.data_path)
        assert p_data_path.exists(), f'"{p_data_path}" does not exist!'
        assert p_data_path.is_dir(), f'"{p_data_path}" is not a directory!'
        return p_data_path

    def ensure_mod_name(self) -> str:
        glob_result = list(self.data_folder.glob(f'Projects/{self.arguments.name}_*'))
        assert len(glob_result) <= 1, f'Found multiple folders for name "{self.arguments.name}"!'
        assert len(glob_result) == 1, (f'Cannot find "{self.arguments.name}" mod folder '
                                       f'in "{self.data_folder / 'Projects'}"! '
                                       f'Make sure you created this mod in BG3 Toolkit')
        mod_name = glob_result[0].name
        print(f'"{self.arguments.name}" mod unique name: {mod_name}')
        return mod_name

    def ensure_mod_folders(self) -> List[Path]:
        result = []
        for p in JUNCTION_TARGETS:
            mf = Path(self.data_folder / p / self.mod_name)
            assert mf.exists(), f'"{mf}" does not exist!'
            assert mf.is_dir(), f'"{mf}" is not a directory!'
            result.append(mf)

        print('Mod folders:')
        [print(mf) for mf in result]
        return result

    def ensure_project_folder(self) -> Path:
        path = Path(self.arguments.path) if self.arguments.path is not None else Path.cwd() / self.arguments.name
        assert path.is_dir() or not path.exists(), f'"{path}" is not a directory!'

        if not path.exists():
            path.mkdir()

        print(f'Project folder: {path}')
        return path


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-n', '--name', help='Project name without GUID part', required=True)
    arg_parser.add_argument('-p', '--path', help='Path to the project directory. '
                                                 'If not provided - a new directory will be created in the current '
                                                 'working directory.', default=None)
    arg_parser.add_argument('-d', '--data-path', help='Path to BG3 "Data" folder',
                            default=DEFAULT_DATA_PATH)

    args = arg_parser.parse_args()

    print(f'Running with args: {args}')

    runner = _Runner(args)