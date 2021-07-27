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

image_path = 'assets/images'

# Run selected page
if pageSelect == 'splashpage':
    splashPage(image_path)
elif pageSelect == 'howBuild':
    howBuild(image_path)
elif pageSelect == 'dataProcessing':
    dataProcessing(cached_name(), cached_height(), cached_data(), cached_dataSets())
elif pageSelect == 'classData':
    classData(image_path, cached_dataSets(), cached_results())


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")
