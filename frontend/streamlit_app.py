import streamlit as st

pages = {
    "Bases": [
        #st.Page("pages/bases/sih.py", title="SIH"),
        #st.Page("pages/bases/sim.py", title="SIM"),
        st.Page("pages/bases/sinan.py", title="SINAN")
    ],
    "Insights": [
        st.Page("pages/insights.py", title="Insight 1"),
        st.Page("pages/insights.py", title="Insight 2", url_path='i'),
        st.Page("pages/insights.py", title="Insight 3", url_path='i2'),
    ],
}

pg = st.navigation(pages)
pg.run()