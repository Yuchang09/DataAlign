import pandas as pd
from scipy.signal import find_peaks
from utils.msg_utils import Msg

class AnalysisUtil:

    @staticmethod
    def find_event(
            df,
            signal_column,
            time_column,
            threshold,
            onset = True
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

        above_threshold = signal >= threshold

        if onset:
            event = above_threshold & ~above_threshold.shift(fill_value=False)
        else:
            event = above_threshold & ~above_threshold.shift(-1, fill_value=False)

        return df.loc[event, time_column]


    @staticmethod
    def calculate_puff_tone_difference(tone_times, puff_times):

        results = []

        for puff_time in puff_times:

            # Find tones that occurred before this puff
            previous_tones = tone_times[tone_times < puff_time]

            if len(previous_tones) == 0:
                # No tone before this puff
                continue

            # The last tone before the puff
            nearest_tone = previous_tones.iloc[-1]

            difference = puff_time - nearest_tone

            results.append({
                "tone_time": nearest_tone,
                "puff_time": puff_time,
                "difference": difference
            })

        return pd.DataFrame(results)

    @staticmethod
    def build_event_dataframe(
            tone_onset,
            tone_offset,
            puff_onset,
            puff_offset
    ):
        result = pd.DataFrame({
            "tone_onset_time": tone_onset.values,
            "tone_onset_index": tone_onset.index,
            "tone_offset_time": tone_offset.values,
            "tone_offset_index": tone_offset.index
        })

        result["puff_onset_time"] = pd.NA
        result["puff_onset_index"] = pd.NA
        result["puff_offset_time"] = pd.NA
        result["puff_offset_index"] = pd.NA

        for puff_index, puff_time in puff_onset.items():

            previous_tones = tone_onset[
                tone_onset < puff_time
                ]

            if previous_tones.empty:
                continue

            tone_index = previous_tones.index[-1]

            tone_row = result.index[
                result["tone_onset_index"] == tone_index
                ][0]

            # Add puff information
            result.loc[tone_row, "puff_onset_time"] = puff_time
            result.loc[tone_row, "puff_onset_index"] = puff_index

            previous_offsets = puff_offset[
                puff_offset.index > puff_index
                ]

            if not previous_offsets.empty:
                offset_index = previous_offsets.index[0]
                offset_time = previous_offsets.iloc[0]

                result.loc[tone_row, "puff_offset_time"] = offset_time
                result.loc[tone_row, "puff_offset_index"] = offset_index

        result["ISI_length"] = (
                result["puff_onset_time"]
                - result["tone_offset_time"]
        )

        result["tone_puff_difference"] = (
                result["puff_onset_time"]
                - result["tone_onset_time"]
        )

        result["tone_length"] = (
            result["tone_offset_time"]
            - result["tone_onset_time"]
        )

        result["puff_length"] = (
            result["puff_offset_time"]
            - result["puff_onset_time"]
        )

        return result