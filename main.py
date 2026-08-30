from utils.file_utils import FileUtils
from utils.config_utils import DataConfig
from utils.data_utils import DataUtils
from utils.analysis_util import AnalysisUtil

def main():
    data = FileUtils.read_excel_file(DataConfig.FilePath)

    neuro_data = DataUtils.filter_rows_by_threshold(data, "NeuralVoltage", 5, "==")

    tone_onset = AnalysisUtil.find_event(neuro_data, "ToneVoltage", "Time", 5)
    tone_offset = AnalysisUtil.find_event(neuro_data, "ToneVoltage", "Time", 5, False)

    puff_onset = AnalysisUtil.find_event(neuro_data, "PuffVoltage", "Time", 5)
    puff_offset = AnalysisUtil.find_event(neuro_data, "PuffVoltage", "Time", 3, False)

    print(tone_onset)
    print(tone_offset)
    print(puff_onset)
    print(puff_offset)

if __name__ == '__main__':
    main()
