import streamlit as st

pages = {
    "Bases": [
        st.Page("pages/sinan.py", title="SINAN")
    ],
    "Insights": [
        st.Page("pages/insights.py", title="Insight 1")
    ]
}

pg = st.navigation(pages)
pg.run()