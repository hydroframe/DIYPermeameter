# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import math
from pages.dataProcessing import dataProcessing
from pages.splashPage import splashPage
from pages.classData import classData
from pages.howBuild import howBuild


##############################################################################
# DEFINE CACHES

@st.cache(allow_output_mutation=True)
def cached_data():
    return []


@st.cache(allow_output_mutation=True)
def cached_height():
    return []


@st.cache(allow_output_mutation=True)
def cached_name():
    return []


@st.cache(allow_output_mutation=True)
def cached_dataSets():
    return []


@st.cache(allow_output_mutation=True)
def cached_results():
    return []


##############################################################################
# Code for each page. 
# Eventually offload to separate functions to clean up, 
# and replace with import statement above

def challenge():
    st.title('Hello challenge')
    kLoam = 3.06374218 * 10 ** -13  # m^2
    pkLoam = -math.log10(kLoam)  # ~12.5

    st.markdown('A good loam for growing plants has a retention of $R=12.5$ '
                '(permeability $k=3·10^{-13}~\mathrm{m}^2$) (Cosby *et al.* '
                'Water Resources Research, Vol. 20(6), 1984).')

    st.markdown('*If pk is too high, avoid overwatering or avoid walking on wet soil'
                '(compacts it, further increasing pk)'
                '*aerate soil to decrease pk'
                '*Add mulch or compost to increase pk')


##############################################################################
# APP LEVEL CODE

# Define keys for each page name for easier reference internal to this code
PageDictionary = {
    'What is soil hydraulic conductivity?': 'splashpage',
    'Build your own DIY soil flow-meter': 'howBuild',
    'Process experiment data': 'dataProcessing',
    'Compare soils': 'classData',
    'Designer soil challenge': 'challenge'
}

# Select Page and convert displayed name to my code key for page using PageDictionary
pageSelect = PageDictionary[
    st.sidebar.radio("Pick a page",
                     ('What is soil hydraulic conductivity?',
                      'Build your own DIY soil flow-meter',
                      'Process experiment data',
                      'Compare soils'))]

# Set up some custom html commands
st.markdown("""
            <style>
            .caption {
                font-size:12px !important;
            }
            </style>
            <style>
            .captionLatex {
                font-size:12px !important;
                font-family: cmr;
            }
            </style>
            
            """, unsafe_allow_html=True)

# Run selected page
if pageSelect == 'splashpage':
    splashPage()
elif pageSelect == 'howBuild':
    howBuild()
elif pageSelect == 'dataProcessing':
    dataProcessing(cached_name(), cached_height(), cached_data(), cached_dataSets())
elif pageSelect == 'classData':
    classData(cached_dataSets(), cached_results())
elif pageSelect == 'challenge':
    challenge()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")
