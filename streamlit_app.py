import streamlit as st
import uuid

st.set_page_config(page_title="Gerador de Links", page_icon="🔗")

st.title("🔗 Teste de geração de links aleatórios")

BASE_URL = "https://nbrviewer-ebynf4piupeqipdew7egah.streamlit.app"  # seu app publicado

# Lê parâmetros da URL (compat: não chame a QueryParamsProxy como função)
if hasattr(st, "query_params"):
    # Em versões recentes, `st.query_params` é uma propriedade/objeto (QueryParamsProxy)
    # que não é chamável. Se por acaso for uma função, chamamos; caso contrário, usamos direto.
    qp_attr = st.query_params
    qp = qp_attr() if callable(qp_attr) else qp_attr
elif hasattr(st, "get_query_params"):
    qp = st.get_query_params()
elif hasattr(st, "experimental_get_query_params"):
    qp = st.experimental_get_query_params()
else:
    qp = {}

if "id" in qp:
    id_val = qp['id']
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
