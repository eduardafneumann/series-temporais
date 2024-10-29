import streamlit as st

pages = {
    "Bases": [
        #st.Page("views/bases/sih.py", title="SIH"),
        #st.Page("views/bases/sim.py", title="SIM"),
        st.Page("views/bases/sinan.py", title="SINAN", icon='🦠')
    ],
    "Insights": [
        st.Page("views/insights.py", title="Insight 1"),
        st.Page("views/insights.py", title="Insight 2", url_path='i'),
        st.Page("views/insights.py", title="Insight 3", url_path='i2'),
    ],
}

pg = st.navigation(pages, position="hidden")
pg.run()

with st.sidebar:
    st.image("images/logo-datasus.png", use_column_width=True)
    #st.title("DATASUS")
    st.page_link(pages['Bases'][0])
    st.page_link(pages['Insights'][0])