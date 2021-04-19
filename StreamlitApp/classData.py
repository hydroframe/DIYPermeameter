# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:40:24 2021

@author: chrst
"""
import streamlit as st
import altair as alt
import time
import math
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from myStreamlit import myCaption

def classData(cached_sets,cached_results):
    numSamples=len(cached_sets)
    # st.write(cached_sets)
    strList=[cached_sets[i]["Sample name"][0] for i in range(numSamples)]
    # st.write(strList)
    def linFunc(x,a):
        return a*x   
    ######### Physical Parameters ######### 
    visc=0.00089 #Pa*s
    rho=1000 #kg/m^3
    g=9.81 #m/s
    
    ######### Real ranges ###########
    # pK values (-log(k [m^2]))
    df_pK=pd.DataFrame({'name':['Gravel','Clean sand','Silty sand','Silt'],
                     'low':[7,9,10,12],
                     'high':[10,13,14,16]})
    # st.write(df_pK)
    
    ######### Site construction ######### 
    st.title('Compare soils')
    
    st.write('Use this page to compare multiple soil samples you collected '
             'on the previous page, download sample data, or upload '
             'previous soil samples. You can also use this to collect data '
             'across your classroom. Below ')
    
     
    st.header('Upload, download, or remove samples')
    ######### Upload file from csv ########
    # st.subheader('Upload from csv:')
    panel_upload=st.beta_expander("Upload from csv", expanded=False)
    with panel_upload:
        left, right = st.beta_columns(2)
        with left:
            upload_file = st.file_uploader("Choose a file")
            if upload_file is not None:
                df_upload = pd.read_csv(upload_file)
                # st.write(df_upload)
        with right:
            if upload_file is not None:
                sampleName=df_upload['Sample name'][0] #upload_file.name.split('.')[0]
                addSample=True
                if strList:
                    if sampleName in strList:
                        addSample=False
                if not addSample:
                    customSampleName = st.text_input('You already have a soil with the same name. Give \
                             this one a different name if you would like to \
                             still add it.')
                    if len(customSampleName)>0:
                        sampleName=customSampleName
                        df_upload['Sample name'][0]=customSampleName
                        st.write('New name:**'+customSampleName+'**')
                        addSample=True
                if strList:
                    if sampleName in strList:
                        addSample=False
                if addSample:
                    
                    # st.write(upload_file.name)
                    
                    # st.write(customSampleName)
                    
                        # st.write(df_upload)
                    df_main=pd.DataFrame({'Water height (cm)': df_upload['Water height (cm)'],
                                           'Time (s)': df_upload['Time (s)']})
                    height=df_upload['Sample height (cm)'][0]
                    st.write(pd.DataFrame({'Sample height (cm)': [height]}))
                    st.write(df_main)
                    # should_add_sample=st.button('Add sample')
                    # if should_add_sample:
                    cached_sets.append(df_upload)
                    upload_file=None
                            # should_add_sample=False
                            ### Hoang: I think I need some way to automatically rerun here ###
    
    ######### Data Downloading ######### 
    numSamples=len(cached_sets)
    strList=[cached_sets[i]["Sample name"][0] for i in range(numSamples)]
    panel_download=st.beta_expander("Download to csv", expanded=False)
    with panel_download:
        left, right=st.beta_columns(2)
        with left:
            st.subheader('Download to csv:')
        with right:
            for i in range(numSamples):
                desiredFileName=cached_sets[i]["Sample name"][0]+'.csv'
                df_export=cached_sets[i]
                csv = df_export.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}" download ="{desiredFileName}">'+cached_sets[i]["Sample name"][0]+': Download as a .csv file</a>'  
                st.markdown(href, unsafe_allow_html=True)       
                
    ######### Remove samples ######### 
    numSamples=len(cached_sets)
    strList=[cached_sets[i]["Sample name"][0] for i in range(numSamples)]
    panel_remove=st.beta_expander("Remove samples", expanded=False)
    with panel_remove:
        left, mid, right = st.beta_columns(3)
        with left:
            st.subheader('Remove samples:')                   
        with mid:
            st.write(' ')
            # removePoint=st.selectbox("Data point to remove", strList, key=0)
        with right:
            st.write(' ')
            st.write(' ')
            # should_remove_sample=st.button("Remove this sample")
            # if should_remove_sample:
            #     cache_record=cached_sets #record old cache
            #     for i in range(len(cached_sets)):
            #         cached_sets.pop() # clear old cache
            #     for i in range(len(cache_record)):
            #         st.write(cache_record[i]["sample name"][0])
            #         if cache_record[i]["sample name"][0] is not removePoint:
            #             cached_sets.append(cache_record[i]) # re-add everything from old cache to new cache except point marked for removal
            #     should_remove_sample=False
            should_clear_samples=st.button("Clear all samples")
            if should_clear_samples:
                for i in range(len(cached_sets)):
                    cached_sets.pop() # clear all samples   
                should_clear_samples=False
                ### Hoang: I think I need some way to automatically rerun here ###
    ######### Display samples ######### 
    numSamples=len(cached_sets)
    strList=[cached_sets[i]["Sample name"][0] for i in range(numSamples)]
    
    # cached_sets=cached_dataSets
    df_allSamples=pd.DataFrame({"Sample name":cached_sets[i]["Sample name"][0],
                           "Height (cm)":cached_sets[i]["Sample height (cm)"][0],
                           "Number of points":len(cached_sets[i]["Time (s)"])} 
                          for i in range(numSamples))
    st.header('Compare your samples')
    if not list(df_allSamples):
        st.write('Upload a sample or process the data using the **Process \
                 experiment data** tab')
    else:
        ######### Display data plots #########     
        ## Initialize figure
        maxH=0
        maxV=0
        for s in range(len(cached_results)):
            cached_results.pop()#clear results cache and re-fill in every time on this page
        
        ## Process, Save, and Plot data 
        fig, (ax1a, ax1b) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        for s in range(numSamples):
            heights=cached_sets[s]['Water height (cm)']
            times=cached_sets[s]['Time (s)']
            sampleHeight=cached_sets[i]["Sample height (cm)"][0]
            vels=[-(h2-h1)/(t2-t1) for h1,h2,t1,t2 in 
                  zip(heights[0:-1],heights[1::],times[0:-1],times[1::])]
            heightsAv=[(h1+h2)/2 for h1,h2 in zip(heights[1::],heights[0:-1])]
            
            maxH=max([maxH, max(heightsAv)])
            maxV=max([maxV, max(vels)])
            
            ax1a.scatter(x=heights,
                       y=times,
                       marker='o',label=cached_sets[s]['Sample name'][0])
            ax1b.scatter(x=heightsAv,
                       y=vels,
                       marker='o',label=cached_sets[s]['Sample name'][0])
            ## Curve fitting
            [mdl, mdlcov] = curve_fit(linFunc, heightsAv, vels) #units of s
            cached_results.append(pd.DataFrame({'Sample name': cached_sets[s]['Sample name'][0],
                                                'Permeability':mdl*visc*sampleHeight/100/rho/g,
                                                'Retention':-math.log10(mdl*visc/rho/g)}))
            # Plot fit
            linH=np.linspace(0, maxH)
            ax1b.plot(linH, linH*mdl, '--', linewidth=2)
        ## Format axes
        
        ax1a.set_xlabel('Water Height (cm)', fontsize=12)
        ax1a.set_ylabel('Time (s)', fontsize=12)
        ax1a.legend([cached_sets[i]['Sample name'][0]
                    for i in range(numSamples)],
                   fontsize=12 )
        ax1b.set_xlabel('Water Height (cm)', fontsize=12)
        ax1b.set_ylabel('Velocity (cm/s)', fontsize=12)
        ax1b.legend([cached_sets[i]['Sample name'][0]
                    for i in range(numSamples)],
                   fontsize=12 )
        ax1b.set_xlim([0, 1.1*maxH])
        ax1b.set_ylim([0, 1.1*maxV])
        
        # loosen subplot spacing
        plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.4)
        st.write(fig)
        
        
        
        listNames=[cached_results[i]['Sample name'][0] for i in range(numSamples)]
        listPerm=["{:.2e}".format(cached_results[i]['Permeability'][0]) for i in range(numSamples)]
        listRetention=["{:.2f}".format(cached_results[i]['Retention'][0]) for i in range(numSamples)]
        #########  Display permability results ######### 
        # leftB,colN,colP,colR,rightB=st.beta_columns((.5,1,1,1,.5))
        # with colN:
        #     st.subheader('Sample Name')
        #     for i in range(len(listNames)):
        #         st.write(listNames[i]) 
        # with colP:
        #     st.subheader('Permeability (m²)')
        #     for i in range(len(listNames)):
        #         st.write(listPerm[i]) 
        # with colR:
        #     st.subheader('Retention')
        #     for i in range(len(listNames)):
        #         st.write(listRetention[i]) 
        
        # Write data to table
        df_perms=pd.DataFrame({'Sample name': listNames,
                               'Permeability (m²)': listPerm,
                               'Retention':listRetention})  
        _,col,_=st.beta_columns((.2,1,.2))
        with col:
            st.write(df_perms)
            
        ## Compare to real soil distributions    
        st.header('Compare with real soils')
        col1,col2=st.beta_columns((1,1))
        with col1:
            st.markdown('A typical soil or gravel can \
                    have a permeability somewhere in the range of \
                    $k=10^{-17}~$ to $~10^{-7}~\mathrm{m^2}$ (Figure 1), \
                    or a retentions of $pk=7~$ to $17~$ (\
                    $pk=-\mathrm{log}(k)$). \
                    When looking at a map (Figure 1), it is usually convenient \
                    to separate soils into a few cateogories, so it is easier \
                    to talk about the water retention in different regions. \
                    Let''s see how your samples compare to these ranges:')
        with col2:
            st.image('images\MapRetention.png')
            myCaption('<b>Figure 1</b>: Map of soil types across USA. Colors represent \
                 changes in soil water retention (adapted from Gleeson \
                <i>et al.</i> Geophysical Research Letters 38(2) 2011.') 
        numReal=len(df_pK['low'])
        fig2, ax2 = plt.subplots(nrows=1, ncols=1, \
                         figsize=(8, len(df_pK['low'])*.5+numSamples*.5))
        for i in range(numReal):
            ax2.plot([df_pK['low'][i], df_pK['high'][i]],[-1-i, -1-i],'-', linewidth=4)
            plt.text(x=(df_pK['low'][i]+df_pK['high'][i])/2, y=-1-i, s=df_pK['name'][i], \
                  fontsize=12, horizontalalignment='center', \
                  verticalalignment='bottom')
        # plt.gca().set_prop_cycle(colors[numSamples-1:numReal-1])
                
        for i in range(numSamples):
            ax2.scatter(x=cached_results[i]['Retention'][0],y=-1-numReal-(i+1))
            plt.text(x=cached_results[i]['Retention'][0], y=-1-numReal-(i+1), \
                      s='  ' + listNames[i], \
                  fontsize=12, horizontalalignment='left', \
                  verticalalignment='center')
                
        plt.ylabel('')
        plt.yticks([], [])
        ax2.set_ylim([-len(df_pK['low'])-numSamples-1.5,0])
        ax2.set_xlabel('Retention', fontsize=12)
        # plt.xticks(np.linspace(0,20,5),np.linspace(0,20,5))
        # ax2.set_ylabel('Samples', fontsize=12)
        st.write(fig2)
        st.markdown('')