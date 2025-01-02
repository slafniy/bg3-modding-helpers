import argparse
import os

from pathlib import Path
from typing import List, Dict

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
        self.project_root: Path = self.ensure_project_root()
        self.junction_map : Dict[Path, Path] = self.prepare_junction_map()  # source: target

        self.make_junctions()


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


    def ensure_project_root(self) -> Path:
        path = Path(self.arguments.path) if self.arguments.path is not None else Path.cwd() / self.arguments.name
        assert path.is_dir() or not path.exists(), f'"{path}" is not a directory!'

        if not path.exists():
            path.mkdir()

        print(f'Project folder: {path}')
        return path

    def make_junctions(self):
        for source, target in self.junction_map.items():
            cmd = f'mklink /J "{target}" "{source}"'
            print(f'Executing "{cmd}"')
            os.system(cmd)

    def prepare_junction_map(self) -> Dict[Path, Path]:
        result = {}
        for p in JUNCTION_TARGETS:
            mod_source = Path(self.data_folder / p / self.mod_name)
            assert mod_source.exists(), f'"{mod_source}" does not exist!'
            assert mod_source.is_dir(), f'"{mod_source}" is not a directory!'

            mod_target = self.project_root / p / self.mod_name
            assert mod_target.is_dir() or not mod_target.exists(), f'"{mod_target}" is not a directory!'
            os.makedirs(mod_target.parent, exist_ok=True)

            result[mod_source] = mod_target

        return result


if __name__ == '__main__':
    assert os.name == 'nt', 'This scripts creates directory junctions and works only on Windows'

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