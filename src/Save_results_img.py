import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
from datetime import date

from matplotlib.ticker import (MultipleLocator)


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

        # params = {'legend.fontsize': 'small',
        #           'axes.labelsize': 'small',
        #           'axes.titlesize': 'small',
        #           'xtick.labelsize': 'small',
        #           'ytick.labelsize': 'small'}
        self.wavelength = self.data[self.sample_name]['Wavelength']
        self.transmittance_avg = self.data[self.sample_name]['Transmittance_Avg']
        self.transmittance_std = self.data[self.sample_name]['Transmittance_Std_Dev']
        self.haze_avg = self.data[self.sample_name]['Haze_Avg']
        self.haze_std = self.data[self.sample_name]['Haze_Std_Dev']
        self.path = self.data[self.sample_name]['path']
        self.img_width = float(self.parent.parent.image_width_entry.get()) * cm
        self.img_height = float(self.parent.parent.image_height_entry.get()) * cm
        self.format = self.parent.parent.image_format_option_menu.get()
        self.plot_transmittance()
        self.plot_haze()

    def plot_transmittance(self):
        fig, ax = plt.subplots(dpi=300, figsize=(self.img_width, self.img_height))
        ax.plot(self.wavelength, self.transmittance_avg, lw=1, zorder=3)
        ax.fill_between(self.wavelength, self.transmittance_avg - self.transmittance_std,
                        self.transmittance_avg + self.transmittance_std, alpha=0.1, zorder=1)

        ax.set_xticks(np.arange(300, 801, 100))
        ax.set_xlim([300, 800])
        ax.xaxis.set_minor_locator(MultipleLocator(25))

        ax.set_yticks(np.arange(0, 101, 10))
        ax.set_ylim([0, 100])
        ax.yaxis.set_minor_locator(MultipleLocator(5))

        ax.set_xlabel('Wavelength ($\mathrm{nm}$)')
        ax.set_ylabel('Transmittance ($\%$)')

        plt.tight_layout()
        path = self.path + '/' + f'{date.today()}_T_' + self.sample_name + '.' + self.format
        fig.savefig(path, format=self.format)
        print(f'Plot of Transmittance for {self.sample_name} is saved in {path}')

    def plot_haze(self):
        fig, ax = plt.subplots(dpi=300, figsize=(self.img_width, self.img_height))
        ax.plot(self.wavelength, self.haze_avg, lw=1, zorder=3)
        ax.fill_between(self.wavelength, self.haze_avg - self.haze_std,
                        self.haze_avg + self.haze_std, alpha=0.1, zorder=1)

        ax.set_xticks(np.arange(300, 801, 100))
        ax.set_xlim([300, 800])
        ax.xaxis.set_minor_locator(MultipleLocator(25))

        ax.set_yticks(np.arange(0, 101, 10))
        ax.set_ylim([0, 100])
        ax.yaxis.set_minor_locator(MultipleLocator(5))

        ax.set_xlabel('Wavelength ($\mathrm{nm}$)')
        ax.set_ylabel('Haze ($\%$)')

        plt.tight_layout()
        path = self.path + '/' + f'{date.today()}_haze_' + self.sample_name + '.' + self.format
        fig.savefig(path, format=self.format)
        print(f'Plot of Haze for {self.sample_name} is saved in {path}')

