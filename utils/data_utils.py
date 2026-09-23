from utils.msg_utils import Msg
import numpy as np
import pandas as pd

class DataUtils:

    @staticmethod
    def filter_rows_by_threshold(df, column, threshold, operator = ">"):

        if isinstance(column, int):
            if column < 0 or column >= len(df.columns):
                Msg.print_error(f"Column index {column} is out of range. DataFrame has {len(df.columns)} columns.")
                raise IndexError

            column = df.columns[column]

        elif isinstance(column, str):
            if column not in df.columns:
                Msg.print_error( f"Column '{column}' does not exist. Available columns: {list(df.columns)}" )
                raise KeyError

        else:
            Msg.print_error( "column must be either a column name (str) or column index (int)." )
            raise TypeError


        if operator == ">":
            mask = df[column] > threshold
        elif operator == ">=":
            mask = df[column] >= threshold
        elif operator == "<":
            mask = df[column] < threshold
        elif operator == "<=":
            mask = df[column] <= threshold
        elif operator == "==":
            mask = df[column] == threshold
        elif operator == "!=":
            mask = df[column] != threshold

        return df[mask]

    @staticmethod
    def reset_row_numbers(df, drop = False):
        if drop:
            return df.reset_index(drop=True)

        return df.reset_index()

    @staticmethod
    def keep_first_consecutive_row(df):

        if df.empty:
            return df

        consecutive = df.index.to_series().diff() == 1

        return df[~consecutive]

    @staticmethod
    def calculate_mean(data, axis=0):
        return np.nanmean(data, axis=axis)

    @staticmethod
    def calculate_max(data, axis=0):
        return np.nanmax(data, axis=axis)

    @staticmethod
    def calculate_std(data, axis=0):
        return np.nanstd(data, axis=axis)

    @staticmethod
    def calculate_zscore(data, mean, std):
        return (data - mean) / std

    @staticmethod
    def calculate_period_stats(data, event_markers, axis=1, stats = "mean"):
        data = np.asarray(data)

        markers = sorted(event_markers.items())
        results = {}

        for i in range(len(markers) - 1):
            start_frame, start_name = markers[i]
            end_frame, end_name = markers[i + 1]

            if axis == 1:
                period_data = data[:, start_frame:end_frame]
            elif axis == 0:
                period_data = data[start_frame:end_frame, :]
            else:
                raise ValueError("axis must be 0 or 1")

            if stats == "mean":
                results[i] = DataUtils.calculate_mean(period_data, axis=axis)
            elif stats == "max":
                results[i] = DataUtils.calculate_max(period_data, axis=axis)

        return pd.DataFrame(results)

    @staticmethod
    def slice_by_markers(data, event_markers, axis=-1):
        data = np.asarray(data)
        markers = sorted(event_markers.items())
        boundaries = [(0, "Start")] + markers
        results = {}

        for i in range(len(boundaries) - 1):
            start, _ = boundaries[i]
            end, period_name = boundaries[i + 1]

            slices = [slice(None)] * data.ndim
            slices[axis] = slice(start, end)
            results[period_name] = data[tuple(slices)]

        return results

    @staticmethod
    def subset_trials(dff, trials):
        dff = np.asarray(dff)
        tone_only = dff[trials]

        # Get the remaining trial indices
        all_trials = np.arange(dff.shape[0])
        remaining_trials = np.setdiff1d(all_trials, trials)

        # Select the remaining trials
        tone_puff = dff[remaining_trials]

        return tone_puff, tone_only

    @staticmethod
    def get_rest(dff, event_markers):
        frames = sorted(event_markers.keys())
        n_frames = dff.shape[1]

        boundaries = frames + [n_frames]

        results = {}

        for i in range(len(boundaries) - 2):
            start = boundaries[i]
            end = boundaries[i + 1]
            rest_data = np.concatenate([dff[:, :start], dff[:, end:]], axis=1)
            results[i] = dff

        return results
