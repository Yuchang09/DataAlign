import pandas as pd
from scipy.signal import find_peaks
from utils.msg_utils import Msg

class AnalysisUtil:

    @staticmethod
    def find_event(
            df,
            signal_column,
            time_column,
            prominence=1,
            values=False
    ):

        if isinstance(signal_column, int):
            if signal_column < 0 or signal_column >= len(df.columns):
                Msg.print_error(
                    f"Signal column index {signal_column} is out of range. "
                    f"DataFrame has {len(df.columns)} columns."
                )
                raise IndexError

            signal_column = df.columns[signal_column]

        elif isinstance(signal_column, str):
            if signal_column not in df.columns:
                Msg.print_error(
                    f"Signal column '{signal_column}' does not exist. "
                    f"Available columns: {list(df.columns)}"
                )
                raise KeyError

        else:
            Msg.print_error(
                "signal_column must be either a column name (str) or column index (int)."
            )
            raise TypeError

        if isinstance(time_column, int):
            if time_column < 0 or time_column >= len(df.columns):
                Msg.print_error(
                    f"Time column index {time_column} is out of range. "
                    f"DataFrame has {len(df.columns)} columns."
                )
                raise IndexError

            time_column = df.columns[time_column]

        elif isinstance(time_column, str):
            if time_column not in df.columns:
                Msg.print_error(
                    f"Time column '{time_column}' does not exist. "
                    f"Available columns: {list(df.columns)}"
                )
                raise KeyError

        else:
            Msg.print_error(
                "time_column must be either a column name (str) or column index (int)."
            )
            raise TypeError

        signal = df[signal_column]

        peaks, properties = find_peaks(
            signal,
            prominence=prominence
        )

        # Return peak values and times
        if values:
            return signal.iloc[peaks], df[time_column].iloc[peaks]

        return df[time_column].iloc[peaks]