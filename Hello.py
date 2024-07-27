# ! main module

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