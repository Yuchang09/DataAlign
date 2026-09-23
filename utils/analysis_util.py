import pandas as pd
from utils.msg_utils import Msg
import numpy as np
from utils.data_utils import DataUtils
from utils.config_utils import DataConfig
from utils.plot_utils import PlotUtils
from utils.path_utils import PathUtils

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
                Msg.print_error(f"Signal column index {signal_column} is out of range. "
                                f"DataFrame has {len(df.columns)} columns.")
                raise IndexError

            signal_column = df.columns[signal_column]

        elif isinstance(signal_column, str):
            if signal_column not in df.columns:
                Msg.print_error(f"Signal column '{signal_column}' does not exist. "
                                f"Available columns: {list(df.columns)}")
                raise KeyError

        else:
            Msg.print_error("signal_column must be either a column name (str) or column index (int).")
            raise TypeError

        if isinstance(time_column, int):
            if time_column < 0 or time_column >= len(df.columns):
                Msg.print_error(f"Time column index {time_column} is out of range. "
                                f"DataFrame has {len(df.columns)} columns.")
                raise IndexError

            time_column = df.columns[time_column]

        elif isinstance(time_column, str):
            if time_column not in df.columns:
                Msg.print_error(f"Time column '{time_column}' does not exist. "f"Available columns: {list(df.columns)}")
                raise KeyError

        else:
            Msg.print_error("time_column must be either a column name (str) or column index (int).")
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
        mask = (df[start].notna() & df[end].notna() & (difference != threshold))
        df.loc[mask, end] = df.loc[mask, start] + threshold
        return df

    @staticmethod
    def build_event_dataframe(
            tone_onset,
            tone_offset,
            puff_onset,
            puff_offset
    ):
        result = pd.DataFrame({"tone_onset_index": tone_onset.index,"tone_offset_index": tone_offset.index})
        result["puff_onset_index"] = pd.NA
        result["puff_offset_index"] = pd.NA

        for puff_index, puff_time in puff_onset.items():
            previous_tones = tone_onset[tone_onset < puff_time]
            if previous_tones.empty:
                continue

            tone_index = previous_tones.index[-1]
            tone_row = result.index[result["tone_onset_index"] == tone_index][0]

            # Add puff information
            result.loc[tone_row, "puff_onset_index"] = puff_index
            previous_offsets = puff_offset[puff_offset.index > puff_index]

            if not previous_offsets.empty:
                offset_index = previous_offsets.index[0]
                result.loc[tone_row, "puff_offset_index"] = offset_index

        return result

    @staticmethod
    def add_diff(result):
        result["ISI_length"] = (result["puff_onset_index"] - result["tone_offset_index"])
        result["trail_length"] = (result["puff_offset_index"] - result["tone_onset_index"])
        result["tone_length"] = (result["tone_offset_index"] - result["tone_onset_index"])
        result["puff_length"] = (result["puff_offset_index"] - result["puff_onset_index"])
        return result

    @staticmethod
    def calculate_dff(F, frame_rate, window_seconds=30, percentile=10):

        window_frames = int(window_seconds * frame_rate)
        if window_frames < 1:
            raise ValueError("Window must contain at least one frame.")

        F = np.asarray(F, dtype=float)
        F_df = pd.DataFrame(F.T)
        F0_df = (F_df.rolling(window=window_frames, center=True, min_periods=1).quantile(percentile / 100))
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

            if trial_dff.shape[1] != total_frames:
                continue

            trial_data.append(trial_dff)
            extracted_indices.append(idx)

        dff_trials = np.stack(trial_data, axis=0)
        extracted_trials = trials_df.loc[extracted_indices].copy()
        extracted_trials = extracted_trials.reset_index(drop=True)
        relative_frames = np.arange(-pre_frames,trial_length + post_frames)

        return dff_trials, extracted_trials, relative_frames

    @staticmethod
    def get_average_activiy_per_period_across_trails(dff):
        mean_dff = DataUtils.calculate_mean(dff, axis=1)
        results = DataUtils.calculate_period_stats(mean_dff, DataConfig.StimuliMarkers)
        PlotUtils.draw_line_plot(
            y_values=[
                results["0"],
                results["1"],
                results["2"]
            ],
            labels=["Tone", "ISI", "Puff"],
            x_label="Trial",
            y_label="Mean dF/F",
            title="Mean dF/F Across Trails",
            save_path=PathUtils.join_path(DataConfig.mouse_plot_dir, f"{DataConfig.MiceID}_period_averaged_across_trail.png")
        )

    @staticmethod
    def get_heatmap(dff, axis, slice = None):
        mean_dff = DataUtils.calculate_mean(dff, axis=axis)
        if axis == 0:
            axis ="neuron"
            sort = True
        else:
            axis = "trail"
            sort = False
        if slice:
            savepath = PathUtils.join_path(DataConfig.mouse_plot_dir,
                                        f"{DataConfig.MiceID}_Heatmap_{axis}_{slice}.png")
        else:
            savepath = PathUtils.join_path(DataConfig.mouse_plot_dir,
                                            f"{DataConfig.MiceID}_Heatmap_{axis}.png")
        PlotUtils.draw_heatmap(mean_dff, sorted = sort, event_markers=DataConfig.StimuliMarkers, save_path = savepath)

    @staticmethod
    def get_per_slice_heatmap(dff):
        periods = DataUtils.slice_by_markers(dff, DataConfig.TrailMarkers, axis=0)
        for name, period in periods.items():
            AnalysisUtil.get_heatmap(period, 0, name)

    @staticmethod
    def classify_period_cells(dff, threshold = 2, stats = "mean"):
        mean_dff = DataUtils.calculate_mean(dff, axis=0)
        period_response = DataUtils.calculate_period_stats(mean_dff, DataConfig.StimuliMarkers, axis=1, stats = stats)
        baseline_dff = DataUtils.get_rest(mean_dff, DataConfig.StimuliMarkers)
        baseline_response = {k: DataUtils.calculate_mean(v, axis = 1) for k, v in baseline_dff.items()}
        baseline_std = {k: DataUtils.calculate_std(v, axis = 1) for k, v in baseline_dff.items()}

        z_scores = {}
        for period in period_response:
            z_scores[period] = DataUtils.calculate_zscore(period_response[period], baseline_response[period], baseline_std[period])

        cells = {period: z_scores[period] >= threshold for period in z_scores}
        periods = ["tone", "isi", "puff"]

        z_matrix = np.column_stack([z_scores[i] for i in z_scores])
        max_z = np.max(z_matrix, axis=1)
        max_idx = np.argmax(z_matrix, axis=1)
        identities = np.array(periods, dtype=object)[max_idx]
        identities[max_z < threshold] = "none"

        return identities, cells

    @staticmethod
    def classify_trials(dff, mode="slice", stats="max"):

        if mode == "slice":
            data_groups = DataUtils.slice_by_markers(dff, DataConfig.TrailMarkers, axis=0)

        elif mode == "trial":
            data_groups = {i: dff[i:i + 1] for i in range(dff.shape[0])}

        elif mode == "all":
            data_groups = {"all": dff}

        else:
            raise ValueError("mode must be 'session', 'trial', or 'all'")

        classification = {}
        for name, data in data_groups.items():
            identities, cells = AnalysisUtil.classify_period_cells(data,stats=stats)
            classification[name] = {"identities": identities, "cells": cells}

        return classification

    @staticmethod
    def calculate_identity_stats(classification, stat="percentage", exclude_none = False):
        names = list(classification.keys())
        cell_types = np.unique(np.concatenate([classification[name]["identities"]for name in names]))

        results = {}
        if exclude_none:
            cell_types = cell_types[cell_types != "none"]

        for cell_type in cell_types:
            results[cell_type] = []

            for name in names:
                identities = classification[name]["identities"]
                if exclude_none:
                    identities = identities[identities != "none"]

                count = np.sum(identities == cell_type)

                if stat == "count":
                    results[cell_type].append(count)

                elif stat == "percentage":
                    results[cell_type].append(count / len(identities) * 100)

                else:
                    raise ValueError("stat must be 'count' or 'percentage'")

        return names, cell_types, results

    @staticmethod
    def calculate_transition_probability(
            identities_before,
            identities_after
    ):
        cell_types = np.unique(np.concatenate([identities_before, identities_after]))
        transition = np.zeros((len(cell_types), len(cell_types)))

        for i, before_type in enumerate(cell_types):
            mask = identities_before == before_type

            for j, after_type in enumerate(cell_types):
                transition[i, j] = np.sum(identities_after[mask] == after_type)

            if np.sum(mask) > 0:
                transition[i] /= np.sum(mask)

        return cell_types, transition


