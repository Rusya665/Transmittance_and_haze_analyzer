from __future__ import annotations

import os
from tkinter import messagebox
from typing import Dict

import customtkinter as ctk
from natsort import natsorted

from src.Calculator import ProcessSpectroscopyData
from src.Helpers import pick_the_last_one, find_all_matches
from src.PLot_spectroscopy_data import TransmittanceAndHazePlotter
from src.Save_results_into_single_xlsx import SaveIntoSingleExcel
from src.settings import SETTINGS


class InitialWindow(ctk.CTk):
    """ A CustomTkinter window class that prompts the user to open a file. """

    def __init__(self, file_naming: str = 'file_names_conventional'):
        """
        Initializes the InitialWindow with a title and a fixed size.

        :param file_naming: File naming style. Default is "conventional".
        """
        super().__init__()
        self.t3_path_root = None
        self.t1_path_root = None
        self.root_folder_name = None
        self.root_folder_path = None
        self.common_t1_and_t3_flag = False
        self.data_folders = {}
        self.file_naming = file_naming
        self.title("Open File")
        self.geometry("310x430")
        self.minsize(310, 430)
        self.folders_to_show = {}  # This will be a dictionary to keep track of the counts
        self.save_images_flag = False
        self.save_xlsx_flag = False
        self.save_all_flag = False
        self.add_sample_name_row_flag = False
        self._setup_ui()

    def _setup_ui(self):
        # Button to open a folder
        self.open_button = ctk.CTkButton(self, text="Open File", command=self.open_folder)
        self.open_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Checkboxes for saving options
        self.save_images_checkbox = ctk.CTkCheckBox(self, text="Save plots as png",
                                                    command=self.toggle_option_widgets)
        self.save_images_checkbox.grid(row=1, column=0, pady=10)
        self.save_xlsx_checkbox = ctk.CTkCheckBox(self, text="Save xlsx's",
                                                  command=lambda: self.flag_setter_checkboxes('save_xlsx'))
        self.save_xlsx_checkbox.grid(row=1, column=1, pady=10)

        # Labels and Entry fields for image dimensions, initially disabled
        self.label_image_width = ctk.CTkLabel(self, text="Image Width in cm:")
        self.label_image_width.grid(row=2, column=0, pady=(0, 5))
        self.image_width_entry = ctk.CTkEntry(self, placeholder_text="e.g., 16")
        self.image_width_entry.grid(row=3, column=0, pady=(0, 10))
        self.image_width_entry.insert(0, '16')
        self.image_width_entry.last_valid_value = '16'  # Set default last valid value
        self.image_width_entry.configure(state='disabled')
        self.image_width_entry.bind("<KeyRelease>", self.validate_numeric_entry)

        self.label_image_height = ctk.CTkLabel(self, text="Image Height in cm:")
        self.label_image_height.grid(row=2, column=1, pady=(0, 5))
        self.image_height_entry = ctk.CTkEntry(self, placeholder_text="e.g., 12")
        self.image_height_entry.grid(row=3, column=1, pady=(0, 10))
        self.image_height_entry.insert(0, '12')
        self.image_height_entry.last_valid_value = '12'  # Set default last valid value
        self.image_height_entry.configure(state='disabled')
        self.image_height_entry.bind("<KeyRelease>", self.validate_numeric_entry)

        # X-axis settings label and entry
        self.label_x_min = ctk.CTkLabel(self, text="X-axis Min:")
        self.label_x_min.grid(row=4, column=0, pady=(0, 5))
        self.entry_x_min = ctk.CTkEntry(self, placeholder_text="200")
        self.entry_x_min.grid(row=5, column=0, pady=(0, 10))
        self.entry_x_min.insert(0, '200')
        self.entry_x_min.last_valid_value = '200'  # Set default last valid value
        self.entry_x_min.configure(state='disabled')
        self.entry_x_min.bind("<KeyRelease>", self.validate_numeric_entry)

        self.label_x_max = ctk.CTkLabel(self, text="X-axis Max:")
        self.label_x_max.grid(row=4, column=1, pady=(0, 5))
        self.entry_x_max = ctk.CTkEntry(self, placeholder_text="1100")
        self.entry_x_max.grid(row=5, column=1, pady=(0, 10))
        self.entry_x_max.insert(0, '1100')
        self.entry_x_max.last_valid_value = '1100'  # Set default last valid value
        self.entry_x_max.configure(state='disabled')
        self.entry_x_max.bind("<KeyRelease>", self.validate_numeric_entry)

        # Y-axis settings label and entry
        self.label_y_min = ctk.CTkLabel(self, text="Y-axis Min:")
        self.label_y_min.grid(row=6, column=0, pady=(0, 5))
        self.entry_y_min = ctk.CTkEntry(self, placeholder_text="e.g., 0")
        self.entry_y_min.grid(row=7, column=0, pady=(0, 10))
        self.entry_y_min.insert(0, '0')
        self.entry_y_min.last_valid_value = '0'  # Set default last valid value
        self.entry_y_min.configure(state='disabled')
        self.entry_y_min.bind("<KeyRelease>", self.validate_numeric_entry)

        self.label_y_max = ctk.CTkLabel(self, text="Y-axis Max:")
        self.label_y_max.grid(row=6, column=1, pady=(0, 5))
        self.entry_y_max = ctk.CTkEntry(self, placeholder_text="e.g., 100")
        self.entry_y_max.grid(row=7, column=1, pady=(0, 10))
        self.entry_y_max.insert(0, '100')
        self.entry_y_max.last_valid_value = '100'  # Set default last valid value
        self.entry_y_max.configure(state='disabled')
        self.entry_y_max.bind("<KeyRelease>", self.validate_numeric_entry)

        # Label and Dropdown for image format, initially disabled
        self.label_image_format = ctk.CTkLabel(self, text="Image Format:")
        self.label_image_format.grid(row=8, column=0, columnspan=2, pady=(0, 5))
        self.image_format_option_menu = ctk.CTkOptionMenu(self, values=["png", "jpg", "jpeg", "tiff"], state='disabled')
        self.image_format_option_menu.grid(row=9, column=0, columnspan=2, pady=(0, 10))

        # Save all in one Excel
        self.save_all_in_one_checkbox = ctk.CTkCheckBox(self, text="Save all data in one",
                                                        command=lambda: self.flag_setter_checkboxes('Save_all'))
        self.save_all_in_one_checkbox.grid(row=10, column=0, pady=(0, 10), padx=5)

        # self.add_sample_name_row_checkbox = ctk.CTkCheckBox(self, text="Sample name row",
        #                                                     command=lambda:
        #                                                     self.flag_setter_checkboxes('Add_sample_name'))
        # self.add_sample_name_row_checkbox.grid(row=10, column=1, pady=(0, 10), padx=5)
        # self.add_sample_name_row_checkbox.toggle()
        # self.add_sample_name_row_checkbox.configure(state='disabled')

    @staticmethod
    def validate_numeric_entry(event):
        """Validate the entry to allow only numeric input, including negative values."""
        entry_widget = event.widget
        text = entry_widget.get()

        # Allow negative numbers and numbers with a single decimal point
        if text and not (text.replace('.', '', 1).isdigit() or
                         (text.startswith('-') and text[1:].replace('.', '', 1).isdigit())):
            # If the current value isn't empty, it's not numeric, and it's not a negative number
            # (allowing one decimal point), reset the text to the last valid value.
            entry_widget.delete(0, 'end')  # Remove current text
            try:
                entry_widget.insert(0, entry_widget.last_valid_value)  # Insert last valid value
            except AttributeError:
                pass
        else:
            # If the input is valid, store the current value as the last valid value.
            entry_widget.last_valid_value = text

    def toggle_option_widgets(self):
        self.flag_setter_checkboxes('save_images')
        state = 'normal' if self.save_images_flag else 'disabled'
        self.image_width_entry.configure(state=state)
        self.image_height_entry.configure(state=state)
        self.image_format_option_menu.configure(state=state)
        self.entry_x_min.configure(state=state)
        self.entry_x_max.configure(state=state)
        self.entry_y_min.configure(state=state)
        self.entry_y_max.configure(state=state)

    def open_folder(self) -> None:
        """
        This doc is outdated.
        Opens a file dialog for the user to select a file, and initializes a plotter for the file.
        If the file is already opened, increments a counter for the file name.
        """
        self.root_folder_path = None
        self.root_folder_path = ctk.filedialog.askdirectory()  # Use a file dialog to get the file path
        if self.root_folder_path is not None and self.root_folder_path != '':
            self.root_folder_name = os.path.basename(self.root_folder_path)
            # Check if the file is already opened and increment the counter
            if self.root_folder_name in self.folders_to_show:
                self.folders_to_show[self.root_folder_name] += 1
                self.root_folder_name = f"{self.root_folder_name} {self.folders_to_show[self.root_folder_name]}"
            else:
                self.folders_to_show[self.root_folder_name] = 1  # Initialize the counter

            self.state('iconic')

            self.proceed_each_folder()
            self.process_and_sort_data_folders()
            data_calculator = ProcessSpectroscopyData(self)
            data_calculator.process_samples()
            SaveIntoSingleExcel(self)
            TransmittanceAndHazePlotter(self, 'Transmittance')
            TransmittanceAndHazePlotter(self, 'Haze')

    def proceed_each_folder(self):
        """
        Apply the file-picking logic to the root directory and its immediate subdirectories.

        :return: A dictionary with folder names as keys and dictionaries of file paths as values.
        """
        self.data_folders.clear()
        self.common_t1_and_t3_flag = False
        self.t1_path_root, self.t3_path_root = None, None

        # Apply function to the root directory
        self.data_folders[self.root_folder_name] = self.proceed_with_given_folder(self.root_folder_path)
        try:
            self.t1_path_root = self.data_folders[self.root_folder_name]['t1']
            self.t3_path_root = self.data_folders[self.root_folder_name]['t3']
            if self.t1_path_root is not None and self.t3_path_root is not None:
                self.common_t1_and_t3_flag = True
        except KeyError:
            messagebox.showwarning("Warning!", "No spectroscopy data was found!")
            return
        # Apply function to immediate subdirectories
        for entry in os.listdir(self.root_folder_path):
            full_path = os.path.join(self.root_folder_path, entry)
            if os.path.isdir(full_path):
                picked_data = self.proceed_with_given_folder(full_path)
                if picked_data is not None:
                    self.data_folders[entry] = picked_data
        return

    def proceed_with_given_folder(self, folder_path) -> None | Dict:
        """
        Proceed each folder and call spectroscopy calculation method is applicable.

        :return: Dict with the paths
        """
        spectroscopy_data = {}

        t1_file_path = pick_the_last_one(folder_path, SETTINGS[self.file_naming][0])
        t2_files_paths = find_all_matches(folder_path, SETTINGS[self.file_naming][1])
        t3_file_path = pick_the_last_one(folder_path, SETTINGS[self.file_naming][2])
        t4_files_paths = find_all_matches(folder_path, SETTINGS[self.file_naming][3])

        if t1_file_path is None and t2_files_paths is None and t3_file_path is None and t4_files_paths is None:
            return None

        spectroscopy_data["t2"] = t2_files_paths
        spectroscopy_data["t4"] = t4_files_paths

        # Assign common T1 and T3 if needed and available
        if t1_file_path and t3_file_path:
            spectroscopy_data["t1"] = t1_file_path
            spectroscopy_data["t3"] = t3_file_path
        if self.common_t1_and_t3_flag:
            if t1_file_path is None:
                spectroscopy_data["t1"] = self.t1_path_root
            if t3_file_path is None:
                spectroscopy_data["t3"] = self.t3_path_root
        spectroscopy_data['path'] = folder_path
        return spectroscopy_data

    def process_and_sort_data_folders(self):
        """
        Processes and sorts the data folders.

        Removes any entries where:
        - Any of t1, t2, t3, or t4 data is missing (None or empty).
        - The number of T2 and T4 files does not match.

        Sorts the remaining entries using natural sorting.
        """
        # Create a list of keys to remove to avoid modifying the dictionary while iterating
        keys_to_remove = []

        for sample_name, data in self.data_folders.items():
            # Check if any key is None or T2/T4 lists are empty
            if data.get('t1') is None or not data.get('t2') or data.get('t3') is None or not data.get('t4'):
                keys_to_remove.append(sample_name)
                continue

            # Ensure the number of T2 and T4 files is equal
            if len(data['t2']) != len(data['t4']):
                raise ValueError(f"The number of T2 and T4 files does not match for sample '{sample_name}'.")

        # Remove identified samples
        for key in keys_to_remove:
            del self.data_folders[key]

        # Natural sorting of keys
        sorted_keys = natsorted(self.data_folders.keys())
        self.data_folders = {key: self.data_folders[key] for key in sorted_keys}

        return

    def flag_setter_checkboxes(self, which_checkbox: str) -> None:
        if which_checkbox == 'save_images':
            self.save_images_flag = bool(self.save_images_checkbox.get())
        if which_checkbox == 'save_xlsx':
            self.save_xlsx_flag = bool(self.save_xlsx_checkbox.get())
        if which_checkbox == 'Save_all':
            self.save_all_flag = bool(self.save_all_in_one_checkbox.get())
            state_xlsx = 'normal' if self.save_all_flag else 'disabled'
            # self.add_sample_name_row_checkbox.configure(state=state_xlsx)
        # if which_checkbox == 'Add_sample_name':
        #     self.add_sample_name_row_flag = bool(self.add_sample_name_row_checkbox.get())
