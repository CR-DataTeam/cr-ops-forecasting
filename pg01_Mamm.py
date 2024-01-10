import streamlit as st
from streamlit.logger import get_logger
import helpers as h
import pandas as pd
from tempfile import NamedTemporaryFile

LOGGER = get_logger(__name__)

# Optional -- adds the title and icon to the current page
st.set_page_config(
     page_title="Mamm History",
     layout="wide"
     )

forecast_list = ['Forecast Version','00+12','01+11','02+10','03+09','04+08','05+07','06+06','07+05','08+04','09+03','10+02','11+01']
forecast_select = st.selectbox('Forecast Version', forecast_list, index=1)

subm_df = h.stored_GET_data(h.ssid_subm, 'All!A1:K')[0]
df = subm_df[(subm_df['ServiceLine']=='Mamm') & (subm_df['Version']==forecast_select)]
df