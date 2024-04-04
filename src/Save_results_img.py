import os
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib.ticker import (AutoMinorLocator, MaxNLocator)


class SavePlotsImg:
    def __init__(self, parent, sample_name: str):
        self.parent = parent
        self.sample_name = sample_name
        self.data = self.parent.data
        style.use('seaborn-v0_8-colorblind')

        plt.rc('text', usetex=True)  # use latex text

        cm = 1 / 2.54  # convert px to cm
        plt.rcParams.update({
            "text.usetex": False,
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial"]})

        self.wavelength = self.data[self.sample_name]['Wavelength']
        self.transmittance_avg = self.data[self.sample_name]['Transmittance_Avg']
        self.transmittance_std = self.data[self.sample_name]['Transmittance_Std_Dev']
        self.haze_avg = self.data[self.sample_name]['Haze_Avg']
        self.haze_std = self.data[self.sample_name]['Haze_Std_Dev']
        self.path = self.data[self.sample_name]['path']
        self.img_width = float(self.parent.parent.image_width_entry.get()) * cm
        self.img_height = float(self.parent.parent.image_height_entry.get()) * cm
        self.format = self.parent.parent.image_format_option_menu.get()
        self.y_min = float(self.parent.parent.entry_y_min.get())
        self.y_max = float(self.parent.parent.entry_y_max.get())
        self.x_min = float(self.parent.parent.entry_x_min.get())
        self.x_max = float(self.parent.parent.entry_x_max.get())
        self.plot_transmittance()
        self.plot_haze()

    def plot_transmittance(self):
        fig, ax = plt.subplots(dpi=300, figsize=(self.img_width, self.img_height))
        ax.plot(self.wavelength, self.transmittance_avg, lw=1, zorder=3)
        ax.fill_between(self.wavelength, self.transmittance_avg - self.transmittance_std,
                        self.transmittance_avg + self.transmittance_std, alpha=0.1, zorder=1)

        ax.set_xlim([self.x_min, self.x_max])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))

        ax.set_ylim([self.y_min, self.y_max])
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # For integer ticks
        ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))

        ax.set_xlabel('Wavelength ($\mathrm{nm}$)')
        ax.set_ylabel('Transmittance ($\%$)')

        plt.tight_layout()
        path = self.path + '/' + f'{date.today()}_T_' + self.sample_name + '.' + self.format
        # Check if the file exists and modify the filename accordingly
        counter = 1
        original_path = path
        while os.path.exists(path):
            len_extension = len(self.format) + 1
            path = f"{original_path[:-len_extension]}-copy{counter}{original_path[-len_extension:]}"
            counter += 1
            print(f'The filename already exist {original_path} changed to {path}')
        fig.savefig(path, format=self.format)
        plt.close(fig)  # Close the figure after saving to free up memory
        print(f'Plot of Transmittance for {self.sample_name} is saved in {path}')

    def plot_haze(self):
        fig, ax = plt.subplots(dpi=300, figsize=(self.img_width, self.img_height))
        ax.plot(self.wavelength, self.haze_avg, lw=1, zorder=3)
        ax.fill_between(self.wavelength, self.haze_avg - self.haze_std,
                        self.haze_avg + self.haze_std, alpha=0.1, zorder=1)

        ax.set_xlim([self.x_min, self.x_max])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))

        ax.set_ylim([self.y_min, self.y_max])
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # For integer ticks
        ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))

        ax.set_xlabel('Wavelength ($\mathrm{nm}$)')
        ax.set_ylabel('Haze ($\%$)')

        plt.tight_layout()
        path = self.path + '/' + f'{date.today()}_haze_' + self.sample_name + '.' + self.format
        # Check if the file exists and modify the filename accordingly
        counter = 1
        original_path = path
        while os.path.exists(path):
            len_extension = len(self.format) + 1
            path = f"{original_path[:-len_extension]}-copy{counter}{original_path[-len_extension:]}"
            counter += 1
            print(f'The filename already exist {original_path} changed to {path}')
        fig.savefig(path, format=self.format)
        plt.close(fig)  # Close the figure after saving to free up memory
        print(f'Plot of Haze for {self.sample_name} is saved in {path}')
