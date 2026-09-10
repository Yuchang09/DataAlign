class DataConfig:
    MiceID = "m6d2"
    dffPath = rf"C:\Users\HoLab4\Yuchang\DataAlign\files\{MiceID}\{MiceID}_dff.csv"
    TrailsPath = rf"C:\Users\HoLab4\Yuchang\DataAlign\files\{MiceID}\{MiceID}_trails.csv"

    if MiceID == "m6d1":
        FilePath = r"C:\imageripping\m6d1\20260124_timeseries_m6_d1_900_las500p900_29.3fps_1x_int187_tonepuff-223\20260124_timeseries_m6_d1_900_las500p900_29.3fps_1x_int187_tonepuff-223_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "m6d2":
        FilePath = r"C:\imageripping\m6d2\20260127_timeseries_m6_d2_930_las351p900_29.3fps_1x_int92_tonepuff-244\20260127_timeseries_m6_d2_930_las351p900_29.3fps_1x_int92_tonepuff-244_Cycle00001_VoltageRecording_001.csv"
        Suite2pPath = r"C:\imageripping\m6d2\tifm6d2\suite2p\plane0\Fall.mat"
    elif MiceID == "m6d3":
        FilePath = r"C:\imageripping\m6d3\20260128_timeseries_m6_d3_930_las321p900_29.3fps_1x_int86_tonepuff-245\20260128_timeseries_m6_d3_930_las321p900_29.3fps_1x_int86_tonepuff-245_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "m4d3":
        FilePath = r"C:\imageripping\m4d3\20260125_timeseries_m4_d3_930_las300p900_29.3fps_1x_int220_tonepuff_rest3-241\20260125_timeseries_m4_d3_930_las300p900_29.3fps_1x_int220_tonepuff_rest3-241_Cycle00001_VoltageRecording_001.csv"
    elif MiceID == "home":
        FilePath = r"/Users/yuchang/Downloads/m6d2_filtered_reindexed.csv"
        Suite2pPath = r"/Users/yuchang/Downloads/Fall.mat"
