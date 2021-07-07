# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from MultiApp2 import MultiApp
import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
def dataEntry():
    ## Header instructions
    st.title('Soda bottle permeameter')
    st.markdown('This online tool helps you process data from your \
                **Soda bottle permeameter** experiment. \
                Enter your data below to learn the \
                    hydraulic conductivity of your soil sample!')
    
    ## Data entry
    st.header('Enter your data')
    sampleHeightText = st.text_input("Enter height of your soil sample")
    sampleHeightTextSplit = sampleHeightText
    waterHeightText = st.text_input("Enter list of water heights")
    waterHeightTextSplit = waterHeightText.replace(',',' ').split()
    lengthOption=st.radio("units", ('centimeters','inches'))
    timePointsText = st.text_input("Enter list of times")
    timePointsTextSplit = timePointsText.replace(',',' ').split()
    timeOption=st.radio("units", ("seconds","minutes"))
     
    ## Get lengths of inputs for easy code analysis
    numH = len(waterHeightTextSplit)
    numT = len(timePointsTextSplit)
    numS = len(sampleHeightTextSplit)
    
    
    if numH > 1 and numH == numT and numS == 1:
        st.header('See how your data is processed')
        
        ## Unit conversions
        if lengthOption=='centimeters':
            lengthConv=1.0
            lengthAbv='cm'
        elif lengthOption=='inches':
            lengthConv=2.54
            lengthAbv='in'
            
        if timeOption=="seconds":
            timeConv=1.0
            timeAbv='s'
        elif timeOption=="minutes":
            timeConv=60.0
            timeAbv='min'
            
        ## String to float conversions    
        sampleHeight=float(sampleHeightTextSplit)
        sampleHeightSI=sampleHeight*lengthConv    
        waterHeight = [float(item) for item in waterHeightTextSplit]
        waterHeightSI=[i*lengthConv for i in waterHeight]
        timePoints = [float(item) for item in timePointsTextSplit]
        timePointsSI= [timeConv*i for i in timePoints]  
        
        
        
        
        
        ## Conversions
        avHeight=[(waterHeightSI[i]+waterHeightSI[i+1])/2 for i in range(numH-1)]
        avVel=[-(waterHeightSI[i]-waterHeightSI[i+1])/(timePointsSI[i]-timePointsSI[i+1]) for i in range(numH-1)]
    
        ## Curve fitting
        def linFunc(x,a):
            return a*x    
        mdl, mdlcov = curve_fit(linFunc, avVel, avHeight) #units of s
        # st.write(mdl)
        
        ## Compute Hydraulic conductivity
        hydCond=sampleHeightSI/mdl #units of cm/s
    
        
        def animate(ax,i,listX,listY):  ## update the y values (every 1000ms)
            ax.line.set_xdata(listX)
            ax.line.set_ydata(listY)
            the_plot.pyplot(plt)    
            
        
        ## Make figure and format appearance
        fig2, (ax0,ax1) = plt.subplots(1,2,figsize=(6, 2))
        plt.subplots_adjust(wspace=.2)
        ax0.set_xlabel("Time ("+timeAbv+")", fontsize=12)
        ax0.set_ylabel("Height ("+lengthAbv+")", fontsize=12)
        ax0.set_xlim(0, math.ceil(max(timePoints)*1.1))
        ax0.set_ylim(0, math.ceil(max(waterHeight)*1.1))
        ax0.line, = ax0.plot(timePoints,np.empty(len(waterHeight))+np.NaN,'o')
        
        # ax1.set_ylabel("Pressure Head ("+lengthAbv+")", fontsize=12)
        ax1.set_xlabel("Velocity ("+lengthAbv+"/"+timeAbv+")", fontsize=12)
        ax1.set_xlim(0, math.ceil(max(avVel)*1.1*10)/10)
        # ax1.set_ylim(0, math.ceil(max(avHeight)*1.1*10)/10)
        ax1.set_ylim(0, math.ceil(max(waterHeight)*1.1))
        ax1.line, = ax1.plot(avVel, np.empty(len(avHeight))+np.NaN,'o')
        
        ## Plot everything initially
        the_plot = st.pyplot(plt)
        
        ## hide everything
        # init(ax0)
        # init(ax1)
        
        ## Animate data entry
        animate(ax0,1,timePoints[0],waterHeight[0])
        for i in range(1,numH+1):
            animate(ax0,i,timePoints[0:i],waterHeight[0:i])
            animate(ax1,i,avVel[0:i-1],avHeight[0:i-1])
            # time.sleep(0.001)
        xArray = np.linspace(0,math.ceil(max(avVel)*1.1*10)/10)
        ax1.plot(xArray,linFunc(xArray,mdl),'--')
        the_plot.pyplot(plt)
        st.header('Conductivity of your sample')
        st.markdown('Your hydraulic conductivity is %.3f ' % hydCond +lengthAbv + '/' +timeAbv)    
        return (sampleHeight, waterHeight, timePoints,lengthOption,timeOption)
    else:
        if numH<2:
            st.write('You need at least two data points so we can see how fast the water is moving.')
        elif numH != numT:
            st.write('Every "water height" needs a "time" to go with it.')
        if numS>1:
            st.write('Only give one number for your sample height.')
        elif numS<1:
            st.write('Specify the sample height.')
            
            # Add better descriptiors
