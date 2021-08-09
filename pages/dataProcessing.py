# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:00:50 2021

@author: chrst
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils.Sample import Sample


def dataProcessing():
    st.title('Let\'s process the data from your experiment!')
    st.write('Use this online tool to enter data from your experiment. '
             'It will compute the **permeability** of your soil sample. '
             'Once you are happy with your data, you can save this and '
             'add it to your soil collection on the next page!')

    # Obtain sample name
    sample_name = st.text_input(label='Give your soil sample a name.', key='current_sample_name',
                                value=st.session_state.current_sample_name)
    st.write('Current sample: **' + st.session_state.current_sample_name + '**')

    # Obtain sample height height
    sample_height = st.number_input(label='Enter height of your soil sample', key='current_sample_height',
                                    value=st.session_state.current_sample_height)
    if sample_height > 0:
        st.write(pd.DataFrame([{'Soil sample height (cm)': st.session_state.current_sample_height}]))

    # Sample data points
    data_point_text = st.text_input(label='Enter a new data point in format #,#.'
                                          'The first number should be a water height '
                                          'in centimeters, '
                                          'and the second number should be the time '
                                          'in seconds.', )

    if len(data_point_text) > 0:
        individual_points = data_point_text.split(',')

        # Convert string to floats, and report error if exception raised
        try:
            st.session_state.current_data_point = [float(item) for item in individual_points]
        except ValueError:
            st.error('Please enter numeric data in the format: #,#')
            st.session_state.current_data_point = []

    left, mid, right = st.columns(3)
    with left:
        if st.button('Add row'):
            add_row = True

            # If data point format is incorrect, do not add row
            if len(st.session_state.current_data_point) != 2:
                add_row = False
                st.warning('Please enter 2 numbers at a time: water height and time')
            else:
                if len(st.session_state.data_points) > 0:
                    # Access most recent data point
                    last_point = st.session_state.data_points[-1]

                    # If water height is increasing, do not add row
                    if st.session_state.current_data_point[0] > last_point['Water height (cm)']:
                        add_row = False
                        st.warning('Water height should not be increasing')

                    # If time value is not equal to most recent time value, do not add row
                    if st.session_state.current_data_point[1] <= last_point['Time (s)']:
                        add_row = False
                        st.warning('Consecutive time values must increase')

            if add_row:
                st.session_state.data_points.append(
                    {'Water height (cm)': st.session_state.current_data_point[0],
                     'Time (s)': st.session_state.current_data_point[1]})

    with mid:
        if st.button('Remove last row'):
            if len(st.session_state.data_points) > 0:
                st.session_state.data_points.pop()
    with right:
        if st.button('Clear all'):
            st.session_state.current_data_point.clear()
            st.session_state.data_points.clear()

    # Display dataframe of points
    points_df = pd.DataFrame(st.session_state.data_points)
    if points_df.size > 1:
        st.write(points_df)

    # Display data plots
    if st.session_state.current_sample_height > 0 and points_df.size > 2:
        # Initialize figure
        maxH = 0
        maxV = 0

        # Process, Save, and Plot data
        fig, (ax1a, ax1b) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        heights = points_df['Water height (cm)']
        times = points_df['Time (s)']
        velocity = [-(h2 - h1) / (t2 - t1) for h1, h2, t1, t2 in
                    zip(heights[0:-1], heights[1::], times[0:-1], times[1::])]
        heights_average = [(h1 + h2) / 2 / st.session_state.current_sample_height for h1, h2 in
                           zip(heights[1::], heights[0:-1])]

        maxH = max([maxH, max(heights_average)])
        maxV = max([maxV, max(velocity)])

        ax1a.scatter(x=times,
                     y=heights,
                     marker='o')
        ax1b.scatter(x=heights_average,
                     y=velocity,
                     marker='o')

        # Curve fitting
        linFunc = lambda x, a: a * x
        [mdl, mdlcov] = curve_fit(linFunc, heights_average, velocity)  # Units of s
        conductivity = mdl * st.session_state.current_sample_height * 60

        # Plot fit
        linH = np.linspace(0, maxH)
        ax1b.plot(linH, linH * mdl, '--', linewidth=2)

        # Format axes
        ax1a.set_ylabel('Water Height (cm)', fontsize=12)
        ax1a.set_xlabel('Time (s)', fontsize=12)
        ax1b.set_xlabel('Water Height / Soil height', fontsize=12)
        ax1b.set_ylabel('Water speed (cm/s)', fontsize=12)
        ax1b.set_xlim([0, 1.1 * maxH])
        ax1b.set_ylim([0, 1.1 * maxV])

        # Loosen subplot spacing
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=0.4)
        st.write(fig)

        st.subheader('How this site computes your hydraulic conductivity')
        st.markdown('Your flow-meter works by monitoring the speed ($U$) '
                    'of water as it passes through your soil sample (height $L$). '
                    'Given the height of the water $h$, the hydraulic conductivity '
                    '$K$ can be computed using a formula called '
                    '**Darcy\'s Law**:')
        st.latex('U=K(h/L)')
        st.markdown('Since you have the speed recorded for many different '
                    'water heights, we can get an even better estimate by '
                    'plotting a best fit line for your data of velocity $U$ '
                    'versus water height divided by soil height $h/L$. The slope '
                    'of this best fit line (or steepness of the line) is the '
                    'hydraulic conductivity $K$. '
                    '*Can you explain now how the hydraulic conductivity is related '
                    'to the speed that water drains, but is not exactly the same?*')
        st.subheader('Your sample "' + st.session_state.current_sample_name + '" has a hydraulic conductivity of '
                     + '{:.2f} cm/min'.format(conductivity[0]))

        # Sample saving
        if st.button('Save this sample data set'):
            # Create Sample object
            current_sample = Sample(st.session_state.current_sample_height,
                                    points_df)

            st.session_state.samples[st.session_state.current_sample_name] = current_sample
