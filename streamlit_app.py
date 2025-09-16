import streamlit as st
import uuid

st.set_page_config(page_title="Gerador de Links", page_icon="🔗")

st.title("🔗 Teste de geração de links aleatórios")

BASE_URL = "https://nbrviewer-ebynf4piupeqipdew7egah.streamlit.app"  # seu app publicado

# Lê parâmetros da URL
qp = st.query_params()
if "id" in qp:
    st.success(f"Você acessou o link com ID: **{qp['id'][0]}**")
else:
    # Gera um link novo
    if st.button("Gerar novo link"):
        random_id = str(uuid.uuid4())[:8]  # gera ID curto
        link = f"{BASE_URL}/?id={random_id}"
        st.write("Link gerado, copie e abra em nova aba:")
        st.code(link, language="text")
