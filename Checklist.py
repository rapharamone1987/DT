import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# Configuração da página e diretórios
st.set_page_config(page_title="Gestão de Frota - Checklist", layout="wide")
os.makedirs("fotos_checklists", exist_ok=True)

# Banco de dados SQLite
conn = sqlite3.connect("frota.db", check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        placa TEXT,
        motorista TEXT,
        km INTEGER,
        nivel_combustivel TEXT,
        lataria_ok TEXT,
        estofados_ok TEXT,
        limpeza_ok TEXT,
        caminho_foto TEXT,
        data_hora TEXT
    )
''')
conn.commit()

st.title("🚗 Sistema de Checklist de Frota")

# Menu Lateral
opcao = st.sidebar.selectbox("Navegação", ["Novo Checklist", "Histórico de Vistorias"])

if opcao == "Novo Checklist":
    st.subheader("📋 Registro de Vistoria")
    
    with st.form("form_checklist"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo = st.selectbox("Tipo de Vistoria", ["Retirada / Empréstimo", "Devolução", "Periódica"])
            placa = st.text_input("Placa do Veículo", placeholder="ABC1D23").upper()
            motorista = st.text_input("Nome do Motorista")
        
        with col2:
            km = st.number_input("Quilometragem Atual (KM)", min_value=0, step=1)
            combustivel = st.select_slider("Nível de Combustível", options=["Reserva", "1/4", "1/2", "3/4", "Cheio"])

        st.markdown("---")
        st.write("### 🔍 Itens de Verificação")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            lataria = st.radio("Lataria e Pintura ok?", ["Sim", "Não"])
        with col_c2:
            estofados = st.radio("Estofados limpos e íntegros?", ["Sim", "Não"])
        with col_c3:
            limpeza = st.radio("Limpeza interna ok?", ["Sim", "Não"])

        st.markdown("---")
        st.write("### 📸 Registro Fotográfico")
        foto = st.camera_input("Tire uma foto do veículo/odômetro")
        
        submeter = st.form_submit_button("Salvar Checklist")
        
        if submeter:
            if not placa or not motorista:
                st.error("Por favor, preencha a placa e o nome do motorista.")
            else:
                caminho_foto = ""
                if foto:
                    img = Image.open(foto)
                    nome_arquivo = f"fotos_checklists/{placa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    img.save(nome_arquivo)
                    caminho_foto = nome_arquivo

                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                c.execute('''
                    INSERT INTO vistorias (tipo, placa, motorista, km, nivel_combustivel, lataria_ok, estofados_ok, limpeza_ok, caminho_foto, data_hora)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (tipo, placa, motorista, km, combustivel, lataria, estofados, limpeza, caminho_foto, data_atual))
                conn.commit()
                
                st.success(f"Checklist de {tipo} registrado com sucesso para o veículo {placa}!")

elif opcao == "Histórico de Vistorias":
    st.subheader("📊 Histórico e Consultas")
    
    df = pd.read_sql_query("SELECT * FROM vistorias ORDER BY id DESC", conn)
    
    if df.empty:
        st.info("Nenhuma vistoria registrada até o momento.")
    else:
        # Filtro por placa
        placas_unicas = ["Todas"] + list(df["placa"].unique())
        filtro_placa = st.selectbox("Filtrar por Placa", placas_unicas)
        
        if filtro_placa != "Todas":
            df = df[df["placa"] == filtro_placa]
            
        st.dataframe(df.drop(columns=["caminho_foto"]), use_container_width=True)
        
        # Exibição das fotos do histórico
        st.markdown("---")
        st.write("### 🖼️ Detalhes e Fotos")
        for idx, row in df.iterrows():
            if row["caminho_foto"] and os.path.exists(row["caminho_foto"]):
                with st.expander(f"Vistoria #{row['id']} - {row['placa']} ({row['tipo']}) em {row['data_hora']}"):
                    st.write(f"**Motorista:** {row['motorista']} | **KM:** {row['km']} | **Combustível:** {row['nivel_combustivel']}")
                    st.image(row["caminho_foto"], width=400)
