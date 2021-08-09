# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:40:24 2021

@author: chrst
"""
import streamlit as st
import math
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils.myStreamlit import myCaption
from utils.Sample import Sample


def remove_sample(sample_name=''):
    if sample_name:
        st.session_state.samples.pop(sample_name, 'None')
        st.session_state.results.pop(sample_name, 'None')
    else:
        st.session_state.samples.clear()

    if st.session_state.current_sample_name == sample_name or sample_name == '':
        st.session_state.current_sample_name = 'Sample 01'
        st.session_state.current_sample_height = 0.0
        st.session_state.data_points.clear()

    st.session_state.key_number += 1


def classData(image_path):
    # Physical Parameters
    visc = 0.00089  # Pa*s
    rho = 1000  # kg/m^3
    g = 9.81  # m/s

    # Real ranges
    # pK values (-log(k [m^2]))
    df_pK = pd.DataFrame({'name': ['Gravel', 'Clean sand', 'Silty sand', 'Silt'],
                          'low': [7, 9, 10, 12],
                          'high': [10, 13, 14, 16]})

    df_cond = pd.DataFrame({'name': ['Gravel', 'Clean sand', 'Silty sand', 'Silt'],
                            'low': [10 ** (-np.array(df_pK['high'][i], dtype=float)) * 1000 * 9.81 / 0.00089 * 60 * 100
                                    for i in range(len(df_pK['high']))],
                            'high': [10 ** (-np.array(df_pK['low'][i], dtype=float)) * 1000 * 9.81 / 0.00089 * 60 * 100
                                     for i in range(len(df_pK['low']))]})

    # Site construction
    st.title('Compare soils')
    st.write('Use this page to compare multiple soil samples you collected '
             'on the previous page, download sample data, or upload '
             'previous soil samples. You can also use this to collect data '
             'across your classroom.')
    st.header('Upload, download, or remove samples')

    # Upload file from csv
    panel_upload = st.beta_expander('Upload from csv', expanded=False)
    with panel_upload:
        left, right = st.beta_columns(2)

        with left:
            upload_file = st.file_uploader('Choose a file', key=f'{st.session_state.key_number}')

            if upload_file is not None:
                upload_file.seek(0)
                df_upload = pd.read_csv(upload_file)

        with right:
            if upload_file is not None:
                sample_name = df_upload['Sample name'][0]

                # If sample doesn't already exist and data is correct size
                if sample_name not in st.session_state.samples and len(df_upload['Water height (cm)']) == \
                        len(df_upload['Time (s)']) and len(df_upload['Water height (cm)']) >= 2:
                    df_main = pd.DataFrame({'Water height (cm)': df_upload['Water height (cm)'],
                                            'Time (s)': df_upload['Time (s)']})
                    height = df_upload['Sample height (cm)'][0]

                    # Display sample height and water height vs time
                    st.write(pd.DataFrame({'Sample height (cm)': [height]}))
                    st.write(df_main)

                    # Create sample from data and add to dict of samples
                    new_sample = Sample(sample_height=df_upload['Sample height (cm)'][0],
                                        data_points=df_main)
                    st.session_state.samples[sample_name] = new_sample

    # Data Downloading
    panel_download = st.beta_expander('Download to csv', expanded=False)
    with panel_download:
        left, right = st.beta_columns(2)
        with left:
            st.subheader('Download to csv:')
        with right:
            for sample_name, sample in st.session_state.samples.items():
                num_rows = len(sample.data_points)

                # Pad lists to number of of data points
                sample_name_list = ['' for i in range(num_rows)]
                sample_name_list[0] = sample_name

                # Pad lists to number of of data points
                sample_height_list = ['' for i in range(num_rows)]
                sample_height_list[0] = sample.sample_height

                df_export = pd.DataFrame({'Sample name': sample_name_list, 'Sample height (cm)': sample_height_list,
                                          'Water height (cm)': sample.data_points['Water height (cm)'],
                                          'Time (s)': sample.data_points['Time (s)']})

                # Generate csv file
                csv = df_export.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                desired_filename = sample_name + '.csv'

                # Generate link to download csv
                href = f'<a href="data:file/csv;base64,{b64}" download ="{desired_filename}">' + \
                       sample_name + ': Download as a .csv file</a>'

                # Write out link
                st.markdown(href, unsafe_allow_html=True)

    # Remove samples
    panel_remove = st.beta_expander('Remove samples', expanded=False)
    with panel_remove:
        left, mid, right = st.beta_columns(3)
        with left:
            st.subheader('Remove samples:')
        with mid:
            st.write(' ')
            st.write(' ')

            for sample_name, sample in st.session_state.samples.items():
                remove_sample_button = st.button(f'Remove {sample_name}', on_click=remove_sample,
                                                 kwargs={'sample_name': sample_name})
        with right:
            st.write(' ')
            st.write(' ')

            should_clear_samples = st.button('Clear all samples', on_click=remove_sample)

    # Display all samples
    st.header('Compare your samples')
    if not st.session_state.samples:
        st.write('Upload a sample or process the data using the **Process \
                 experiment data** tab')
    else:
        # Display data plots
        # Initialize figure
        maxH = 0
        maxV = 0

        # Process, Save, and Plot data
        fig, (ax1a, ax1b) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        for sample_name, sample in st.session_state.samples.items():
            heights = sample.data_points['Water height (cm)']
            times = sample.data_points['Time (s)']

            velocity = [-(h2 - h1) / (t2 - t1) for h1, h2, t1, t2 in
                        zip(heights[0:-1], heights[1::], times[0:-1], times[1::])]
            heights_average = [(h1 + h2) / 2 / sample.sample_height for h1, h2 in zip(heights[1::], heights[0:-1])]

            maxH = max([maxH, max(heights_average)])
            maxV = max([maxV, max(velocity)])

            ax1a.scatter(x=heights,
                         y=times,
                         marker='o', label=sample_name)
            ax1b.scatter(x=heights_average,
                         y=velocity,
                         marker='o', label=sample_name)

            # Curve fitting
            linFunc = lambda x, a: a * x
            [mdl, mdlcov] = curve_fit(linFunc, heights_average, velocity)  # units of s

            permeability = mdl * visc * sample.sample_height / 100 / rho / g
            retention = 0
            if mdl > 0:
                retention = -math.log10(mdl * visc / rho / g)
            conductivity = mdl * sample.sample_height * 60

            # TODO - Results could be a part of the sample class
            st.session_state.results[sample_name] = pd.DataFrame({'Permeability': permeability,
                                                                  'Retention': retention,
                                                                  'Conductivity': conductivity})

            # Plot fit
            linH = np.linspace(0, maxH)
            ax1b.plot(linH, linH * mdl, '--', linewidth=2)

        # Format axes
        ax1a.set_xlabel('Water Height (cm)', fontsize=12)
        ax1a.set_ylabel('Time (s)', fontsize=12)
        ax1a.legend([sample_name for sample_name in st.session_state.samples],
                    fontsize=12)

        ax1b.set_xlabel('Water Height / Soil height', fontsize=12)
        ax1b.set_ylabel('Water speed (cm/s)', fontsize=12)
        ax1b.legend([sample_name for sample_name in st.session_state.samples],
                    fontsize=12)
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

        st.markdown('From these plots, we can measure the hydraulic conductivity '
                    '$K$ using a formula called Darcy\'s Law:')
        st.latex('U=K(h/L)')
        st.markdown('U is the current speed of the water, and h/L is the height '
                    'of the water divided by the height of the soil sample. '
                    'The hydraulic conductivity $K$ is the slope of the dashed '
                    'line fit to your data on the right: a steeper line indicates '
                    'a soil with a higher conductivity, and hence will tend to '
                    'drain water at higher speeds. We can quantify the '
                    'conductivity by measuring this slope:')

        # Write data to table
        sample_conductivity = ['{:.2f}'.format(result['Conductivity'][0]) for result in
                               st.session_state.results.values()]
        df_perms = pd.DataFrame({'Sample name': st.session_state.results.keys(),
                                 'Hydraulic conductivity (cm/min)': sample_conductivity})

        _, col, _ = st.beta_columns((.1, 1, .1))
        with col:
            st.write(df_perms)

        # Compare to real soil distributions
        st.header('Compare with real soils')
        col1, col2 = st.beta_columns((1, 1))
        with col1:
            st.markdown('A typical soil or gravel (Figure 1) can '
                        'have a conductivity as high as 10,000 cm/s, or as low as  '
                        '0.000001 cm/min: that\'s closer to 1 mm every year!')
            st.markdown('This conductivity is not exactly the same as the speed '
                        'you measure. In your experiment, '
                        'you may have noticed that the water moves fastest when '
                        'it is higher above the soil sample. *Why do you think '
                        'water flows fastest when there is a tall water height '
                        '(or "head") above the soil?* '
                        'In the real world, this means that the water speed '
                        'also depends on the amount of water in the soil.')
            st.markdown('When looking at a map (Figure 1), it is usually convenient '
                        'to separate soils into a few categories, so it is easier '
                        'to talk about the conductivity and water content in different regions. '
                        'Let''s see how your samples compare to these ranges:')

        with col2:
            st.image(f'{image_path}/MapConductivity.png')
            myCaption('<b>Figure 1</b>: Map of soil types across USA. Colors represent '
                      'changes in soil water retention (adapted from Gleeson '
                      '<i>et al.</i> Geophysical Research Letters 38(2) 2011.')

        fig2, ax2 = plt.subplots(nrows=1, ncols=1,
                                 figsize=(8, len(df_cond['low']) * .5 + len(st.session_state.samples) * .5))

        num_real = len(df_cond['low'])
        for i in range(num_real):
            ax2.plot([df_cond['low'][i], df_cond['high'][i]], [-1 - i, -1 - i], '-', linewidth=4)
            plt.text(x=10 ** ((math.log10(df_cond['low'][i]) + math.log10(df_cond['high'][i])) / 2), y=-1 - i,
                     s=df_cond['name'][i],
                     fontsize=12, horizontalalignment='center',
                     verticalalignment='bottom')

        for sample_name, result in st.session_state.results.items():
            ax2.scatter(x=result['Conductivity'][0], y=-1 - num_real - (i + 1))
            plt.text(x=result['Conductivity'][0], y=-1 - num_real - (i + 1),
                     s='  ' + sample_name,
                     fontsize=12, horizontalalignment='left',
                     verticalalignment='center')

        plt.ylabel('')
        plt.yticks([], [])
        ax2.set_ylim([-len(df_cond['low']) - len(st.session_state.samples) - 1.5, 0])
        ax2.set_xlabel('Hydraulic conductivity (cm/min)', fontsize=12)
        ax2.set_xscale('log')

        st.write(fig2)
        st.markdown('You may notice that your samples tend to be higher '
                    'conductivity than the ranges above, and even higher than '
                    'the real soils in the map in Figure 1! This is because '
                    'your samples are likely topsoil (near the surface), while '
                    'scientists studying water flow (hydrologists) often take '
                    'samples from deeper down. *Why do you think samples deeper '
                    'underground have a lower conductivity than the samples you '
                    'measured?*')
