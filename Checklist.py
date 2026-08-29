import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Configuração da página
st.set_page_config(page_title="Checklist de Frota Completo", layout="wide")

# Diretórios para arquivos
os.makedirs("fotos_checklists", exist_ok=True)
os.makedirs("assinaturas", exist_ok=True)

# Conexão com Banco de Dados SQLite
conn = sqlite3.connect("frota_completa.db", check_same_thread=False)
c = conn.cursor()

# Criação da tabela com todos os campos do checklist
c.execute('''
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_vistoria TEXT,
        placa TEXT,
        motorista TEXT,
        km INTEGER,
        nivel_combustivel TEXT,
        destino_objetivo TEXT,
        
        -- Interior
        painel_luzes TEXT,
        cintos_seguranca TEXT,
        limpadores_lavador TEXT,
        retrovisores TEXT,
        buzina_freio_mao TEXT,
        
        -- Sob o Capô
        oleo_motor TEXT,
        liquido_arrefecimento TEXT,
        fluido_freio TEXT,
        fluido_direcao TEXT,
        reservatorio_limpador TEXT,
        bateria TEXT,
        
        -- Externa e Iluminação
        farois_lanternas TEXT,
        luzes_sinalizacao TEXT,
        luz_placa TEXT,
        palhetas_borracha TEXT,
        
        -- Pneus e Rodas
        pressao_pneus TEXT,
        conservacao_twi TEXT,
        estepe TEXT,
        
        -- Equipamentos e Docs
        kit_emergencia TEXT,
        documento_crlv TEXT,
        
        -- Lataria, Pintura e Placas
        lataria_pintura TEXT,
        adesivagem_logos TEXT,
        placas_lacre_qr TEXT,
        
        -- Estofados e Cabine
        estofados_bancos TEXT,
        revestimentos_limpeza TEXT,
        tapetes_fixacao TEXT,
        ar_multimidia_acessorios TEXT,
        
        -- Mídia e Registro
        observacoes TEXT,
        caminho_foto TEXT,
        caminho_assinatura TEXT,
        data_hora TEXT
    )
''')
conn.commit()

st.title("🚗 Gestão de Frota - Checklist Veicular Completo")

menu = st.sidebar.radio("Navegação", ["Novo Checklist", "Histórico de Vistorias"])

