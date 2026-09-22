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
            vlines=None,
            vline_color="red",
            vline_style="--",
            vline_alpha=0.7,
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
            if y_values.ndim == 1:
                y_values = [y_values]
            elif y_values.ndim == 2:
                y_values = y_values
            else:
                raise ValueError("y_values must be a 1D or 2D array.")

        # Generate x-values if none provided
        if x_values is None:
            x_values = range(len(y_values[0]))

        # Plot each y-value list
        for i, y in enumerate(y_values):
            if labels is not None:
                plt.plot(x_values, y, label=labels[i])
            else:
                plt.plot(x_values, y)

        # Add vertical lines
        if vlines is not None:
            for x in vlines:
                plt.axvline(
                    x=x,
                    color=vline_color,
                    linestyle=vline_style,
                    alpha=vline_alpha
                )

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

    @staticmethod
    def draw_heatmap(
        dff,
        relative_frames=None,
        sorted=True,
        event_markers=None,
        title=None,
        x_label="Frames relative to tone onset",
        y_label=None,
        colorbar_label="Mean dF/F",
        figsize=(10, 8),
        save_path=None,
        show=True
    ):

        if sorted:
            peak_frames = np.nanargmax(dff, axis=1)
            sort_idx = np.argsort(peak_frames)
            plot_dff = dff[sort_idx]
            default_y_label = "Neuron (sorted by peak)"
        else:
            plot_dff = dff
            default_y_label = "Trail"

        if y_label is None:
            y_label = default_y_label

        fig, ax = plt.subplots(figsize=figsize)

        if relative_frames is not None:
            extent = (relative_frames[0], relative_frames[-1], plot_dff.shape[0], 0)
            im = ax.imshow(plot_dff, aspect="auto", extent=extent)
        else:
            im = ax.imshow(plot_dff, aspect="auto", origin="upper"
            )
        if event_markers is not None:
            for frame, event_name in event_markers.items():
                ax.axvline(
                    frame,
                    linestyle="--",
                    color="red",
                    label=event_name
                )

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if title is not None:
            ax.set_title(title)

        fig.colorbar(im, ax=ax, label=colorbar_label)

        if event_markers:
            ax.legend()

        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300)

        if show:
            plt.show()

        plt.close(fig)
