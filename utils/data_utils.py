import pandas as pd
from utils.msg_utils import Msg

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

        # Compare the original index to the previous index
        consecutive = df.index.to_series().diff() == 1

        # Keep the first row and rows that are NOT consecutive
        return df[~consecutive]