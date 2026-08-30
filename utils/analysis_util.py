import pandas as pd

class AnalysisUtil:

    @staticmethod
    def find_event(df, signal_column, time_column, threshold, onset = True):

        signal = df[signal_column]

        above_threshold = signal >= threshold

        if onset:
            event = above_threshold & ~above_threshold.shift(fill_value=False)
        else:
            event = above_threshold & ~above_threshold.shift( -1, fill_value=False )

        return df.loc[event, time_column]