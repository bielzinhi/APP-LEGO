import streamlit as st
import pandas as pd

# Inicializa estado da sessão
if "planilha" not in st.session_state:
    st.session_state.planilha = None
if "bipados" not in st.session_state:
    st.session_state.bipados = set()
if "coluna_codigos" not in st.session_state:
    st.session_state.coluna_codigos = None

st.title("📦 Sistema de Bipagem de Códigos")

# Upload da planilha
uploaded_file = st.file_uploader("📂 Carregar planilha Excel", type=["xlsx", "csv"])
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        st.session_state.planilha = pd.read_csv(uploaded_file)
    else:
        st.session_state.planilha = pd.read_excel(uploaded_file)
    
    st.session_state.bipados = set()
    st.success("✅ Planilha carregada com sucesso!")

# Só continua se tiver planilha carregada
if st.session_state.planilha is not None:
    df = st.session_state.planilha

    # Escolher a coluna de códigos
    colunas = df.columns.tolist()
    st.session_state.coluna_codigos = st.selectbox("📌 Selecione a coluna de códigos:", colunas)

    st.subheader("🔍 Bipagem")

    # Campo para bipar
    codigo = st.text_input("Digite ou escaneie o código:")

    if st.button("Confirmar Bipagem"):
        if codigo.strip() == "":
            st.warning("⚠️ Digite ou escaneie um código válido!")
        elif codigo in st.session_state.bipados:
            st.error("❌ Código já bipado!")
        elif codigo not in df[st.session_state.coluna_codigos].astype(str).values:
            st.error("🚫 Código não existe na planilha!")
        else:
            st.session_state.bipados.add(codigo)
            st.success(f"✅ Código {codigo} bipado com sucesso!")

    # Contadores
    total = len(df)
    bipados = len(st.session_state.bipados)
    faltando = total - bipados

    st.progress(bipados / total)
    st.write(f"📊 Bipados: {bipados} / {total} | ⏳ Faltando: {faltando}")

    # Mostrar códigos faltantes
    faltantes = df[~df[st.session_state.coluna_codigos].astype(str).isin(st.session_state.bipados)]
    with st.expander("📋 Códigos faltantes"):
        st.dataframe(faltantes)
