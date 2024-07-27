# streamlit_app.py
import streamlit as st

pg = st.navigation({
    "Submit Files": [
        st.Page('Hello.py', title="Submission Form", default=True, icon="📁"),
        ],
    "Review Forecasts": [
        st.Page('pg01_Mamm.py', title="Mamm Forecast Files", icon="🏥"),
        st.Page('pg02_CIS.py',  title="CIS Forecast Files",  icon="🏥"),
        st.Page('pg03_Vein.py', title="Vein Forecast Files", icon="🏥"),
        ],
})
pg.run()