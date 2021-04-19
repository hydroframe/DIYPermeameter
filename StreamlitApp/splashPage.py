# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 19:44:17 2021

@author: chrst
"""

import streamlit as st
import altair as alt
import time
import math
import numpy as np
import pandas as pd
from myStreamlit import myCaption

def splashPage():
    st.title('DIY permeability-meter')
    st.markdown('This site helps you build your own do-it-yourself (DIY) **permeability-meter** \
                 with materials around your home, and measure the permeability of \
                     soils around your home. \
                     You can also compare your soil samples to others, \
                     and attempt the **designer soil challenge**!')
    st.header('Why permeability matters:') 
    col1, col2 = st.beta_columns((1,1))
    with col1:
        st.markdown('Motion of water in the environment ' 
                 'is super important for the health of plants, ecosystems, '
                 'and human drinking water supply. The amount and quality of '
                 'this water depends on how quickly water moves through soils '
                 'and rocks after rainfall (Figure 1). \
                     If the water moves too quickly, '
                 'then rainwater will drain from the soil before plants can '
                 'drink it, and rivers and lakes will tend to dry up. If the '
                 'water moves too slowly, then rainwater will pool, which can '
                 'drown plants or cause landslides or flooding. As climate '
                 'change alters rates of rainfall in different regions, we '
                 'need to be able to predict what regions will have too much '
                 'or too little water in the soil.')
        st.markdown('Responding to these changes can be difficult because '
                 'different regions have different soils, which can let water '
                 'pass through them faster or slower (Figure 2). Temperate regions '
                 'tend to have dense soils that retain water long, while arid '
                 'regions often have grainy soils that drain water quickly. '
                 'Responding to climate change in these regions should look '
                 'different too!')
    with col2:
        st.image('images\SketchRegion2.png')
        myCaption('<b>Figure 1</b>: Soils in different regions can drain water at '
                 'different speeds. This means that soils can be too wet or '
                 'too dry for plants')
        st.image('images\MapRetention.png')
        myCaption('<b>Figure 2</b>: Map of soil types across USA. Colors represent \
                 changes in soil water retention (adapted from Gleeson \
                <i>et al.</i> Geophysical Research Letters 38(2) 2011.')  
    # col1,col2=st.beta_columns((1,1))
    # with col1:    
        
    # with col2:
        
    st.header('How permeability is measured')
    col1, col2 = st.beta_columns((1,1))
    with col1:
        st.markdown('To better understand what regions need '
                 'special attention to maintain water health, scientists '
                 'quantify this speed with a number called **permeability**. \
                     '
                 'Soils that let water flow quickly have a high permeability, '
                 'while soils that retain water for a long time have a low '
                 'permeability.')
        st.markdown('Permeability is given the symbol $k$. A typical soil can \
                    have a permeability somewhere in the range of \
                    $k=10^{-17}~$ to $~10^{-10}~\mathrm{m^2}$. \
                    To make these numbers look a little nicer, \
                    we can instead define the **retention**:')
        st.markdown('$~~~~~\mathrm{retention}=pk=-\mathrm{log}(k)$')
        st.markdown('Typical soils have retentions of $pk=10~$ to $17~$ (Figure 2). \
                    Loose soils like gravel are very permeable to water, \
                    and will retain water very poorly with $pk=7$. \
                    Denser soils like mud are much less water permeabile, and \
                    have high water retenions like $pk=16$.')
        st.markdown('Scientists can measure this using a device '
                 'called a **permability-meter** (or a **permeameter**, Figure 3), '
                 'allowing them to construct maps of soil permeability '
                 'and better plan for climate changes. \
                 A simple permeability-meter works by holding a set amount of \
                 soil, and watching the speed that water drains from it. \
                 By building your own permeability-meter, you can see how \
                 this speed is measured, and how it is used to compute the \
                 permeability $k$ and the retention $pk$!')
        
        
    with col2:
        st.image('images\PicRealPermeameter.png',width=300)
        myCaption('<b>Figure 3</b>: A research-grade permeameter. Image from groundtest.co.nz')
        st.image('images\SketchBasicPermeameter.png')
        myCaption('<b>Figure 4</b>: Schematic of a permeability-meter \
                  (falling head permeameter) works by measuring the speed that \
                  water flows through a soil sample.')
        
    st.header('Build your own DIY permeability-meter!')
    col1,col2=st.beta_columns((1,1))
    with col1:
        st.write('Our goal is to build a simple DIY experimental setup '
                 'to measure how quickly water moves through different soils. '
                 'By exploring different soils around your home, we can '
                 'investigate how rainwater is retained or lost, and predict '
                 'how this will influence plant health, flooding, and the '
                 'spreading of human contaminants through the environment. If '
                 'you measure the permeability of some soils near your home, '
                 'you can upload your findings to our database, and be a part '
                 'of building a more refined map of soil permeability in your '
                 'area!')
    with col2:
        st.image('images\PicWorking.jpg')
        myCaption('<b>Figure 5</b>: A DIY permeability-meter you can build at home!')
        



    