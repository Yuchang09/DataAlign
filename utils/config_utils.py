from utils.path_utils import PathUtils


class DataConfig:
    MiceID = "m3d1"
    dffPath = rf"files/{MiceID}/{MiceID}_dff.csv"
    TrailsPath = rf"files/{MiceID}/{MiceID}_trails.csv"
    DffTrailPath = rf"files/{MiceID}/{MiceID}_dff_trails.npz"
    mouse_plot_dir = PathUtils.make_mouse_plot_dir(MiceID)

    if MiceID == "m6d1":
        FilePath = r"C:\imageripping\m6d1\20260124_timeseries_m6_d1_900_las500p900_29.3fps_1x_int187_tonepuff-223\20260124_timeseries_m6_d1_900_las500p900_29.3fps_1x_int187_tonepuff-223_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "m6d2":
        FilePath = r"C:\imageripping\m6d2\20260127_timeseries_m6_d2_930_las351p900_29.3fps_1x_int92_tonepuff-244\20260127_timeseries_m6_d2_930_las351p900_29.3fps_1x_int92_tonepuff-244_Cycle00001_VoltageRecording_001.csv"
        Suite2pPath = r"C:\imageripping\m6d2\tifm6d2\suite2p\plane0\Fall.mat"
    elif MiceID == "m6d3":
        FilePath = r"C:\imageripping\m6d3\20260128_timeseries_m6_d3_930_las321p900_29.3fps_1x_int86_tonepuff-245\20260128_timeseries_m6_d3_930_las321p900_29.3fps_1x_int86_tonepuff-245_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "m4d3":
        FilePath = r"C:\imageripping\m4d3\20260125_timeseries_m4_d3_930_las300p900_29.3fps_1x_int220_tonepuff_rest3-241\20260125_timeseries_m4_d3_930_las300p900_29.3fps_1x_int220_tonepuff_rest3-241_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "m3d1":
        FilePath = r"/Users/yuchang/Downloads/m3d1/voltage.csv"
        Suite2pPath = r"/Users/yuchang/Downloads/m3d1/Fall.mat"

    StimuliMarkers = {
            10: "tone onset",
            19: "tone offset",
            35: "puff onset",
            41: "puff offset"
    }

    TrailMarkers = {
            18: "Early",
            36: "Middle",
            54: "Late"
    }
