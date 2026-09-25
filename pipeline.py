from utils.file_utils import FileUtils
from utils.config_utils import DataConfig
from utils.data_utils import DataUtils
from utils.analysis_util import AnalysisUtil
from utils.path_utils import PathUtils
import pandas as pd

mouse_id = PathUtils.extract_mouse_id(DataConfig.FilePath)
mouse_file_dir = PathUtils.make_mouse_file_dir(mouse_id)


def filter_data():
    data = FileUtils.read_csv_file(DataConfig.FilePath)
    filtered_voltage_data = DataUtils.filter_rows_by_threshold(data, 1, 5, ">=")
    filtered_voltage_data = DataUtils.keep_first_consecutive_row(filtered_voltage_data)
    filtered_voltage_data = DataUtils.reset_row_numbers(filtered_voltage_data, drop=True)

    filtered_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_filtered_reindexed.csv")
    FileUtils.write_csv_file(filtered_data_path, filtered_voltage_data)

    tone_onset = AnalysisUtil.find_event(data, " tone", "Time(ms)", 9.9)
    tone_offset = AnalysisUtil.find_event(data, " tone", "Time(ms)", 9.9,
                                          False)
    puff_onset = AnalysisUtil.find_event(data, " puff", "Time(ms)", 3)
    puff_offset = AnalysisUtil.find_event(data, " puff", "Time(ms)", 3,
                                          False)

    tone_onset_time = DataUtils.reset_row_numbers(tone_onset, drop=False)
    tone_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_tone_onset.csv")
    FileUtils.write_csv_file(tone_path, tone_onset_time)

    tone_offset_time = DataUtils.reset_row_numbers(tone_offset, drop=False)
    tone_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_tone_offset.csv")
    FileUtils.write_csv_file(tone_path, tone_offset_time)

    puff_onset_time = DataUtils.reset_row_numbers(puff_onset, drop=False)
    puff_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_puff_onset.csv")
    FileUtils.write_csv_file(puff_path, puff_onset_time)

    puff_offset_time = DataUtils.reset_row_numbers(puff_offset, drop=False)
    puff_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_puff_offset.csv")
    FileUtils.write_csv_file(puff_path, puff_offset_time)


    tone_onset = AnalysisUtil.find_event(filtered_voltage_data, " tone", "Time(ms)", 9.9)
    tone_offset = AnalysisUtil.find_event(filtered_voltage_data, " tone", "Time(ms)", 9.9,
                                          False)
    puff_onset = AnalysisUtil.find_event(filtered_voltage_data, " puff", "Time(ms)", 3)
    puff_offset = AnalysisUtil.find_event(filtered_voltage_data, " puff", "Time(ms)", 3,
                                          False)

    trails_df = AnalysisUtil.build_event_dataframe(tone_onset, tone_offset, puff_onset, puff_offset)

    trails_df = AnalysisUtil.limit_difference(trails_df, start="tone_onset_index", end="puff_offset_index",threshold=31)
    trails_df = AnalysisUtil.limit_difference(trails_df, start="tone_onset_index", end="tone_offset_index",threshold=9)
    trails_df = AnalysisUtil.limit_difference(trails_df, start="tone_offset_index", end="puff_onset_index", threshold=16)
    trails_df = AnalysisUtil.add_diff(trails_df)
    trail_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_trails.csv")
    FileUtils.write_csv_file(trail_path, trails_df)

def get_standardized_data():
    suite2p_data = FileUtils.read_mat_file(DataConfig.Suite2pPath)
    F = suite2p_data['F']
    iscell = suite2p_data['iscell']
    iscell_df = pd.DataFrame(iscell)
    filtered_iscell = DataUtils.filter_rows_by_threshold(iscell_df, column=0, threshold=1, operator="==")
    F_subset = F[filtered_iscell.index]
    dff, f0 = AnalysisUtil.calculate_dff(F_subset, 30, window_seconds=30, percentile=10)
    z_score = (F_subset - f0) / DataUtils.calculate_std(F_subset)
    dff_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_dff.csv")
    f0_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_f0.csv")
    f_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_f_data.csv")
    z_score_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_z_score.csv")

    FileUtils.write_csv_file(dff_data_path, dff)
    FileUtils.write_csv_file(f0_data_path, f0)
    FileUtils.write_csv_file(f_data_path, F_subset)
    FileUtils.write_csv_file(z_score_data_path, z_score)

def get_trail_data(data_type):
    if data_type == "z_score":
        data = FileUtils.read_csv_file(DataConfig.z_scorePath)
        data_trails_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_z_score_trails.npz")
    elif data_type == "dff":
        data = FileUtils.read_csv_file(DataConfig.dffPath)
        data_trails_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_dff_trails.npz")

    trials_df = FileUtils.read_csv_file(DataConfig.TrailsPath)
    data_trials, extracted_trials, relative_frames = AnalysisUtil.extract_trial_data(
        data, trials_df, trial_length=31, pre_frames=10, post_frames=10)
    FileUtils.write_npz_file(data_trails_path, data=data_trials, relative_frames=relative_frames)


def main():
    filter_data()
    get_standardized_data()
    get_trail_data(DataConfig.DataType)

if __name__ == "__main__":
    main()