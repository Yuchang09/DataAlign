import pandas as pd
from utils.msg_utils import Msg
from scipy.io import loadmat

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
    def write_csv_file(filepath, df):
        try:
            df.to_csv(filepath, index=False)
        except Exception:
            Msg.print_error("Error while writing to " + filepath)
