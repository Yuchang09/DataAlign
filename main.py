from utils.file_utils import FileUtils
from utils.config_utils import DataConfig
from utils.data_utils import DataUtils
from utils.analysis_util import AnalysisUtil
from utils.plot_utils import PlotUtils
from utils.path_utils import PathUtils

mouse_id = PathUtils.extract_mouse_id(DataConfig.FilePath)
mouse_plot_dir = PathUtils.make_mouse_plot_dir(mouse_id)


def main():
    data = FileUtils.read_npz_file(DataConfig.DffTrailPath)
    dff = data["dff"]
    trails = [0,1,2,3,4,14,24,34,44,54,62]
    tone_puff, tone_only = DataUtils.subset_trials(dff,trails)

    AnalysisUtil.get_average_activiy_per_period_across_trails(tone_puff)


if __name__ == '__main__':
    main()
