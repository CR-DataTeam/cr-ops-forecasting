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
import random
import pandas as pd

LOGGER = get_logger(__name__)

# Optional -- adds the title and icon to the current page
st.set_page_config(
     page_title="Forecasting Tool",
     layout="wide"
     )

st.write("# Forecasting Tool")

col1, col2, col3 = st.columns([.25,1,.25])

servline_list = ['Service Line','Mamm','CIS','Vein']
forecast_list = ['Forecast Version','0+12','1+11','2+10','3+9','4+8','5+7','6+6','7+5','8+4','9+3','10+2','11+1']
fxarea_list = ['Functional Area', 'Ops', 'Finance', 'Marketing', 'Other']
with col2:
    with st.form("my_form"):
        fxarea_select     = st.selectbox('Functional Area', fxarea_list)
        servline_select = st.selectbox('Service Line', servline_list)
        forecast_select = st.selectbox('Forecast Version', forecast_list)
        editor_entry = st.text_input('Name')
        note_entry   = st.text_input('Submission Note')
        uploaded_file = st.file_uploader("Upload File")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")



col1b, col2b, col3b = st.columns(3)

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
      forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
      Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)


