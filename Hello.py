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
from st_pages import Page, show_pages
import helpers as h
import pandas as pd
from tempfile import NamedTemporaryFile

LOGGER = get_logger(__name__)

show_pages(
    [
        Page("Hello.py", "Submit File"),
        Page("pages/01_Mamm.py", "Mamm Review"),
        Page("pages/02_CIS.py",  "CIS Review" ),
        Page("pages/03_Vein.py", "Vein Review"),
    ]
)

# Optional -- adds the title and icon to the current page
st.set_page_config(
     page_title="Forecasting Tool",
     layout="wide"
     )

st.write("# Forecasting Tool")

col1, col2, col3 = st.columns([.25,1,.25])

servline_list = ['Service Line','Mamm','CIS','Vein']
forecast_list = ['Forecast Version','00+12','01+11','02+10','03+09','04+08','05+07','06+06','07+05','08+04','09+03','10+02','11+01']
fxarea_list   = ['Functional Area', 'Ops', 'Finance', 'Marketing', 'Other']
with col2:
    with st.form("my_form", clear_on_submit=True):
        servline_select = st.selectbox('Service Line', servline_list)
        forecast_select = st.selectbox('Forecast Version', forecast_list)
        fxarea_select   = st.selectbox('Functional Area', fxarea_list)
        editor_entry    = st.text_input('Name')
        note_entry      = st.text_input('Submission Note')
        uploaded_file   = st.file_uploader("Upload File")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

fl = ['Ballantyne', 'Blakeney', 'Huntersville', 'Matthews',
        'McDowell', 'MCP', 'MMP', 'Mobile', 'Monroe', 'Mooresville', 
        'Pineville', 'Prosperity', 'Rock Hill', 'Rosedale', 'Southpark', 
        'Steele Creek', 'Union West', 'University']



if uploaded_file is not None:

    # data = h.excel_reader_get_data('Mamm 2024 Initial Load.xlsx', fl)
    # new = h.reformat_add_df_context(df,'Ballantyne','asdfasdfasdf')
    # h.stored_APPEND_data(h.ssid_full,'Mamm!A:P',h.excel_storage_conversion(new))
    asdf = {'serv':servline_select, 'fileid':upfileid}
    sdf = pd.DataFrame(asdf)

    upfileid = h.upload_file_to_drive(uploaded_file, 'form_test.xlsx')
    sdf['servline'] = servline_select
    sdf['fileid'] = upfileid
    sdf

    st.write(upfileid)
    