def dataView(sampleHeight, waterHeight, timePoints,lengthOption,timeOption):
    st.title("Let's get it!!")
    st.header('See how your data is processed')
    ## Unit conversions
    if lengthOption=='centimeters':
        lengthConv=1.0
        lengthAbv='cm'
    elif lengthOption=='inches':
        lengthConv=2.54
        lengthAbv='in'
        
    if timeOption=="seconds":
        timeConv=1.0
        timeAbv='s'
    elif timeOption=="minutes":
        timeConv=60.0
        timeAbv='min'
    
    ## String to float conversions    
    
    sampleHeightSI=sampleHeight*lengthConv    
    waterHeightSI=[i*lengthConv for i in waterHeight]
    timePointsSI= [timeConv*i for i in timePoints]  
    
    numH = len(waterHeightSI)
    numT = len(timePointsSI)
    numS = len(sampleHeightSI)
    
    ## Conversions
    avHeight=[(waterHeightSI[i]+waterHeightSI[i+1])/2 for i in range(numH-1)]
    avVel=[-(waterHeightSI[i]-waterHeightSI[i+1])/(timePointsSI[i]-timePointsSI[i+1]) for i in range(numH-1)]

    ## Curve fitting
    def linFunc(x,a):
        return a*x    
    mdl, mdlcov = curve_fit(linFunc, avVel, avHeight) #units of s
    # st.write(mdl)
    
    ## Compute Hydraulic conductivity
    hydCond=sampleHeightSI/mdl #units of cm/s

    
    def animate(ax,i,listX,listY):  ## update the y values (every 1000ms)
        ax.line.set_xdata(listX)
        ax.line.set_ydata(listY)
        the_plot.pyplot(plt)    
        
    
    ## Make figure and format appearance
    fig2, (ax0,ax1) = plt.subplots(1,2,figsize=(6, 2))
    plt.subplots_adjust(wspace=.2)
    ax0.set_xlabel("Time ("+timeAbv+")", fontsize=12)
    ax0.set_ylabel("Height ("+lengthAbv+")", fontsize=12)
    ax0.set_xlim(0, math.ceil(max(timePoints)*1.1))
    ax0.set_ylim(0, math.ceil(max(waterHeight)*1.1))
    ax0.line, = ax0.plot(timePoints,np.empty(len(waterHeight))+np.NaN,'o')
    
    # ax1.set_ylabel("Pressure Head ("+lengthAbv+")", fontsize=12)
    ax1.set_xlabel("Velocity ("+lengthAbv+"/"+timeAbv+")", fontsize=12)
    ax1.set_xlim(0, math.ceil(max(avVel)*1.1*10)/10)
    # ax1.set_ylim(0, math.ceil(max(avHeight)*1.1*10)/10)
    ax1.set_ylim(0, math.ceil(max(waterHeight)*1.1))
    ax1.line, = ax1.plot(avVel, np.empty(len(avHeight))+np.NaN,'o')
    
    ## Plot everything initially
    the_plot = st.pyplot(plt)
    
    ## hide everything
    # init(ax0)
    # init(ax1)
    
    ## Animate data entry
    animate(ax0,1,timePoints[0],waterHeight[0])
    for i in range(1,numH+1):
        animate(ax0,i,timePoints[0:i],waterHeight[0:i])
        animate(ax1,i,avVel[0:i-1],avHeight[0:i-1])
        # time.sleep(0.001)
    xArray = np.linspace(0,math.ceil(max(avVel)*1.1*10)/10)
    ax1.plot(xArray,linFunc(xArray,mdl),'--')
    the_plot.pyplot(plt)
    st.header('Conductivity of your sample')
    st.markdown('Your hydraulic conductivity is %.3f ' % hydCond +lengthAbv + '/' +timeAbv)    
    

app = MultiApp()
app.add_app("Enter Data", dataEntry)
app.add_app("View Data", dataView)
app.run()    




# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")