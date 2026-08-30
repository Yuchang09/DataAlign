import pandas as pd
from utils.msg_utils import Msg

class FileUtils:

    @staticmethod
    def read_excel_file(filepath):
        try:
            return pd.read_excel(filepath)
        except Exception:
            Msg.print_error("Error while reading from " + filepath)
            raise