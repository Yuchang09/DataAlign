from utils.file_utils import FileUtils
from utils.config_utils import DataConfig
from utils.data_utils import DataUtils
from utils.analysis_util import AnalysisUtil
from utils.plot_utils import PlotUtils
from utils.path_utils import PathUtils

def main():

    data = FileUtils.read_csv_file(DataConfig.FilePath)
    filtered_voltage_data = DataUtils.filter_rows_by_threshold(data, " Frame begin", 5, ">=")
    filtered_voltage_data = DataUtils.keep_first_consecutive_row(filtered_voltage_data)

    mouse_id = PathUtils.extract_mouse_id(DataConfig.FilePath)
    mouse_plot_dir = PathUtils.make_mouse_plot_dir(mouse_id)

    PlotUtils.draw_line_plot(
        filtered_voltage_data.iloc[:, -2],
        x_values=filtered_voltage_data.iloc[:, 0],
        x_label="Time(ms)",
        y_label=filtered_voltage_data.columns[-2],
        title="Voltage over time",
        save_path=PathUtils.join_path(mouse_plot_dir, f"{mouse_id}_{filtered_voltage_data.columns[-2]}.png")
    )
    PlotUtils.draw_line_plot(
        filtered_voltage_data.iloc[:, -1],
        x_values=filtered_voltage_data.iloc[:, 0],
        x_label="Time(ms)",
        y_label=filtered_voltage_data.columns[-1],
        title="Voltage over time",
        save_path = PathUtils.join_path(mouse_plot_dir, f"{mouse_id}_{filtered_voltage_data.columns[-1]}.png")
    )

    PlotUtils.draw_line_plot(
        y_values=[
            filtered_voltage_data.iloc[:, -2],
            filtered_voltage_data.iloc[:, -1]
        ],
        x_values=filtered_voltage_data.iloc[:, 0],
        x_label="Time(ms)",
        y_label="Voltage",
        labels=["Tone", "Puff"],
        title="Voltage over time",
        x_start=100000,
        x_stop=200000,
        save_path=PathUtils.join_path(mouse_plot_dir, f"{mouse_id}_TonePuff_overlay.png")
    )

    filtered_voltage_data = DataUtils.reset_row_numbers(filtered_voltage_data, drop = True)

    tone_peaks, tone_peaks_time = AnalysisUtil.find_event(filtered_voltage_data, " tone",
                                                          "Time(ms)", values = True)
    puff_peaks, puff_peaks_time = AnalysisUtil.find_event(filtered_voltage_data, " puff",
                                                          "Time(ms)", values = True)

    mouse_file_dir = PathUtils.make_mouse_file_dir(mouse_id)
    filtered_data_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_filtered_reindexed.csv")
    FileUtils.write_csv_file(filtered_data_path, filtered_voltage_data)

    tone_peaks_time = DataUtils.reset_row_numbers(tone_peaks_time, drop=False)
    tone_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_{filtered_voltage_data.columns[-2]}.csv")
    FileUtils.write_csv_file(tone_path, tone_peaks_time)

    puff_peaks_time = DataUtils.reset_row_numbers(puff_peaks_time, drop=False)
    puff_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_{filtered_voltage_data.columns[-1]}.csv")
    FileUtils.write_csv_file(puff_path, puff_peaks_time)

    time_difference = AnalysisUtil.calculate_puff_tone_difference(tone_peaks_time.iloc[:, -1], puff_peaks_time.iloc[:, -1])
    diff_path = PathUtils.join_path(mouse_file_dir, f"{mouse_id}_time_diff.csv")
    FileUtils.write_csv_file(diff_path, time_difference)

    PlotUtils.draw_histogram(
        time_difference["difference"],
        x_label="Puff - Previous Tone (ms)",
        title="Time Between Tone and Puff",
        bins = 5,
        save_path=PathUtils.join_path(
            mouse_plot_dir,
            f"{mouse_id}_TonePuff_Difference.png"
        )
    )


if __name__ == '__main__':
    main()
