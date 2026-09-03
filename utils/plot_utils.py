import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

class PlotUtils:

    @staticmethod
    def draw_line_plot(y_values, x_values=None, x_label="Sample", y_label="Value",
            title=None, save_path=None, figsize=(12, 5), show=True):
        plt.figure(figsize=figsize)

        if x_values is None:
            x_values = range(len(y_values))

        plt.plot(x_values, y_values)

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
