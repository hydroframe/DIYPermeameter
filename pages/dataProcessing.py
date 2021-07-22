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


def dataProcessing(cached_name, cached_height, cached_data, cached_dataSets):
    def linFunc(x, a):
        return a * x

    st.title('Let\'s process the data from your experiment!')
    st.write('Use this online tool to enter data from your experiment. '
             'It will compute the **permeability** of your soil sample. '
             'Once you are happy with your data, you can save this and '
             'add it to your soil collection on the next page!')

    sampleName = st.text_input('Give your soil sample a name.')
    if len(cached_name) == 0:
        if len(sampleName) == 0:
            sampleName = 'Sample 01'
            cached_name.append({"Sample name": sampleName})
    else:
        if len(sampleName) > 0:
            cached_name.pop()
            cached_name.append({"Sample name": sampleName})
    st.write("Current sample: **" + cached_name[0].get("Sample name") + "**")

    sampleHeightText = st.text_input("Enter height of your soil sample")
    if len(sampleHeightText) > 0:
        if len(cached_height) > 0:
            cached_height.pop()
        cached_height.append({"Soil sample height (cm)": float(sampleHeightText)})
    if len(cached_height) > 0:
        st.write(pd.DataFrame(cached_height))

    newDataText = st.text_input('Enter a new data point in format #,#.'
                                'The first number should be a water height '
                                'in centimeters, '
                                'and the second number should be the time '
                                'in seconds.')

    newDataTextSplit = newDataText.replace(',', ' ').split()
    newDataFloat = [float(item) for item in newDataTextSplit]

    left, mid, right = st.beta_columns(3)
    with left:
        if st.button("Add row"):
            if len(newDataFloat) == 2:
                cached_data.append({'Water height (cm)': newDataFloat[0],
                                    'Time (s)': newDataFloat[1]})
            else:
                st.write('You need to add exactly 2 numbers at a time: water height and time')
    with mid:
        if st.button("Remove last row"):
            if len(cached_data) > 0:
                cached_data.pop()
    with right:
        if st.button("Clear all"):
            if len(cached_data) > 0:
                for i in range(len(cached_data)):
                    cached_data.pop()

    df_cache = pd.DataFrame(cached_data)

    if df_cache.size > 1:
        st.write(df_cache)

    # Display data plots
    if df_cache.size > 2:
        # Initialize figure
        maxH = 0
        maxV = 0

        # Process, Save, and Plot data
        fig, (ax1a, ax1b) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        heights = df_cache['Water height (cm)']
        times = df_cache['Time (s)']
        vels = [-(h2 - h1) / (t2 - t1) for h1, h2, t1, t2 in
                zip(heights[0:-1], heights[1::], times[0:-1], times[1::])]
        heightsAv = [(h1 + h2) / 2 / cached_height[0]['Soil sample height (cm)'] for h1, h2 in
                     zip(heights[1::], heights[0:-1])]

        maxH = max([maxH, max(heightsAv)])
        maxV = max([maxV, max(vels)])

        ax1a.scatter(x=heights,
                     y=times,
                     marker='o')
        ax1b.scatter(x=heightsAv,
                     y=vels,
                     marker='o')

        # Curve fitting
        [mdl, mdlcov] = curve_fit(linFunc, heightsAv, vels)  # Units of s
        MyConductivity = mdl * cached_height[0]['Soil sample height (cm)'] * 60

        # Plot fit
        linH = np.linspace(0, maxH)
        ax1b.plot(linH, linH * mdl, '--', linewidth=2)

        # Format axes
        ax1a.set_xlabel('Water Height (cm)', fontsize=12)
        ax1a.set_ylabel('Time (s)', fontsize=12)
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
        st.subheader('Your sample "' + cached_name[0][
            'Sample name'] + '" has a hydraulic conductivity of ' + '{:.2f} cm/min'.format(MyConductivity[0]))

        # Sample saving
        if st.button("Save this sample data set"):
            sampleNameList = ['' for i in range(len(df_cache))]
            sampleNameList[0] = cached_name[0]['Sample name']
            cached_heightList = ['' for i in range(len(df_cache))]
            cached_heightList[0] = cached_height[0]['Soil sample height (cm)']
            cached_dataSets.append(pd.DataFrame({'Sample name': sampleNameList,
                                                 'Sample height (cm)': cached_heightList,
                                                 'Time (s)': df_cache['Time (s)'],
                                                 'Water height (cm)': df_cache['Water height (cm)']}))
