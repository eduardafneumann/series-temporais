import streamlit as st

pages = {
    "Insights": [
        st.Page("views/serie_completa.py", title="Comparações entre Doenças", icon='📈'),
        st.Page("views/plot_sazonal.py", title="Plots Sazonais", icon='📉'),
        st.Page("views/serie_categoria.py", title="Comparações entre Valores de Categoria", icon='📊'),
    ],
}

pg = st.navigation(pages, position="hidden")
pg.run()

with st.sidebar:
    st.image("images/logo-datasus.png", use_column_width=True)
    #st.title("DATASUS")
    st.page_link(pages['Insights'][0])
    st.page_link(pages['Insights'][1])
    st.page_link(pages['Insights'][2])
    