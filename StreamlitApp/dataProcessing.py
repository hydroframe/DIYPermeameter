# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:00:50 2021

@author: chrst
"""
# from MultiApp2 import MultiApp
import streamlit as st
import altair as alt
# import time
# import math
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
# from scipy.optimize import curve_fit
from myStreamlit import myCaption


def dataProcessing(cached_name, cached_height, cached_data, cached_dataSets):
    st.title('Let''s process the data from your experiment!')
    st.write('Use this online tool to enter data from your experiment. '
             'It will compute the **permeability** of your soil sample. '
             'Once you are happy with your data, you can save this and '
             'add it to your soil collection on the next page!')
    
    
    sampleName = st.text_input('Give your soil sample a name.')  
    if len(cached_name)==0:
        if len(sampleName)==0:
            sampleName='Sample 01'
            cached_name.append({"Sample name": sampleName})
    else:
        if len(sampleName)>0:
            cached_name.pop()
            cached_name.append({"Sample name": sampleName})
    st.write("Current sample: **"+cached_name[0].get("Sample name")+"**")
    
    
    sampleHeightText = st.text_input("Enter height of your soil sample")
    if len(sampleHeightText)>0:
        if len(cached_height)>0:
            cached_height.pop()
        cached_height.append({"Soil sample height (cm)": float(sampleHeightText)})
    if len(cached_height)>0:
        st.write(pd.DataFrame(cached_height))
    newDataText = st.text_input("Enter a new data point in format #,#.\
                                    The first number should be a water height \
                                        in centimeters, \
                                        and the second number should be the time \
                                            in seconds.")
    newDataTextSplit = newDataText.replace(',',' ').split()
    newDataFloat = [float(item) for item in newDataTextSplit]
    left, mid, right = st.beta_columns(3)
    with left:
        if st.button("Add row"):
            if len(newDataFloat)==2:
                cached_data.append({'Water height (cm)': newDataFloat[0],
                                  'Time (s)': newDataFloat[1]})
            else:
                st.write('You need to add exactly 2 numbers at a time: water height and time')
    with mid:
        if st.button("Remove last row"):
            if len(cached_data)>0:
                cached_data.pop()
    with right:
        if st.button("Clear all"):
            if len(cached_data)>0:
                for i in range(len(cached_data)):
                   cached_data.pop()
    df_cache=pd.DataFrame(cached_data)
    if df_cache.size>0:
        st.write(df_cache)
        scatter_chart = st.altair_chart(
            alt.Chart(df_cache)
                .mark_circle(size=60)
                .encode(x='Water height (cm)', y='Time (s)')
                .interactive()
        )
        
        if st.button("Save this sample data set"):
            cached_dataSets.append({'SampleName':sampleName,
                                    'df':df_cache,
                                    'height':cached_height})
    st.markdown('Your permeability-meter works by monitoring the speed ($U$) \
             of water as it passes through your soil sample (height $L$). \
             Given the height of the water $h$, and some other constants \
             for water that are known. Given some other known \
             (viscosity $µ$, density $ρ$, gravitational acceleration $g$) \
             the permeability $k$ can be computed using a formula called \
             **Darcy''s Law**:')
    st.latex('k=(µLU)/(ρgh)')
    st.markdown('Since you have the speed recorded for many different \
                water heights, we can get an even better estimate by \
                plotting a best fit line for your data of velocity $U$ \
                versus water height $h$:')
    st.latex('U=(ρgk)/(µL)·h')
    st.markdown('The slope of this best fit line is then $(ρgk)/(µL)$. \
                This site then directly computes $k$ from this slope to \
                give you the permeability of your sample, and the retention $pk$!')           
        
        