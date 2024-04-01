import os
from datetime import date

import numpy as np
import pandas as pd
from numpy import ndarray

from src.Save_results_img import SavePlotsImg


class ProcessSpectroscopyData:
    def __init__(self, parent):
        self.parent = parent
        self.data = self.parent.data_folders
        self.file_naming = self.parent.file_naming

    def process_samples(self):
        """
        Process each sample in self.data_folders and perform calculations.
        """

        for sample_name, paths in self.data.items():
            # Load data for T1 and T3, splitting into wavelengths and measurements
            t1 = pd.read_csv(paths['t1'], sep=",", header=1).values.ravel()
            t3 = pd.read_csv(paths['t3'], sep=",", header=1).values.ravel()
            measurements_t1 = t1[1::2]  # Measurements are at odd indices
            measurements_t3 = t3[1::2]

            # Extract wavelength from the first t2 file, assuming it's the first column
            self.data[sample_name]['Wavelength'] = t1[::2]

            # Load and process T2 and T4
            t2_data_frames = [pd.read_csv(file, sep=",", header=1) for file in paths['t2']]
            t4_data_frames = [pd.read_csv(file, sep=",", header=1) for file in paths['t4']]
            t2 = np.concatenate([df.iloc[:, 1:].values for df in t2_data_frames], axis=1)
            t4 = np.concatenate([df.iloc[:, 1:].values for df in t4_data_frames], axis=1)
            # Perform calculations
            self.calculate_metrics(measurements_t1, t2, measurements_t3, t4, sample_name, len(paths['t2']))

            # Save results
            if self.parent.save_images_flag:
                SavePlotsImg(self, sample_name)
            if self.parent.save_xlsx_flag:
                self.save_results_xlsx(sample_name)

    def calculate_metrics(self, t1: ndarray, t2: ndarray, t3: ndarray, t4: ndarray,
                          sample_name: str, num_measurement_areas: int) -> None:
        """
        Calculate metrics for transmittance (T) and haze.

        :param t1: ndarray: Reference transmittance measurement.
        :param t2: ndarray: Transmittance measurements of the sample.
        :param t3: ndarray: Reference haze measurement.
        :param t4: ndarray: Haze measurements of the sample.
        :param sample_name: str: Name of the currently proceeding sample.
        :param num_measurement_areas: int: Number of areas measured for the same sample.
        :return: None

        The transmittance metrics are calculated as follows:
        - Transmittance Average (Transmittance_Avg):
            100 * (average of t2 values / t1)
        - Transmittance Variance (Transmittance_Var):
            variance of t2 values
        - Transmittance Standard Deviation (Transmittance_Std_Dev):
            standard deviation of t2 values

        The haze metrics for each measurement area are calculated using:
        Haze = 100 * ((t4 / t2) - (t3 / t1))

        After obtaining haze calculations for each area, the following aggregate metrics are computed:
        - Haze Average (Haze_Avg):
            average of haze values across all measurement areas
        - Haze Variance (Haze_Var):
            variance of haze values across all measurement areas
        - Haze Standard Deviation (Haze_Std_Dev):
            standard deviation of haze values across all measurement areas
        """
        # Calculate transmittance metrics for each measurement area
        # transmittance_calculations_per_area = [100 * (t2[:, area_index] / t1)
        #                                        for area_index in range(num_measurement_areas)]

        # transmittance_avg_per_area = np.average(np.vstack(transmittance_calculations_per_area), axis=0)
        # transmittance_var_per_area = np.var(np.vstack(transmittance_calculations_per_area), axis=0)
        # transmittance_std_dev_per_area = np.std(np.vstack(transmittance_calculations_per_area), axis=0)

        transmittance_avg_per_area = np.average(t2, axis=1)
        transmittance_var_per_area = np.var(t2, axis=1)
        transmittance_std_dev_per_area = np.std(t2, axis=1)

        # Iterate through each measurement area and calculate haze
        haze_calculations_per_area = [100 * (t4[:, area_index] / t2[:, area_index] - t3 / t1) for area_index in
                                      range(num_measurement_areas)]
        # Calculate average, variance, and standard deviation for haze across all areas
        aggregate_haze_avg = np.average(np.vstack(haze_calculations_per_area), axis=0)
        aggregate_haze_variance = np.var(np.vstack(haze_calculations_per_area), axis=0)
        aggregate_haze_std_dev = np.std(np.vstack(haze_calculations_per_area), axis=0)

        # Store the results in the class data attribute
        self.data[sample_name]['Transmittance_Avg'] = transmittance_avg_per_area
        self.data[sample_name]['Transmittance_Var'] = transmittance_var_per_area
        self.data[sample_name]['Transmittance_Std_Dev'] = transmittance_std_dev_per_area
        self.data[sample_name]['Haze_Avg'] = aggregate_haze_avg
        self.data[sample_name]['Haze_Var'] = aggregate_haze_variance
        self.data[sample_name]['Haze_Std_Dev'] = aggregate_haze_std_dev

    def save_results_xlsx(self, sample_name: str) -> None:
        """
        Save the calculated metrics to an Excel file.

        :param sample_name: str - Name of the sample.
        """
        # Assuming metrics are stored in self.data[sample_name]
        metrics = self.data[sample_name]

        # Prepare DataFrame for Excel
        df = pd.DataFrame({
            "Wavelength": metrics['Wavelength'],
            "Transmittance_Avg": metrics['Transmittance_Avg'],
            "Transmittance_Var": metrics['Transmittance_Var'],
            "Transmittance_Std_Dev": metrics['Transmittance_Std_Dev'],
            "Haze_Avg": metrics['Haze_Avg'],
            "Haze_Var": metrics['Haze_Var'],
            "Haze_Std_Dev": metrics['Haze_Std_Dev']
        })

        # Save DataFrame to Excel
        excel_file_path = os.path.join(self.data[sample_name]['path'], f'{date.today()}_{sample_name}_data.xlsx')
        df.to_excel(excel_file_path, index=False)
        print(f'File was saved for {sample_name} in {excel_file_path}')
