import streamlit as st

st.set_page_config(page_title="DataSUS", page_icon="🦠")

pages = {
    "Insights": [
        st.Page("src/views/serie_completa.py", title="Comparações entre Doenças", icon='📈'),
        st.Page("src/views/plot_sazonal.py", title="Plots Sazonais", icon='📉'),
        st.Page("src/views/serie_categoria.py", title="Comparações entre Valores de Categoria", icon='📊'),
        st.Page("src/views/decomposicao.py", title="Decomposição das Séries", icon='📈'),
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
    st.page_link(pages['Insights'][3])
    
    st.sidebar.title("Sobre")
    st.sidebar.info(
        """
        O DataSUS é o departamento de informática do Sistema Único de Saúde (SUS), responsável por fornecer sistemas de informação e suporte tecnológico que auxiliam no planejamento, operação e controle das ações de saúde pública. Entre seus serviços, destaca-se o TABNET, uma plataforma que disponibiliza dados cruciais para análises da situação de saúde, tomadas de decisão baseadas em evidências e a formulação de políticas públicas.
        Este aplicativo fornece insights e visualizações para dados de séries temporais relacionados a várias doenças.
        Você pode explorar diferentes comparações e gráficos sazonais para obter uma melhor compreensão das tendências e padrões.
        """
    )
