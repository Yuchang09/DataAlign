import os
import re
from pathlib import Path

class PathUtils:

    @staticmethod
    def extract_mouse_id(filepath):
        path = Path(filepath)

        match = re.search(r'm\d+d\d+', str(path))

        if match:
            return match.group()

        return None

    @staticmethod
    def get_root_dir_path():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_plot_dir_path():
        return PathUtils.join_path(PathUtils.get_root_dir_path(), "plots")

    @staticmethod
    def get_file_dir_path():
        return PathUtils.join_path(PathUtils.get_root_dir_path(), "files")

    @staticmethod
    def make_dir(path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def make_mouse_plot_dir(mouse_id):
        plot_dir = PathUtils.join_path(PathUtils.get_plot_dir_path(), mouse_id)
        PathUtils.make_dir(plot_dir)

        return plot_dir

    @staticmethod
    def make_mouse_file_dir(mouse_id):
        file_dir = PathUtils.join_path(PathUtils.get_file_dir_path(), mouse_id)
        PathUtils.make_dir(file_dir)

        return file_dir

    @staticmethod
    def join_path(*paths):
        return os.path.join(*paths)