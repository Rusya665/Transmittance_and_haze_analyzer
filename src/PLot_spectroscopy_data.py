import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

from src.Control_panel import ControlPanel


class TransmittanceAndHazePlotter:
    """
    A class to plot transmittance and haze data using matplotlib.

    :param parent: Parental class containing all necessary sorted and prepared data to plot.
    :param plot_type: Which spectroscopy data to plot (transmittance or haze).
    """

    def __init__(self, parent, plot_type: str):
        """ Initialize the TransmittanceAndHazePlotter with data and a file name. """
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.size'] = 16
        rcParams['axes.linewidth'] = 1.1
        rcParams['axes.labelpad'] = 10.0
        rcParams['axes.xmargin'] = 0
        rcParams['axes.ymargin'] = 0
        rcParams.update({"figure.figsize": (6.4, 4.8),
                         "figure.subplot.left": 0.177, "figure.subplot.right": 0.946,
                         "figure.subplot.bottom": 0.156, "figure.subplot.top": 0.965,
                         "axes.autolimit_mode": "round_numbers",
                         "xtick.major.size": 7,
                         "xtick.minor.size": 3.5,
                         "xtick.major.width": 1.1,
                         "xtick.minor.width": 1.1,
                         "xtick.major.pad": 5,
                         "xtick.minor.visible": True,
                         "ytick.major.size": 7,
                         "ytick.minor.size": 3.5,
                         "ytick.major.width": 1.1,
                         "ytick.minor.width": 1.1,
                         "ytick.major.pad": 5,
                         "ytick.minor.visible": True,
                         "lines.markersize": 10,
                         "lines.markerfacecolor": "none",
                         "lines.markeredgewidth": 0.8})
        self.legend = None
        self.parent = parent
        self.plot_type = plot_type
        self.window_name = self.parent.root_folder_name
        self.data = self.parent.data_folders
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title(f"{self.window_name} {self.plot_type}")
        self.lines = {}
        self.additional_lines = []
        self._plot_initial_data()
        self.original_x_lim = self.ax.get_xlim()
        self.original_y_lim = self.ax.get_ylim()
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n=2))
        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(n=2))
        plt.show(block=False)
        self.control_panel = ControlPanel(self, self.window_name, self.plot_type)

    def _plot_initial_data(self) -> None:
        """ Plot the initial data based on plot_type. """
        avg, std_dev, y_label = None, None, ''
        for sample_name, metrics in self.data.items():
            wavelengths = metrics['Wavelength']
            if self.plot_type == "Transmittance":
                avg = metrics['Transmittance_Avg']
                std_dev = metrics['Transmittance_Std_Dev']
                y_label = 'Transmittance (%)'
            elif self.plot_type == "Haze":
                avg = metrics['Haze_Avg']
                std_dev = metrics['Haze_Std_Dev']
                y_label = 'Haze (%)'

            line, = self.ax.plot(wavelengths, avg, lw=1, label=sample_name)
            self.lines[sample_name] = line
            self.ax.fill_between(wavelengths, avg - std_dev, avg + std_dev, alpha=0.1)

        self.ax.set_xlabel('Wavelength (nm)')
        self.ax.set_ylabel(y_label)
        self.ax.legend()
        self.legend = self.ax.legend()

    def reset_view(self) -> None:
        """ Reset the plot view to the initial x and y-axis limits. """
        self.ax.set_xlim(self.original_x_lim)
        self.ax.set_ylim(self.original_y_lim)
        self.fig.canvas.draw_idle()

    def update_legend(self) -> None:
        """ Update the plot legend to only show visible data lines. """
        visible_lines = [line for line in self.lines.values() if line.get_visible()]
        labels = [label for label, line in self.lines.items() if line.get_visible()]
        self.legend.remove()  # Remove the old legend
        self.legend = self.ax.legend(visible_lines, labels)  # Create a new legend with the visible lines and labels

    def toggle_visibility(self, sample_name: str) -> None:
        """
        Toggle the visibility of a data line in the plot.

        :param sample_name: The name of the sample associated with the line to toggle.
        """
        line = self.lines[sample_name]
        line.set_visible(not line.get_visible())
        self.update_legend()
        self.fig.canvas.draw_idle()

    def show_all(self) -> None:
        """ Set all data lines to visible in the plot. """
        for line in self.lines.values():
            line.set_visible(True)
        self.update_legend()
        self.fig.canvas.draw_idle()
        for chk in self.control_panel.checkboxes:
            chk.select()

    def hide_all(self) -> None:
        """ Set all data lines to hidden in the plot. """
        for line in self.lines.values():
            line.set_visible(False)
        self.update_legend()
        self.fig.canvas.draw_idle()
        for chk in self.control_panel.checkboxes:
            chk.deselect()

    def zoom_to_x(self, x_min: float, x_max: float) -> None:
        """
        Zoom into a specified range on the x-axis.

        :param x_min: The minimum x-axis value to zoom to.
        :param x_max: The maximum x-axis value to zoom to.
        """
        self.ax.set_xlim(x_min, x_max)
        self.fig.canvas.draw_idle()

    def zoom_to_y(self, y_min: float, y_max: float) -> None:
        """
        Zoom into a specified range on the y-axis.

        :param y_min: The minimum y-axis value to zoom to.
        :param y_max: The maximum y-axis value to zoom to.
        """
        self.ax.set_ylim(y_min, y_max)
        self.fig.canvas.draw_idle()

    def draw_horizontal_line(self, y_value: float, **kwargs) -> None:
        """
        Draw a horizontal line at the specified y-value.

        :param y_value: The y-axis value at which to draw the horizontal line.
        """
        h_line = self.ax.axhline(y=y_value, **kwargs)
        self.additional_lines.append(h_line)
        self.fig.canvas.draw_idle()

    def draw_vertical_line(self, x_value: float, **kwargs) -> None:
        """
        Draw a vertical line at the specified x-value.

        :param x_value: The x-axis value at which to draw the vertical line.
        """
        v_line = self.ax.axvline(x=x_value, **kwargs)
        self.additional_lines.append(v_line)
        self.fig.canvas.draw_idle()

    def remove_additional_lines(self) -> None:
        """ Remove all additional lines (horizontal or vertical) from the plot. """
        while self.additional_lines:
            line = self.additional_lines.pop()
            line.remove()
        self.fig.canvas.draw_idle()
