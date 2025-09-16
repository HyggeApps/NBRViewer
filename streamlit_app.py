# streamlit_app.py
import streamlit as st
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from urllib.parse import urlencode

st.set_page_config(page_title="Visualizador de Resultados (exemplo sem DB)", layout="wide")

# ---------- CONFIGURAÇÃO (troque a chave em produção usando Streamlit Secrets) ----------
DEFAULT_JWT_SECRET = "troque_esta_chave_em_producao_por_um_valor_MUITO_longo"
JWT_SECRET = st.secrets.get("jwt_secret", DEFAULT_JWT_SECRET) if "secrets" in st.__dict__ else DEFAULT_JWT_SECRET
BASE_URL = st.secrets.get("base_url", "http://localhost:8501") if "secrets" in st.__dict__ else "http://localhost:8501"
# ---------------------------------------------------------------------------------------

st.title("📊 Visualizador de Resultados — Demo sem banco")

st.markdown(
    "Este demo **gera links assinados** (`?t=<token>`) que carregam todo o resultado dentro do token. "
    "Útil para compartilhar sem precisar de banco de dados."
)

# ----------------- Pequena base de exemplos (models embutidos) -----------------
EXAMPLE_RESULTS = {
    "RES-EX-001": {
        "result_id": "RES-EX-001",
        "client_name": "Construtora Exemplo S.A.",
        "title": "Diagnóstico Rápido — Empreendimento Alfa",
        "summary": "Resumo executivo: unidades tipo 1 atendem; sugestão de melhoria nas fachadas.",
        "metrics": {
            "sDA_300_50 (%)": 63.2,
            "ASE_1000_250 (%)": 7.1,
            "U_wall (W/m²K)": 2.35,
            "SHGC_glazing": 0.32
        },
        "tables": [
            {
                "title": "Resultados por Tipologia",
                "columns": ["Tipologia", "sDA300/50", "ASE1000/250", "Status"],
                "rows": [
                    ["T01", 62.1, 8.4, "OK"],
                    ["T02", 65.9, 6.8, "OK"],
                    ["T03", 58.5, 10.2, "Rever"]
                ]
            }
        ],
        "assets": {
            "images": [
                {"label": "Mapa sDA (exemplo)", "url": "https://via.placeholder.com/1000x400.png?text=Mapa+sDA"},
                {"label": "Mapa ASE (exemplo)", "url": "https://via.placeholder.com/1000x400.png?text=Mapa+ASE"}
            ],
            "pdfs": [
                {"label": "Relatório resumido (PDF)", "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
            ]
        },
        "created_at": "2025-09-16T00:00:00Z"
    },

    "RES-EX-002": {
        "result_id": "RES-EX-002",
        "client_name": "Residencial Beta",
        "title": "Simulação Lumínica — Empreendimento Beta",
        "summary": "Relatório lumínico. Algumas tipologias abaixo do limiar sDA 300/50.",
        "metrics": {"sDA_300_50 (%)": 58.9, "ASE_1000_250 (%)": 9.0},
        "tables": [],
        "assets": {"images": [], "pdfs": []},
        "created_at": "2025-09-12T00:00:00Z"
    }
}
# --------------------------------------------------------------------------------

st.sidebar.header("Gerador de links (demo)")
with st.sidebar.form("link_form"):
    st.subheader("Gerar link assinado (no app)")
    pick = st.selectbox("Escolha um resultado exemplo", options=list(EXAMPLE_RESULTS.keys()))
    expires_days = st.number_input("Expira em (dias)", min_value=1, max_value=365, value=30)
    include_pin = st.checkbox("Exigir PIN simples ao abrir (opcional)", value=False)
    pin = None
    if include_pin:
        pin = st.text_input("PIN público (ex: 1234)", value="1234")
    submit = st.form_submit_button("Gerar link de visualização")

if submit:
    now = datetime.utcnow()
    payload = {
        "iss": "hygge-demo",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=int(expires_days))).timestamp()),
        # Aqui colocamos TODO o bloco do resultado dentro do token -> sem necessidade de DB
        "data": {
            "result": EXAMPLE_RESULTS[pick],
            "pin": pin  # opcional: app pedirá este PIN antes de mostrar dados sensíveis
        }
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    qs = urlencode({"t": token})
    vis_link = f"{BASE_URL}/?{qs}"
    st.sidebar.success("Link gerado (copie abaixo)")
    st.sidebar.code(vis_link, language="text")
    st.sidebar.caption("Abra em uma janela anônima para testar como cliente.")

st.markdown("---")
# ------------------------ Visualizador (única página) ------------------------
qp = st.experimental_get_query_params()
token_list = qp.get("t")
if not token_list:
    st.info("Nenhum token na URL. Gere um link no painel lateral e cole na barra de endereço (ou abra o link gerado).")
    st.stop()

token = token_list[0]

# - decodifica e valida token
try:
    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
except ExpiredSignatureError:
    st.error("Este link expirou. Gere um novo.")
    st.stop()
except InvalidTokenError:
    st.error("Token inválido. Verifique o link.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao validar token: {e}")
    st.stop()

data = decoded.get("data", {})
result = data.get("result")
if not result:
    st.error("Token válido mas não contém resultado.")
    st.stop()

# Se o token contém um PIN, pedir para o usuário digitar antes de revelar
required_pin = data.get("pin")
if required_pin:
    user_pin = st.text_input("Este link exige um PIN para liberar o resultado", type="password")
    if st.button("Validar PIN"):
        if user_pin == required_pin:
            st.success("PIN correto — desbloqueando resultado.")
        else:
            st.error("PIN incorreto.")
            st.stop()
    else:
        st.stop()

# Exibir resultado
st.success(f"Resultado para: **{result.get('client_name','-')}**")
st.caption(f"ID: `{result.get('result_id')}` • Criado em {result.get('created_at')}")

st.header(result.get("title", "Resultado"))
st.write(result.get("summary", ""))

# Métricas
metrics = result.get("metrics", {}) or {}
if metrics:
    st.subheader("Indicadores")
    cols = st.columns(min(4, max(1, len(metrics))))
    for (k, v), col in zip(metrics.items(), cols):
        with col:
            st.metric(label=k, value=str(v))

# Tabelas
tables = result.get("tables", []) or []
if tables:
    st.subheader("Tabelas")
    import pandas as pd
    for t in tables:
        st.markdown(f"**{t.get('title','Tabela')}**")
        df = pd.DataFrame(t.get("rows", []), columns=t.get("columns", []))
        st.dataframe(df, use_container_width=True)

# Assets
assets = result.get("assets", {}) or {}
if assets.get("images") or assets.get("pdfs"):
    st.subheader("Anexos")
    if assets.get("images"):
        for img in assets.get("images"):
            st.markdown(f"**{img.get('label','Imagem')}**")
            st.image(img.get("url"), use_container_width=True)
    if assets.get("pdfs"):
        for pdf in assets.get("pdfs"):
            st.markdown(f"**{pdf.get('label','PDF')}**")
            st.write(f"[Abrir PDF]({pdf.get('url')})")

# JSON bruto e download
st.divider()
st.subheader("JSON (bruto)")
st.json(result)
st.download_button("Baixar JSON do resultado", data=str(result).encode("utf-8"), file_name=f"{result.get('result_id')}.json")
# --------------------------------------------------------------------------------
