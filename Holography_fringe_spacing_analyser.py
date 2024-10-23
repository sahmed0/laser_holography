# -*- coding: utf-8 -*-
'''
Plots peaks for laser TV holography lab.
Input position and intensity data from ImageJ,
Code will plot the peaks and output average fringe separation over a homogenous section.
By Sajid  26/03/2024
'''


import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

# Read the CSV file
# Adjust the path as necessary
data = pd.read_csv('0-60normal.csv', header=None)
x = data[0].values  # Assuming the first column is x
y = data[1].values  # Assuming the second column is y

sigma_peak_position = 0.01

# Filter data for x-values between 4 and 10
filtered_indices = (x >= 5.5) & (x <= 10)
x_filtered = x[filtered_indices]
y_filtered = y[filtered_indices]

# Find peaks within the filtered data
peaks, _ = find_peaks(y_filtered, prominence=0.4, width=6)

# Calculate the average x-distance between adjacent peaks
average_distance = None
if len(peaks) > 1:  # Ensure there are at least two peaks to calculate distances
    # Differences between adjacent peak x-values
    peak_distances = np.diff(x_filtered[peaks])
    average_distance = np.mean(peak_distances)
    N = len(peak_distances)  # Number of distances
    # Uncertainty in each distance
    sigma_distance = np.sqrt(2) * sigma_peak_position
    sigma_average_distance = sigma_distance / np.sqrt(N)  # Uncertainty in th

# Update the label for the peaks with the average distance information
peak_label = 'Peaks'
if average_distance is not None:
    peak_label = rf'Peaks ($\overline{{\Delta d}} = {average_distance:.3f} \pm {sigma_average_distance:.3f}$ cm)'


# Plotting the filtered data and the identified peaks
plt.plot(x_filtered, y_filtered, label='Filtered Data')
plt.plot(x_filtered[peaks], y_filtered[peaks], 'x', color='red',
         label=peak_label)  # Mark the peaks with updated label

plt.title('Fringe Pattern 0-60V')
plt.xlabel('Scaled Distance (cm)')
plt.ylabel('Intensity')
plt.legend()
plt.show()
