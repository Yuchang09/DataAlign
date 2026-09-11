import pandas as pd
from utils.msg_utils import Msg
import numpy as np

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
    def limit_difference(df, start, end, threshold):
        difference = df[end] - df[start]

        mask = (
                df[start].notna()
                & df[end].notna()
                & (difference != threshold)
        )

        df.loc[mask, end] = df.loc[mask, start] + threshold

        return df

    @staticmethod
    def build_event_dataframe(
            tone_onset,
            tone_offset,
            puff_onset,
            puff_offset
    ):
        result = pd.DataFrame({
            "tone_onset_index": tone_onset.index,
            "tone_offset_index": tone_offset.index
        })

        result["puff_onset_index"] = pd.NA
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
            result.loc[tone_row, "puff_onset_index"] = puff_index

            previous_offsets = puff_offset[
                puff_offset.index > puff_index
                ]

            if not previous_offsets.empty:
                offset_index = previous_offsets.index[0]

                result.loc[tone_row, "puff_offset_index"] = offset_index

        return result

    @staticmethod
    def add_diff(result):
        result["ISI_length"] = (
                result["puff_onset_index"]
                - result["tone_offset_index"]
        )

        result["trail_length"] = (
                result["puff_offset_index"]
                - result["tone_onset_index"]
        )

        result["tone_length"] = (
            result["tone_offset_index"]
            - result["tone_onset_index"]
        )

        result["puff_length"] = (
            result["puff_offset_index"]
            - result["puff_onset_index"]
        )
        return result

    @staticmethod
    def calculate_dff(F, frame_rate, window_seconds=60, percentile=10):

        window_frames = int(window_seconds * frame_rate)

        if window_frames < 1:
            raise ValueError("Window must contain at least one frame.")

        F = np.asarray(F, dtype=float)

        F_df = pd.DataFrame(F.T)

        F0_df = (
            F_df
            .rolling(
                window=window_frames,
                center=True,
                min_periods=1
            )
            .quantile(percentile / 100)
        )

        F0 = F0_df.to_numpy().T

        dff = (F - F0) / F0


        return dff, F0

    @staticmethod
    def extract_trial_dff(dff, trials_df, trial_length=31, pre_frames=10,
                          post_frames=10):

        dff = np.asarray(dff)

        trial_data = []
        extracted_indices = []

        total_frames = pre_frames + trial_length + post_frames

        for idx, trial in trials_df.iterrows():

            tone_onset = int(trial["tone_onset_index"])

            start = tone_onset - pre_frames

            end = start + total_frames

            if start < 0 or end > dff.shape[1]:
                continue

            trial_dff = dff[:, start:end]

            # Sanity check
            if trial_dff.shape[1] != total_frames:
                continue

            trial_data.append(trial_dff)
            extracted_indices.append(idx)

        dff_trials = np.stack(trial_data, axis=0)

        extracted_trials = trials_df.loc[extracted_indices].copy()
        extracted_trials = extracted_trials.reset_index(drop=True)

        relative_frames = np.arange(
            -pre_frames,
            trial_length + post_frames
        )

        return dff_trials, extracted_trials, relative_frames
