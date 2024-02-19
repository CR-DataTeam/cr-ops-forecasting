import streamlit as st
from streamlit.logger import get_logger
import helpers as h
import pandas as pd
from tempfile import NamedTemporaryFile

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

LOGGER = get_logger(__name__)

init_SL = 'CIS'

# Optional -- adds the title and icon to the current page
st.set_page_config(
     page_title=init_SL+ ' Review',
     layout="wide"
     )

forecast_list = ['Budget','01+11','02+10','03+09','04+08','05+07','06+06','07+05','08+04','09+03','10+02','11+01']
forecast_select = st.selectbox('Forecast Version', forecast_list, index=1)

subm_df = h.stored_GET_data(h.ssid_subm, 'All!A1:K')[0]
df = subm_df[(subm_df['ServiceLine']==init_SL) & (subm_df['Version']==forecast_select)]
df['url_o'] = df.SubmissionID.apply(lambda x: 'https://docs.google.com/spreadsheets/d/' + x + '/export?format=xlsx')
df['url_c'] = df.CleanCopyID.apply(lambda x: 'https://docs.google.com/spreadsheets/d/' + x + '/export?format=xlsx')
df['uname_c'] = df['SubmissionTitle'] + ' (clean)'
df['Download Original'] = df.apply(lambda x: make_clickable(x['url_o'], x['SubmissionTitle']), axis=1)
df['Download Clean'] = df.apply(lambda x: make_clickable(x['url_c'], x['uname_c']), axis=1)

col_order = ['ServiceLine', 'Version', 'Iteration', 'FunctionalArea','Submitter', 'SubmissionNotes','Timestamp', 'Download Original', 'Download Clean']
final_df = df[col_order]
final_df = final_df.sort_values('Iteration', ascending=False)

st.markdown(final_df.to_html(escape=False, index=False),unsafe_allow_html=True) 
######################
# st.markdown(""":red[January actuals not yet added.  
#             The file with actuals + the prior month forecast budget will appear here once ready.]""")
######################
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown("""
    ---
    :gray['**Original**' refers to the file as it was uploaded, with no changes made.  
    '**Clean**' refers to a version of the file with *only* the numbers included and all formulas stripped (except for the summary, those are automatically added).  
    Please refer to the Budget files for any of the Service Lines or the initial email sent out for an example.]""")