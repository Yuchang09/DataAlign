from utils.file_utils import FileUtils
from utils.config_utils import DataConfig
from utils.data_utils import DataUtils
from utils.analysis_util import AnalysisUtil
from utils.plot_utils import PlotUtils
from utils.path_utils import PathUtils


def main():
    data = FileUtils.read_npz_file(DataConfig.DffTrailPath)
    dff = data["dff"]
    trails = [0,1,2,3,4,14,24,34,44,54,62]
    tone_puff, tone_only = DataUtils.subset_trials(dff,trails)

    # AnalysisUtil.get_heatmap(tone_puff, axis = 0)


    mode = "slice"
    stat = "count"
    classification = AnalysisUtil.classify_trials(tone_puff, mode = mode)
    # names, cell_types, percentages = AnalysisUtil.calculate_identity_stats(classification, stat = stat, exclude_none=False)
    #
    # savepath = PathUtils.join_path(DataConfig.mouse_plot_dir,
    #                                f"{DataConfig.MiceID}_CellType_across_trial_{mode}_{stat}.png")
    #
    # PlotUtils.draw_line_plot(
    #     y_values=[
    #         percentages[cell_type]
    #         for cell_type in percentages
    #     ],
    #     x_values=names,
    #     x_label="Trials",
    #     y_label="Percentage of Neurons",
    #     labels=list(percentages.keys()),
    #     title="Cell Identity Across Trials",
    #     save_path=savepath
    # )
    # PlotUtils.draw_bar_plot(
    #     percentages,
    #     x_values=names,
    #     x_label="Trials",
    #     y_label="Count of Responsive Neurons",
    #     title="Cell Identity Across Trials",
    #     stacked=True,
    #     save_path=savepath,
    # )

    names = list(classification.keys())

    for before, after in zip(names[:-1], names[1:]):
        identities_before = classification[before]["identities"]
        identities_after = classification[after]["identities"]

        cell_types, transition = AnalysisUtil.calculate_transition_probability(
            identities_before,
            identities_after
        )
        savepath = PathUtils.join_path(DataConfig.mouse_plot_dir,
                                       f"{DataConfig.MiceID}_transition_{before}_{after}.png")

        PlotUtils.draw_transition_heatmap(transition, cell_types, title=f"{before} to {after}", save_path=savepath)
        print(f"{before} → {after}")
        print(transition)



if __name__ == '__main__':
    main()
