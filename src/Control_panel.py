import tkinter as tk
from functools import partial
from tkinter import colorchooser
from typing import List, Tuple

import customtkinter as ctk
import webcolors
from matplotlib.lines import Line2D


class ControlPanel(ctk.CTkToplevel):
    """
    A Control Panel class that provides an interface for manipulating the TransmittancePlotter plot.

    :param plotter: An instance of the TransmittancePlotter class to control.
    :param file_name: The name of the file being analyzed.
    :param plot_type: Which spectroscopy data to plot (transmittance or haze).
    """

    def __init__(self, plotter, file_name: str, plot_type: str):
        super().__init__()
        self.file_name = file_name
        self.plotter = plotter
        self.title(f"{self.file_name} {plot_type} Data Control Panel")
        self.geometry("1090x750")
        self.main_scrollable_frame = ctk.CTkScrollableFrame(self, width=1090, height=750, orientation="horizontal")
        self.main_scrollable_frame.pack()
        self.checkboxes: List[ctk.CTkCheckBox] = []
        self.color_buttons: List[Tuple[ctk.CTkButton, str]] = []

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_scrollable_frame, width=500, height=580)
        self.scrollable_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        for sample_name, line in self.plotter.lines.items():
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.pack(fill='x', padx=5, pady=2)

            chk = ctk.CTkCheckBox(row_frame, text=sample_name,
                                  command=lambda name=sample_name: self.plotter.toggle_visibility(name))
            chk.select()

            self.checkboxes.append(chk)
            hex_color = line.get_color()

            line_styles = ['-', '--', '-.', ':', '']
            line_style_menu = ctk.CTkOptionMenu(row_frame,
                                                values=line_styles, width=55,
                                                command=partial(self.update_line_style, line))
            color_button = ctk.CTkButton(row_frame, fg_color=hex_color, text=f'{self.get_color_name(hex_color)}',
                                         command=lambda name=sample_name: self.change_line_color(name))

            self.color_buttons.append((color_button, sample_name))

            line_width_entry = ctk.CTkEntry(row_frame, placeholder_text='Insert line width', width=50)
            line_width_entry.insert(tk.END, '1')
            line_width_entry.bind('<KeyRelease>', partial(self.line_width_change, line=line))

            chk.pack(side=tk.LEFT, padx=5)
            line_style_menu.pack(side=tk.RIGHT, padx=5)
            line_width_entry.pack(side=tk.RIGHT, padx=5)
            color_button.pack(side=tk.RIGHT, padx=5)

        self.control_frame = ctk.CTkScrollableFrame(self.main_scrollable_frame, width=500)
        self.control_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        self.show_hide_frame = ctk.CTkFrame(self.main_scrollable_frame)
        self.show_hide_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.show_all_button = ctk.CTkButton(self.show_hide_frame, text="Show All", command=self.plotter.show_all)
        self.show_all_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5))

        self.hide_all_button = ctk.CTkButton(self.show_hide_frame, text="Hide All", command=self.plotter.hide_all)
        self.hide_all_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10))

        # Entry for zooming to x
        self.x_zoom_frame = ctk.CTkFrame(self.control_frame)
        self.x_zoom_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.x_zoom_label = ctk.CTkLabel(self.x_zoom_frame, text="Zoom to X:")
        self.x_zoom_label.pack(side=tk.LEFT)

        self.x_zoom_entry_min = ctk.CTkEntry(self.x_zoom_frame, placeholder_text="X min")
        self.x_zoom_entry_min.pack(side=tk.LEFT)

        self.x_zoom_entry_max = ctk.CTkEntry(self.x_zoom_frame, placeholder_text="X max")
        self.x_zoom_entry_max.pack(side=tk.LEFT)

        self.x_zoom_button = ctk.CTkButton(self.x_zoom_frame, text="Zoom", command=self.zoom_x)
        self.x_zoom_button.pack(side=tk.LEFT)

        # Add widgets for y-zooming in the control frame
        self.y_zoom_frame = ctk.CTkFrame(self.control_frame)
        self.y_zoom_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.y_zoom_label = ctk.CTkLabel(self.y_zoom_frame, text="Zoom to Y:")
        self.y_zoom_label.pack(side=tk.LEFT)

        self.y_zoom_entry_min = ctk.CTkEntry(self.y_zoom_frame, placeholder_text="Y min")
        self.y_zoom_entry_min.pack(side=tk.LEFT)

        self.y_zoom_entry_max = ctk.CTkEntry(self.y_zoom_frame, placeholder_text="Y max")
        self.y_zoom_entry_max.pack(side=tk.LEFT)

        self.y_zoom_button = ctk.CTkButton(self.y_zoom_frame, text="Zoom", command=self.zoom_y)
        self.y_zoom_button.pack(side=tk.LEFT)

        # Add a Reset View button
        self.reset_view_button = ctk.CTkButton(self.control_frame, text="Reset View", command=self.plotter.reset_view)
        self.reset_view_button.grid(row=2, column=0, pady=10, padx=10)

        # Entry for drawing a horizontal line
        self.h_line_frame = ctk.CTkFrame(self.control_frame)
        self.h_line_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.h_line_label = ctk.CTkLabel(self.h_line_frame, text="Draw H-Line at Y:")
        self.h_line_label.pack(side=tk.LEFT)

        self.h_line_entry = ctk.CTkEntry(self.h_line_frame, placeholder_text="Y value")
        self.h_line_entry.pack(side=tk.LEFT, padx=(4, 0))

        self.h_line_button = ctk.CTkButton(self.h_line_frame, text="Draw", command=self.draw_h_line)
        self.h_line_button.pack(side=tk.LEFT, padx=(4, 0))

        # Add widgets for drawing a vertical line in the control frame
        self.v_line_frame = ctk.CTkFrame(self.control_frame)
        self.v_line_frame.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        self.v_line_label = ctk.CTkLabel(self.v_line_frame, text="Draw V-Line at X:")
        self.v_line_label.pack(side=tk.LEFT)

        self.v_line_entry = ctk.CTkEntry(self.v_line_frame, placeholder_text="X value")
        self.v_line_entry.pack(side=tk.LEFT, padx=(4, 0))

        self.v_line_button = ctk.CTkButton(self.v_line_frame, text="Draw", command=self.draw_v_line)
        self.v_line_button.pack(side=tk.LEFT, padx=(4, 0))

        # Add widgets for calculating band gap
        self.band_gap_frame = ctk.CTkFrame(self.control_frame)
        self.band_gap_frame.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

        self.band_gap_label = ctk.CTkLabel(self.band_gap_frame, text="Band Gap (eV):")
        self.band_gap_label.pack(side=tk.LEFT)

        self.band_gap_entry = ctk.CTkEntry(self.band_gap_frame, placeholder_text="Enter band gap")
        self.band_gap_entry.pack(side=tk.LEFT, padx=(17, 0))

        self.band_gap_button = ctk.CTkButton(self.band_gap_frame, text="Plot Band Gap", command=self.plot_band_gap)
        self.band_gap_button.pack(side=tk.LEFT, padx=(4, 0))

        self.band_gap_zoom = ctk.CTkEntry(self.band_gap_frame, placeholder_text="2", width=90)
        self.band_gap_zoom.insert(tk.END, 2)
        self.band_gap_zoom.pack(side=tk.LEFT, padx=(4, 0))
        # Button to remove all lines
        self.remove_lines_button = ctk.CTkButton(self.control_frame, text="Remove all lines",
                                                 command=self.plotter.remove_additional_lines)
        self.remove_lines_button.grid(row=6, column=0, pady=10, padx=10)

        # Work around markers
        self.markers_frame = ctk.CTkFrame(self.control_frame)
        self.markers_frame.grid(row=7, column=0, pady=10, padx=10)
        self.marker_label = ctk.CTkLabel(self.markers_frame, text='Choose markers type and size')
        self.marker_label.pack(side=tk.TOP)
        self.marker_style_var = tk.StringVar(value="None")
        self.marker_styles = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4",
                              "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_",
                              "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "none"]

        self.marker_style_menu = ctk.CTkOptionMenu(self.markers_frame, variable=self.marker_style_var,
                                                   values=self.marker_styles, command=self.set_markers)
        self.marker_style_menu.set('none')
        self.marker_style_menu.pack(side=tk.LEFT)

        self.marker_size_entry = ctk.CTkEntry(self.markers_frame, placeholder_text="Marker size")
        self.marker_size_entry.bind('<KeyRelease>', lambda event: self.set_markers())
        self.marker_size_entry.pack(side=tk.LEFT)

        # Add widgets for legend visibility
        self.legend_frame = ctk.CTkFrame(self.control_frame)
        self.legend_frame.grid(row=8, column=0, pady=10, padx=10)
        self.legend_frame_label = ctk.CTkLabel(self.legend_frame, text='Set legend visibility and position')
        self.legend_frame_label.pack(side=tk.TOP)
        self.legend_visibility_var = tk.BooleanVar(value=True)
        self.legend_visibility_checkbox = ctk.CTkCheckBox(
            self.legend_frame,
            text="Show Legend",
            variable=self.legend_visibility_var,
            command=self.toggle_legend_visibility
        )
        self.legend_visibility_checkbox.pack(side=tk.LEFT)

        # Add widgets for legend position
        self.legend_position_var = tk.StringVar(value="best")
        self.legend_position_options = ["best", "upper right", "upper left", "lower left", "lower right",
                                        "right", "center left", "center right", "lower center",
                                        "upper center", "center"]
        self.legend_position_menu = ctk.CTkOptionMenu(
            self.legend_frame,
            variable=self.legend_position_var,
            values=self.legend_position_options,
            command=self.change_legend_position
        )
        self.legend_position_menu.pack(side=tk.LEFT, padx=(4, 0))

    def toggle_legend_visibility(self):
        """Toggle the visibility of the legend."""
        if self.legend_visibility_var.get():
            self.plotter.legend.set_visible(True)
        else:
            self.plotter.legend.set_visible(False)
        self.plotter.fig.canvas.draw_idle()

    def change_legend_position(self, _event: str = None):
        """Change the position of the legend."""
        new_position = self.legend_position_var.get()
        self.plotter.legend.set_loc(new_position)
        self.plotter.fig.canvas.draw_idle()

    def line_width_change(self, event, line: Line2D):
        # Get the Entry widget that fired the event
        entry_widget = event.widget
        # Extract the value typed by the user into the Entry widget
        entered_value = entry_widget.get().strip()  # Using strip() to remove leading and trailing whitespace
        line.set_linewidth(entered_value)
        self.plotter.fig.canvas.draw_idle()

    def update_line_style(self, line: Line2D, style: str) -> None:
        """Update the line style in the plot based on user selection."""
        line.set_linestyle(style)
        self.plotter.fig.canvas.draw_idle()

    def change_line_color(self, sample_name: str) -> None:
        """
        Opens a color picker dialog to change the color of the line associated with the sample name.

        :param sample_name: The name of the sample whose line color is to be changed.
        """
        new_color = colorchooser.askcolor(title="Choose color")[-1]
        if new_color:
            # Set the new color to the line in the plot
            self.plotter.lines[sample_name].set_color(new_color)

            # Find and update the corresponding color button
            for button, name in self.color_buttons:
                if name == sample_name:
                    button.configure(fg_color=new_color, text=self.get_color_name(new_color))
                    break

            # Redraw the canvas to update the plot
            self.plotter.fig.canvas.draw_idle()
            self.plotter.update_legend()

    @staticmethod
    def closest_color(requested_color):
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_color_name(self, requested_color_hex):
        try:
            requested_color_rgb = webcolors.hex_to_rgb(requested_color_hex)
            closest_name = self.closest_color(requested_color_rgb)
        except ValueError:
            closest_name = "Unknown color"
        return closest_name

    def set_markers(self, _event=None) -> None:
        """Set the marker style and size in the plot based on user selection."""
        new_marker = self.marker_style_var.get() if self.marker_style_var.get() != "None" else ''
        # Try to convert the size entry to a float; if it fails, use a default size
        try:
            new_size = float(self.marker_size_entry.get())
        except ValueError:
            new_size = 5  # Default size if the entry is not a valid float
        for line in self.plotter.lines.values():
            line.set_marker(new_marker)
            line.set_markersize(new_size)
        self.plotter.fig.canvas.draw_idle()

    def zoom_x(self) -> None:
        """ Zooms in on the x-axis of the plot based on the user input in the x-axis zoom fields. """
        try:
            x_min = float(self.x_zoom_entry_min.get())
            x_max = float(self.x_zoom_entry_max.get())
            self.plotter.zoom_to_x(x_min, x_max)
        except ValueError:
            pass

    def zoom_y(self) -> None:
        """ Zooms in on the y-axis of the plot based on the user input in the y-axis zoom fields. """
        try:
            y_min = float(self.y_zoom_entry_min.get())
            y_max = float(self.y_zoom_entry_max.get())
            self.plotter.zoom_to_y(y_min, y_max)
        except ValueError:
            pass

    def draw_h_line(self) -> None:
        """ Draws a horizontal line on the plot at the y-axis value specified by the user. """
        try:
            y_value = float(self.h_line_entry.get())
            self.plotter.draw_horizontal_line(y_value)
        except ValueError:
            pass

    def draw_v_line(self) -> None:
        """ Draws a vertical line on the plot at the x-axis value specified by the user. """
        try:
            x_value = float(self.v_line_entry.get())
            self.plotter.draw_vertical_line(x_value)
        except ValueError:
            pass

    def plot_band_gap(self):
        """Plot a vertical line corresponding to the specified band gap energy."""
        try:
            band_gap_energy = float(self.band_gap_entry.get())
            # Convert the band gap energy to a wavelength in nm
            wavelength_nm = 1239.8 / band_gap_energy
            # Plot the vertical line on the plot
            self.plotter.draw_vertical_line(wavelength_nm)
            zoom = float(self.band_gap_zoom.get())
            x_min = wavelength_nm - zoom
            x_max = wavelength_nm + zoom
            self.plotter.zoom_to_x(x_min, x_max)
        except ValueError:
            pass
