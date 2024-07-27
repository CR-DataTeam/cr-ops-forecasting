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
import helpers as h
import pandas as pd
from tempfile import NamedTemporaryFile

LOGGER = get_logger(__name__)

pg = st.navigation({
    "Submit Files": [
        st.Page('pg00_submitform.py', title="Submission Form", default=True, icon="📁"),
        ],
    "Review Forecasts": [
        st.Page('pg01_Mamm.py', title="Mamm Forecast Files", icon="🏥"),
        st.Page('pg02_CIS.py',  title="CIS Forecast Files",  icon="🏥"),
        st.Page('pg03_Vein.py', title="Vein Forecast Files", icon="🏥"),
        ],
})
pg.run()