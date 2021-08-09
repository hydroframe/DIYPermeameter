# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
from pages.dataProcessing import dataProcessing
from pages.splashPage import splashPage
from pages.classData import classData
from pages.howBuild import howBuild


##############################################################################
# DEFINE SESSION STATE

if 'current_sample_name' not in st.session_state:
    st.session_state.current_sample_name = 'Sample 01'

if 'current_sample_height' not in st.session_state:
    st.session_state.current_sample_height = 0.0

if 'current_data_point' not in st.session_state:
    st.session_state.current_data_point = []

if 'data_points' not in st.session_state:
    st.session_state.data_points = []

if 'samples' not in st.session_state:
    st.session_state.samples = {}

if 'results' not in st.session_state:
    st.session_state.results = {}

if 'key_number' not in st.session_state:
    st.session_state.key_number = 0

##############################################################################
# APP LEVEL CODE

# Define keys for each page name for easier reference internal to this code
PageDictionary = {
    'What is soil hydraulic conductivity?': 'splashpage',
    'Build your own DIY soil flow-meter': 'howBuild',
    'Process experiment data': 'dataProcessing',
    'Compare soils': 'classData',
}

# Select Page and convert displayed name to my code key for page using PageDictionary
pageSelect = PageDictionary[
    st.sidebar.radio('Pick a page',
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

image_path = 'assets/images'

# Run selected page
if pageSelect == 'splashpage':
    splashPage(image_path)
elif pageSelect == 'howBuild':
    howBuild(image_path)
elif pageSelect == 'dataProcessing':
    dataProcessing()
elif pageSelect == 'classData':
    classData(image_path)
