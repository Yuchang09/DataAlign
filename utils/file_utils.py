import pandas as pd
from utils.msg_utils import Msg
from scipy.io import loadmat
import numpy as np

class FileUtils:

    @staticmethod
    def read_csv_file(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception:
            Msg.print_error("Error while reading from " + filepath)
            raise

    @staticmethod
    def read_mat_file(filepath):
        try:
            return loadmat(filepath)

        except Exception:
            Msg.print_error("Error while reading from " + filepath)
            raise

    @staticmethod
    def write_csv_file(filepath, data):
        try:
            if isinstance(data, np.ndarray):
                data = pd.DataFrame(data)

            data.to_csv(filepath, index=False)

        except Exception as e:
            Msg.print_error(f"Error while writing to {filepath}: {e}")


    @staticmethod
    def write_npz_file(filepath, **data):
        try:
            np.savez(filepath, **data)

        except Exception as e:
            Msg.print_error(f"Error while writing to {filepath}: {e}")


    @staticmethod
    def read_npz_file(filepath):
        try:
            return np.load(filepath)

        except Exception as e:
            Msg.print_error(f"Error while reading {filepath}: {e}")
            return None


