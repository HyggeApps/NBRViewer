import streamlit as st
import uuid

st.set_page_config(page_title="Gerador de Links", page_icon="🔗")

st.title("🔗 Teste de geração de links aleatórios")

BASE_URL = "https://nbrviewer-ebynf4piupeqipdew7egah.streamlit.app"  # seu app publicado

# Lê parâmetros da URL
qp = st.query_params()
if "id" in qp:
    id_val = qp['id'][0]
    # Mostra conteúdo específico se o id for exatamente 'xpto'
    if id_val == "d0c9ba68":
        st.success("🛡️ Você acessou o link secreto **xpto**!")
        st.info("Conteúdo especial: este é um teste que mostra algo diferente quando o id é 'xpto'.")
        # Pequeno toque visual para destacar o caso especial
        st.balloons()
    else:
        st.success(f"Você acessou o link com ID: **{id_val}**")
else:
    # Gera um link novo
    if st.button("Gerar novo link"):
        random_id = str(uuid.uuid4())[:8]  # gera ID curto
        link = f"{BASE_URL}/?id={random_id}"
        st.write("Link gerado, copie e abra em nova aba:")
        st.code(link, language="text")
