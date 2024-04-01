
# Transmittance and Haze Analyzer

## Table of Contents
1. [Overview](#overview)
2. [Description](#description)
3. [Data Preparation](#data-preparation)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Output](#output)
7. [License](#license)

## Overview

This project provides tools for analyzing and visualizing transmittance and haze data, specifically tailored for use with data obtained from a Shimadzu UV-2600 UV-Vis spectrometer equipped with an integrating sphere. It focuses on processing raw data files, extracting meaningful statistical information, and graphical representations of transmittance and haze characteristics of various materials.

## Description

The Transmittance and Haze Analyzer processes data files from the Shimadzu UV-2600 UV-Vis spectrometer to calculate and plot the transmittance and haze properties of samples. The software automatically processes files with specific measurement configurations (T1, T2, T3, and T4 (this filenaming could be reset in the settings)), and computes the necessary parameters for a comprehensive analysis. The measurements are expected to be organized in folders for individual samples, with transmittance and haze measurements in pairs (like T2-1, T4-1, etc.) representing different spots on the same sample for standard deviation calculation. First, T and Haze are calculated for each pair, then averaged, and finally, the standard deviation is calculated.

## Data Preparation

Before proceeding with the analysis, ensure your data is structured properly. The program accepts either a single folder containing all four minimum required data files (T1, T2, T3, T4) or a root folder with subfolders for each set of T1, T2, T3, and T4 measurements. If subfolders contain their own T1 or T3 files, these will take precedence. Folders missing any of the four essential files will be ignored. Organize your data accordingly to facilitate smooth processing.

## Installation

To install the Transmittance and Haze Analyzer, follow these steps to set up your environment and install necessary dependencies.

### Prerequisites

Ensure you have Python installed on your system. This software is compatible with Python 3.6 and later. You can download Python from [python.org](https://www.python.org/downloads/).

### Cloning the Repository

First, clone the repository to your local machine. Open a terminal or command prompt and run the following command:

```bash
git clone https://github.com/Rusya665/Transmittance_and_haze_analyzer
cd transmittance-and-haze-analyzer
```


## Usage

Run the *MAIN.py* to start the analysis. Follow the on-screen instructions to interact with the software.


### Measurement Configurations

- **T1**: Reference transmittance measurement, representing the baseline transmittance of air or an empty integrating sphere.
- **T2**: Transmittance measurement of the sample without considering the scattered light (haze).
- **T3**: Reference haze measurement, establishing a baseline for haze in the empty integrating sphere.
- **T4**: Haze measurement of the sample, focusing on the scattered light caused by the sample itself.

### Calculations

- **Transmittance (T)**: Calculated as `(T2 / T1) * 100`, expressed as a percentage.
- **Haze**: Determined using the formula `Haze = (T4 / T2) - (T3 / T1)`.
  
Multiple measurements (T2 and T4) for each sample are used to calculate the average and standard deviation for both transmittance and haze.

### Control panel
A **control panel** allows you to interact with plots separately, providing options for:

- Toggling the visibility of individual sample data lines
- Zooming into specific regions of the x and y axes
- Drawing horizontal and vertical lines
- Plotting a vertical line corresponding to specified band gap energy
- Removing additional lines
- Choosing marker styles and sizes
- Setting legend visibility and position

## Output
The script generates **.xlsx** files for each sample as weel as two separate plots:

**Transmittance Plot**: Displays the average transmittance of each sample as a function of wavelength, with shaded error bars representing the standard deviation.

**Haze Plot**: Displays the average haze of each sample as a function of wavelength, also with shaded error bars for standard deviation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
