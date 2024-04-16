import os

import pandas as pd
from datetime import date


class SaveIntoSingleExcel:
    def __init__(self, parent):
        self.parent = parent
        self.data = self.parent.data_folders
        self.include_sample_names = self.parent.add_sample_name_row_flag
        if self.parent.save_all_flag:
            self.save_combined_results_xlsx()

    def save_combined_results_xlsx(self) -> None:
        """
        Save the combined metrics of all samples into a single Excel file.

        """
        # Initialize an empty DataFrame with Wavelength as the first column

        # Initialize an empty DataFrame with Wavelength as the first column
        combined_df = pd.DataFrame()
        combined_df['Wavelength'] = self.data[next(iter(self.data))]['Wavelength']

        for sample_name, metrics in self.data.items():
            # Adding metrics for each sample as new columns
            combined_df[f'{sample_name}_Transmittance_Avg'] = metrics['Transmittance_Avg']
            combined_df[f'{sample_name}_Transmittance_Std_Dev'] = metrics['Transmittance_Std_Dev']

        for sample_name, metrics in self.data.items():
            # Adding metrics for each sample as new columns
            combined_df[f'{sample_name}_Haze_Avg'] = metrics['Haze_Avg']
            combined_df[f'{sample_name}_Haze_Std_Dev'] = metrics['Haze_Std_Dev']

        # Save to Excel
        root_folder_path = self.parent.root_folder_path
        excel_file_path = os.path.join(root_folder_path, f'{date.today()}_combined_results.xlsx')
        combined_df.to_excel(excel_file_path, index=False)
        print(f'Combined results file is saved in {excel_file_path}')