if menu == "Novo Checklist":
    st.subheader("📋 Preenchimento da Vistoria")
    
    with st.form("form_checklist_completo"):
        # --- 1. IDENTIFICAÇÃO E DIÁRIO DE BORDO ---
        st.write("### 1. Diário de Bordo & Identificação")
        c1, c2, c3 = st.columns(3)
        with c1:
            tipo_vistoria = st.selectbox("Tipo de Vistoria", ["Retirada / Empréstimo", "Devolução", "Periódica"])
            placa = st.text_input("Placa do Veículo", placeholder="ABC1D23").upper()
        with c2:
            motorista = st.text_input("Nome do Condutor / Responsável")
            km = st.number_input("Quilometragem (KM)", min_value=0, step=1)
        with c3:
            combustivel = st.select_slider("Nível de Combustível", options=["Reserva", "1/4", "1/2", "3/4", "Cheio"])
            destino = st.text_input("Destino / Objetivo do Trajeto")

        st.markdown("---")

        # --- 2. NO INTERIOR DO VEÍCULO ---
        st.write("### 2. No Interior do Veículo")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            painel = st.radio("Painel / Luzes Espia", ["OK", "Atenção", "N/A"])
        with c2:
            cintos = st.radio("Cintos de Segurança", ["OK", "Atenção", "N/A"])
        with c3:
            limpadores = st.radio("Limpadores / Lavador", ["OK", "Atenção", "N/A"])
        with c4:
            retrovisores = st.radio("Retrovisores (Int/Ext)", ["OK", "Atenção", "N/A"])
        with c5:
            buzina_freio = st.radio("Buzina e Freio de Mão", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 3. SOB O CAPÔ ---
        st.write("### 3. Sob o Capô (Níveis e Fluidos)")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            oleo = st.radio("Óleo do Motor", ["OK", "Atenção", "N/A"])
        with c2:
            arrefecimento = st.radio("Líq. Arrefecimento", ["OK", "Atenção", "N/A"])
        with c3:
            fl_freio = st.radio("Fluido de Freio", ["OK", "Atenção", "N/A"])
        with c4:
            fl_direcao = st.radio("Direção Hidráulica", ["OK", "Atenção", "N/A"])
        with c5:
            res_limpador = st.radio("Água do Limpador", ["OK", "Atenção", "N/A"])
        with c6:
            bateria = st.radio("Bateria / Polos", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 4. ILUMINAÇÃO E SINALIZAÇÃO ---
        st.write("### 4. Iluminação e Sinalização Externa")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            farois = st.radio("Faróis e Lanternas", ["OK", "Atenção", "N/A"])
        with c2:
            sinalizacao = st.radio("Setas / Pisca / Ré", ["OK", "Atenção", "N/A"])
        with c3:
            luz_placa = st.radio("Luz de Placa", ["OK", "Atenção", "N/A"])
        with c4:
            palhetas = st.radio("Estado das Palhetas", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 5. PNEUS E RODAS ---
        st.write("### 5. Pneus e Rodas")
        c1, c2, c3 = st.columns(3)
        with c1:
            pressao_pneus = st.radio("Calibragem / Pressão", ["OK", "Atenção", "N/A"])
        with c2:
            twi_pneus = st.radio("Conservação / TWI / Rasgos", ["OK", "Atenção", "N/A"])
        with c3:
            estepe = st.radio("Estepe (Estado e Pressão)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 6. EQUIPAMENTOS OBRIGATÓRIOS E PLACAS ---
        st.write("### 6. Equipamentos Obrigatórios, Placas e Docs")
        c1, c2, c3 = st.columns(3)
        with c1:
            kit_emergencia = st.radio("Triângulo / Macaco / Chave Roda", ["OK", "Atenção", "N/A"])
        with c2:
            documento = st.radio("Documentação (CRLV)", ["OK", "Atenção", "N/A"])
        with c3:
            placas = st.radio("Placas (Fixação, Lacre e QR Code)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 7. LATARIA, ADESIVAGEM E ESTOFADOS ---
        st.write("### 7. Lataria, Pintura, Acessórios e Estofados")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            lataria = st.radio("Lataria e Pintura (Sem amassados)", ["OK", "Atenção", "N/A"])
            adesivagem = st.radio("Adesivagem / Logotipos", ["OK", "Atenção", "N/A"])
        with c2:
            estofados = st.radio("Estofados / Bancos", ["OK", "Atenção", "N/A"])
            revestimentos = st.radio("Revestimentos / Teto / Teto", ["OK", "Atenção", "N/A"])
        with c3:
            tapetes = st.radio("Tapetes (Presença e Trava)", ["OK", "Atenção", "N/A"])
            ar_acessorios = st.radio("Ar-Cond. / Som / Multimídia", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 8. OBSERVAÇÕES E REGISTRO FOTOGRÁFICO ---
        st.write("### 8. Registro Fotográfico e Observações")
        obs = st.text_area("Observações Adicionais / Detalhes de Avarias", placeholder="Descreva aqui qualquer arranhão, ruído ou problema encontrado...")
        foto = st.camera_input("Tire uma foto do veículo, odômetro ou avaria")

        st.markdown("---")
        st.write("### ✍️ Assinatura do Condutor")
        st.caption("Desenhe sua assinatura abaixo usando o touch ou mouse:")
        
        # Componente de Canvas para Assinatura Digital
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#EEEEEE",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="canvas_assinatura",
        )

        submit = st.form_submit_button("💾 Finalizar e Salvar Vistoria")

        if submit:
            if not placa or not motorista:
                st.error("Erro: Preencha os campos obrigatórios de Placa e Condutor.")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Salvar Foto
                caminho_foto = ""
                if foto:
                    img = Image.open(foto)
                    caminho_foto = f"fotos_checklists/{placa}_{timestamp}.png"
                    img.save(caminho_foto)

                # Salvar Assinatura
                caminho_ass = ""
                if canvas_result.image_data is not None:
                    img_ass = Image.fromarray(canvas_result.image_data.astype('uint8'))
                    caminho_ass = f"assinaturas/{placa}_{timestamp}_ass.png"
                    img_ass.save(caminho_ass)

                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Inserção no banco
                c.execute('''
                    INSERT INTO vistorias (
                        tipo_vistoria, placa, motorista, km, nivel_combustivel, destino_objetivo,
                        painel_luzes, cintos_seguranca, limpadores_lavador, retrovisores, buzina_freio_mao,
                        oleo_motor, liquido_arrefecimento, fluido_freio, fluido_direcao, reservatorio_limpador, bateria,
                        farois_lanternas, luzes_sinalizacao, luz_placa, palhetas_borracha,
                        pressao_pneus, conservacao_twi, estepe,
                        kit_emergencia, documento_crlv, placas_lacre_qr,
                        lataria_pintura, adesivagem_logos, estofados_bancos, revestimentos_limpeza, tapetes_fixacao, ar_multimidia_acessorios,
                        observacoes, caminho_foto, caminho_assinatura, data_hora
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    tipo_vistoria, placa, motorista, km, combustivel, destino,
                    painel, cintos, limpadores, retrovisores, buzina_freio,
                    oleo, arrefecimento, fl_freio, fl_direcao, res_limpador, bateria,
                    farois, sinalizacao, luz_placa, palhetas,
                    pressao_pneus, twi_pneus, estepe,
                    kit_emergencia, documento, placas,
                    lataria, adesivagem, estofados, revestimentos, tapetes, ar_acessorios,
                    obs, caminho_foto, caminho_ass, data_atual
                ))
                conn.commit()
                st.success(f"Vistoria do veículo {placa} registrada com sucesso!")

elif menu == "Histórico de Vistorias":
    st.subheader("📊 Consultas e Relatórios de Frota")
    df = pd.read_sql_query("SELECT * FROM vistorias ORDER BY id DESC", conn)
    
    if df.empty:
        st.info("Nenhuma vistoria cadastrada.")
    else:
        placas = ["Todas"] + list(df["placa"].unique())
        filtro = st.selectbox("Filtrar por Veículo", placas)
        
        if filtro != "Todas":
            df = df[df["placa"] == filtro]

        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.write("### 🖼️ Comprovação Fotográfica e Assinatura")
        for idx, row in df.iterrows():
            with st.expander(f"Vistoria #{row['id']} - {row['placa']} ({row['tipo_vistoria']}) - {row['data_hora']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Motorista:** {row['motorista']}")
                    st.write(f"**KM:** {row['km']} | **Combustível:** {row['nivel_combustivel']}")
                    st.write(f"**Destino:** {row['destino_objetivo']}")
                    st.write(f"**Observações:** {row['observacoes']}")
                
                with col_b:
                    if row['caminho_foto'] and os.path.exists(row['caminho_foto']):
                        st.image(row['caminho_foto'], caption="Registro do Veículo", width=300)
                    if row['caminho_assinatura'] and os.path.exists(row['caminho_assinatura']):
                        st.image(row['caminho_assinatura'], caption="Assinatura Coletada", width=200)
