from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import subprocess
import time

"""
# Welcome to AI Singer Corner!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
def seperate_vocal(files):
    #seperate files to vocal and bgm
    return vocal, bgm
col_1, col_2 = st.columns(2, gap="large")
with col_1:
    st.subheader("📁Select Files")
    files = st.file_uploader("", type=["mp3","mp4","wav",])#, accept_multiple_files=True)
    print(files)
    file_upload_status = st.empty()

with col_2:
    if files is not None:
        # Translation Settings
        #files.name is e.g. identity.wav
        with st.form("Settings"):
            job_name = st.text_input( #e.g. identityout
                'Name Your Output', value=f"{files.name.split('.')[0]}out")
            # source_lang = st.selectbox("Source Language", options=[
            #     "English", "Chinese (Traditional)", "Chinese (Simplified)"])
            voice = st.selectbox("Whose Voice", options=[
                "Yoasobi", "Imagine Dragons",])
            

            btn_Compose = st.form_submit_button(label="Compose")

        progress_bar = st.progress(0)

        # File Upload
        if btn_Compose:
            # blank name is not allowed
            if not job_name: 
                st.error("Please type output file name")
                st.stop()
            
            #preprocessing input music

            #save upload music temperily 
            with open(files.name,'wb') as f:
                f.write(files.getbuffer())
            #infer the music with selected voice
            #now only use my voice 
            model = 'G_1640.pth'
            singer = 'canton'
            #command svc infer -o ./哪裏只得/vocals.out_2.wav -m G_1640.pth -s canton -c config.json -fm crepe -d cpu -t -3 哪裏只得/vocals.wav
            start = time.time()
            st.write(f'Infer start: {time.asctime((time.localtime(start)))}')
            # try: #try to use gpu if exist
            #     ls_process = subprocess.Popen(#["pwd"],
            #                             ["svc", "infer", "-o",f"{job_name}.wav",
            #                             "-m", f"models/{model}", '-s', singer, 
            #                             '-c', 'models/config.json', 
            #                             '-fm', 'crepe', 
            #                             f"{files.name}"], 
            #                             stdout=subprocess.PIPE, text=True)
            #     open(f"{job_name}.wav", "rb") # check if infer successfully done
            #except: # use cpu
            ls_process = subprocess.Popen(#["pwd"],
                        ["svc", "infer", "-o",f"{job_name}.wav",
                        "-m", f"models/{model}", '-s', singer, 
                        '-c', 'models/config.json', 
                        '-fm', 'crepe', '-d', 'cpu' ,
                        f"{files.name}"], 
                        stdout=subprocess.PIPE, text=True)
            st.write(ls_process)
            out,error = ls_process.communicate()
            st.write(out)
            st.write(f'Duration: {time.time() - start }')
            st.write(error)
            #play music
            
            #download music
            with open(f"{job_name}.wav", "rb") as file:
                btn_download = st.download_button(
                        label="Download AI voice",
                        data=file,
                        file_name=f"{job_name}.wav",
                        
                    )

            # same source and target lang not allowed
            # if source_lang == target_lang: 
            #     st.error("Please make sure source language and target language are different")
            #     st.stop()
            # files_total = len(files)
            # file_count = 0
            # if len(set([file.type for file in files])) != 1:
            #     st.error("Please make sure all files uploaded are same file type")
            #     st.stop()
            # for file in files:

            #     file_name = file.name
            #     file_id = file.id
            #     # show uploaded file details Debug
            #     file_details = {"Filename":file_name,"FileType":file.type,"FileSize":file.size}
            #     #st.write(file_details)
                
            #     with st.spinner("Submitting..."):
            #         progress_bar.progress(50)

            #         progress_bar.progress(100)

                    

            #     file_upload_status.info(
            #         f" File {file_count} of {files_total} submitted for Translation")


    else:
        yoasobi = Image.open('images/yoasobi.png')
        imagine_dragons = Image.open('images/imagine_dragons.png')
        st.image(yoasobi, caption='Yoasobi - Idol')
        st.image(imagine_dragons, caption='Imagine Dragons - Believer')
