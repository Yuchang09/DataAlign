import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class PlotUtils:

    @staticmethod
    def draw_line_plot(
            y_values,
            x_values=None,
            x_label="Samples",
            y_label="Value",
            labels=None,
            title=None,
            x_start=None,
            x_stop=None,
            save_path=None,
            figsize=(12, 5),
            show=True
    ):
        plt.figure(figsize=figsize)

        # Single Series
        if isinstance(y_values, pd.Series):
            y_values = [y_values]

        # Single numpy array
        elif isinstance(y_values, np.ndarray):
            y_values = [y_values]

        # Generate x-values if none provided
        if x_values is None:
            x_values = range(len(y_values[0]))

        # Plot each y-value list
        for i, y in enumerate(y_values):
            if labels is not None:
                plt.plot(x_values, y, label=labels[i])
            else:
                plt.plot(x_values, y)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Set x-axis limits
        if x_start is not None or x_stop is not None:
            plt.xlim(x_start, x_stop)

        if labels is not None:
            plt.legend()

        if title is not None:
            plt.title(title)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)

        if show:
            plt.show()

        plt.close()

    @staticmethod
    def draw_histogram(
            x_values,
            x_label="Value",
            y_label="Frequency",
            title=None,
            bins=30,
            save_path=None,
            figsize=(6, 5),
            show=True
    ):
        plt.figure(figsize=figsize)

        plt.hist(x_values.dropna(), bins=bins)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        if title is not None:
            plt.title(title)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)

        if show:
            plt.show()

        plt.close()
