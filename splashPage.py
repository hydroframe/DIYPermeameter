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
    st.title('DIY soil flow-meter')
    st.markdown('This site helps you build your own do-it-yourself (DIY) **soil flow-meter** \
                 with materials around your home, and measure your soil''s \
                 **hydraulic conductivity** (how quickly water flows through the soil). \
                     You can also compare your soil samples to others, \
                     and attempt the **designer soil challenge**!')
    st.header('Why hydraulic conductivity matters:') 
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
                 'drown plants or cause landslides or flooding (Figure 2). As climate '
                 'change alters rates of rainfall in different regions, we '
                 'need to be able to predict what regions will have too much '
                 'or too little water in the soil.')
        st.markdown('Responding to these changes can be difficult because '
                 'different regions have different soils, which can let water '
                 'pass through them faster or slower (Figure 3). Though many \
                 other factors also contribute to the water content of an \
                 ecosystem (including rainfall, water resrvoirs like lakes \
                 and streams, and human interaction), \
                 you can see on the map that temperate regions '
                 'tend to have dense soils that retain water long, while arid '
                 'regions often have grainy soils that drain water quickly. '
                 'Responding to climate change in these regions should look '
                 'different too!')
    with col2:
        st.image('images/SketchRegion.png')
        myCaption('<b>Figure 1</b>: Soils in different regions can drain water at '
                 'different speeds. This means that soils can be too wet or '
                 'too dry for plants')
        st.image('images/Seesaw.png')
        myCaption('<b>Figure 2</b>: A soil with a high hydraulic conductivity \
                  drains quickly, and will tend to dry faster. A soil with a low \
                  hydraulic conductivity drains slowly, and will tend to stay \
                  wet longer')  
        st.image('images/MapConductivity.png')
        myCaption('<b>Figure 3</b>: Map of soil types across USA. Colors represent \
                 changes in soil hydraulic conductivity (adapted from Gleeson \
                <i>et al.</i> Geophysical Research Letters 38(2) 2011.')  
    # col1,col2=st.beta_columns((1,1))
    # with col1:    
        
    # with col2:
        
    st.header('How hydraulic conductivity is measured')
    col1, col2 = st.beta_columns((1,1))
    with col1:
        st.markdown('To better understand what regions need \
                 special attention to maintain water health, scientists \
                 quantify this speed with a number called **hydraulic conductivity**. \
                 Soils that let water flow quickly have a high conductivity, \
                 while soils that retain water for a long time have a low \
                 conductivity (Figure 2).')
        st.markdown('Hydraulic conductivity is given the symbol $K$. A typical soil can \
                    might have a conductivity of \
                    $K=1$ cm/min: this value is *roughly* the speed of draining water, \
                    or the distance water will travel in a given time. \
                    You''ll see later in your experiment how this conductivity \
                    isn''t exactly the speed of water: the real speed will also \
                    depend on the amount of water gravity is pulling down through the soil.')
        st.markdown('\
                    Real soils can have a huge range of hydraulic conductivities.\
                    A man-made gravel may have a conductivity of up to 1000 cm/min, \
                    while a really dense clay may have a conductivity as low as \
                    $.0001$ cm/min: that''s closer to 1 mm every year!')
        st.markdown('Scientists studying water flow in the environment (**hydrologists**) \
                    can measure hydraulic conductivity using a device \
                 called a **soil flow-meter** (or more commonly called a \
                 **falling head permeameter**, Figure 4). The device lets water \
                 of height $L$ drain through a soil sample of height $h$, \
                 and records the speed $U$ of this drainage. S\
                 they can measure the hydraulic conductivity $K$ using a formula \
                     called Darcy''s law, which describes how fluids move through rocks and soils:')
        st.latex('U=K(h/L)')
        st.markdown('By measuring soils in different places, they can construct \
                 maps of soil conductivity (like Figure 3) \
                 and better plan for climate changes. \
                 A simple soil flow-meter works by holding a set amount of \
                 soil, and watching the speed that water drains from it. \
                 By building your own soil flow-meter, you can see how \
                 this speed is measured, and how it is used to compute the \
                 hydraulic conductivity $K$ and compare it to other soils!')
        
        
    with col2:
        st.image('images/PicRealPermeameter.png',width=300)
        myCaption('<b>Figure 4</b>: A research-grade flow-meter \
                  (falling head permeameter). Image from groundtest.co.nz')
        st.image('images/SketchBasicPermeameter.png')
        myCaption('<b>Figure 5</b>: Schematic of a soil flow-meter, which \
                  works by measuring the speed that \
                  water flows through a soil sample.')
        
    st.header('Build your own DIY soil flow-meter!')
    col1,col2=st.beta_columns((1,1))
    with col1:
        st.write('Our goal is to build a simple DIY experimental setup '
                 'to measure how quickly water moves through different soils (Figure 6). '
                 'By exploring different soils around your home, we can '
                 'investigate how rainwater is retained or lost, and predict '
                 'how this will influence plant health, flooding, and the '
                 'spreading of human contaminants through the environment. If '
                 'you measure the hydraulic conductivity of some soils near your home, '
                 'and compare them to other soils!')
    with col2:
        st.image('images/PicWorking.jpg')
        myCaption('<b>Figure 6</b>: A DIY soil flow-meter you can build at home!')
        



    