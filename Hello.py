# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from st_pages import Page, show_pages, add_page_title
import helpers as h
import pandas as pd
from tempfile import NamedTemporaryFile

LOGGER = get_logger(__name__)

# Optional -- adds the title and icon to the current page
st.set_page_config(
     page_title="Forecasting Tool",
     # layout="wide"
     )

# add_page_title()

show_pages(
    [
        Page("Hello.py", "Submit File"),
        Page("pg01_Mamm.py", "Mamm Review"),
        Page("pg02_CIS.py",  "CIS Review" ),
        Page("pg03_Vein.py", "Vein Review"),
    ]
)



st.write("# Forecasting Tool")

col1, col2, col3 = st.columns([.25,1,.25])

servline_list = ['Mamm','CIS','Vein']
forecast_list = ['Budget','01+11','02+10','03+09','04+08','05+07','06+06','07+05','08+04','09+03','10+02','11+01']
fxarea_list   = ['Ops', 'Finance', 'Marketing', 'Other']
with col2:
    with st.form("my_form"):  # , clear_on_submit=True):
        servline_select = st.selectbox('Service Line', servline_list)  # , index=None)
        forecast_select = st.selectbox('Forecast Version', forecast_list)  # , index=None)
        fxarea_select   = st.selectbox('Functional Area', fxarea_list)  # , index=None)
        editor_entry    = st.text_input('Name')
        note_entry      = st.text_input('Submission Note')
        uploaded_file   = st.file_uploader("Upload File")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

facilities = {
    'Mamm': ['Ballantyne', 'Blakeney', 'Huntersville', 'Matthews',
        'McDowell', 'MCP', 'MMP', 'Mobile', 'Monroe', 'Mooresville', 
        'Pineville', 'Prosperity', 'Rock Hill', 'Rosedale', 'Southpark', 
        'Steele Creek', 'Union West', 'University'], 
    'CIS': ['Ballantyne', 'Denver', 'Huntersville', 'Matthews',
        'Rock Hill', 'Southpark'], 
    'Vein': ['Huntersville', 'Southpark']
}




if submitted:
    if servline_select is not None and forecast_select is not None and fxarea_select is not None and editor_entry is not None and uploaded_file is not None:
        input_validity = True
    else:
        input_validity = False
        st.warning('Please fill out form.')

    if input_validity:
        facility_list = facilities[servline_select]

        itnum = h.get_iteration(servline_select,forecast_select)+1
        filenum = h.number_naming_convention(itnum)
        filename = filenum + ' - ' + servline_select + ' - ' + forecast_select + \
                    ' - ' + fxarea_select + ' - ' + h.today_string_file()
        
        df_dict = h.excel_reader_get_data(uploaded_file, facility_list, servline_select)
        upfileid = h.upload_file_to_drive(uploaded_file, filename+'.xlsx')
        cleanfileid = h.create_clean_copy(filename, df_dict, facility_list, servline_select)
        h.final_combine_and_store_all_facilities(df_dict, facility_list, upfileid, servline_select, forecast_select, itnum)
        upload_metadata = {'ServiceLine':servline_select, 
                'Year':2024,
                'Version':forecast_select,
                'FunctionalArea':fxarea_select,
                'Submitter':editor_entry,
                'SubmissionNotes':note_entry,
                'Timestamp':h.today_string(),
                'SubmissionID':upfileid,
                'SubmissionTitle':filename,
                'Iteration':itnum,
                'CleanCopyID':cleanfileid,
                }
        h.add_submission_line(upload_metadata) 
        st.success('File uploaded successfully.')
st.markdown('After submitting, please wait until a green message stating "File uploaded successfully." appears on your screen before doing anything else. The upload itself can take anywhere from 5-20 seconds, I apologize for the delay.')
        
    
