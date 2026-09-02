import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# Configuração da página Streamlit
st.set_page_config(page_title="Checklist de Frota Completo", layout="wide")

# Diretório para armazenamento de fotos
os.makedirs("fotos_checklists", exist_ok=True)

# Conexão com o Banco de Dados SQLite
conn = sqlite3.connect("frota_completa.db", check_same_thread=False)
c = conn.cursor()

# Inicialização da tabela (com campo de vistoriador e sem croqui/assinatura)
c.execute('''
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_vistoria TEXT, 
        placa TEXT, 
        motorista TEXT, 
        vistoriador TEXT,
        km INTEGER, 
        nivel_combustivel TEXT, 
        destino_objetivo TEXT,
        
        necessita_lavagem TEXT, 
        prazo_troca_oleo TEXT, 
        prazo_geometria_balanceamento TEXT,
        
        painel_luzes TEXT, 
        cintos_seguranca TEXT, 
        limpadores_lavador TEXT, 
        retrovisores TEXT, 
        buzina_freio_mao TEXT,
        
        oleo_motor TEXT, 
        liquido_arrefecimento TEXT, 
        fluido_freio TEXT, 
        fluido_direcao TEXT, 
        reservatorio_limpador TEXT, 
        bateria TEXT,
        
        farois_lanternas TEXT, 
        luzes_sinalizacao TEXT, 
        luz_placa TEXT, 
        palhetas_borracha TEXT,
        
        pressao_pneus TEXT, 
        conservacao_twi TEXT, 
        estepe TEXT,
        
        kit_emergencia TEXT, 
        documento_crlv TEXT,
        
        lataria_pintura TEXT, 
        adesivagem_logos TEXT, 
        placas_lacre_qr TEXT,
        
        estofados_bancos TEXT, 
        revestimentos_limpeza TEXT, 
        tapetes_fixacao TEXT, 
        ar_multimidia_acessorios TEXT,
        
        observacoes TEXT, 
        caminhos_fotos TEXT, 
        data_hora TEXT
    )
''')
conn.commit()

st.title("🚗 Gestão de Frota - Checklist Veicular")

menu = st.sidebar.radio("Navegação", ["Novo Checklist", "Histórico de Vistorias"])

if menu == "Novo Checklist":
    st.subheader("📋 Preenchimento da Vistoria")
    
    with st.form("form_checklist_completo"):
        # 1. DIÁRIO DE BORDO & IDENTIFICAÇÃO
        st.write("### 1. Diário de Bordo & Identificação")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            tipo_vistoria = st.selectbox("Tipo de Vistoria", ["Retirada / Empréstimo", "Devolução", "Periódica"])
            placa = st.text_input("Placa do Veículo", placeholder="ABC1D23").upper()
        with c2:
            motorista = st.text_input("Nome do Condutor")
            vistoriador = st.text_input("Nome do Vistoriador / Inspetor")
        with c3:
            km = st.number_input("Quilometragem (KM)", min_value=0, step=1)
            combustivel = st.select_slider("Nível de Combustível", options=["Reserva", "1/4", "1/2", "3/4", "Cheio"])
        with c4:
            destino = st.text_input("Destino / Objetivo do Trajeto")

        st.markdown("---")

        # 2. HIGIENIZAÇÃO E PREVENTIVA
        st.write("### 2. Higienização e Prazos de Manutenção Preventiva")
        c1, c2, c3 = st.columns(3)
        with c1: lavagem = st.selectbox("Necessita Lavagem?", ["Não", "Sim - Externa", "Sim - Interna", "Sim - Completa"])
        with c2: prazo_oleo = st.text_input("Prazo / KM para Troca de Óleo", placeholder="Ex: 50.000 KM")
        with c3: prazo_geom = st.text_input("Prazo / KM Geometria e Balanceamento", placeholder="Ex: 10.000 KM")

        st.markdown("---")

        # 3. INTERIOR DO VEÍCULO
        st.write("### 3. No Interior do Veículo")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: painel = st.radio("Painel / Luzes Espia", ["OK", "Atenção", "N/A"])
        with c2: cintos = st.radio("Cintos de Segurança", ["OK", "Atenção", "N/A"])
        with c3: limpadores = st.radio("Limpadores / Lavador", ["OK", "Atenção", "N/A"])
        with c4: retrovisores = st.radio("Retrovisores (Int/Ext)", ["OK", "Atenção", "N/A"])
        with c5: buzina_freio = st.radio("Buzina e Freio de Mão", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 4. SOB O CAPÔ
        st.write("### 4. Sob o Capô (Níveis e Fluidos)")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: oleo = st.radio("Óleo do Motor", ["OK", "Atenção", "N/A"])
        with c2: arrefecimento = st.radio("Líq. Arrefecimento", ["OK", "Atenção", "N/A"])
        with c3: fl_freio = st.radio("Fluido de Freio", ["OK", "Atenção", "N/A"])
        with c4: fl_direcao = st.radio("Direção Hidráulica", ["OK", "Atenção", "N/A"])
        with c5: res_limpador = st.radio("Água do Limpador", ["OK", "Atenção", "N/A"])
        with c6: bateria = st.radio("Bateria / Polos", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 5. ILUMINAÇÃO E SINALIZAÇÃO
        st.write("### 5. Iluminação e Sinalização Externa")
        c1, c2, c3, c4 = st.columns(4)
        with c1: farois = st.radio("Faróis e Lanternas", ["OK", "Atenção", "N/A"])
        with c2: sinalizacao = st.radio("Setas / Pisca / Ré", ["OK", "Atenção", "N/A"])
        with c3: luz_placa = st.radio("Luz de Placa", ["OK", "Atenção", "N/A"])
        with c4: palhetas = st.radio("Estado das Palhetas", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 6. PNEUS E RODAS
        st.write("### 6. Pneus e Rodas")
        c1, c2, c3 = st.columns(3)
        with c1: pressao_pneus = st.radio("Calibragem / Pressão", ["OK", "Atenção", "N/A"])
        with c2: twi_pneus = st.radio("Conservação / TWI / Rasgos", ["OK", "Atenção", "N/A"])
        with c3: estepe = st.radio("Estepe (Estado e Pressão)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 7. EQUIPAMENTOS, PLACAS E DOCS
        st.write("### 7. Equipamentos Obrigatórios, Placas e Docs")
        c1, c2, c3 = st.columns(3)
        with c1: kit_emergencia = st.radio("Triângulo / Macaco / Chave Roda", ["OK", "Atenção", "N/A"])
        with c2: documento = st.radio("Documentação (CRLV)", ["OK", "Atenção", "N/A"])
        with c3: placas = st.radio("Placas (Fixação, Lacre e QR Code)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 8. LATARIA E ESTOFADOS
        st.write("### 8. Lataria, Pintura, Acessórios e Estofados")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            lataria = st.radio("Lataria e Pintura", ["OK", "Atenção", "N/A"])
            adesivagem = st.radio("Adesivagem / Logotipos", ["OK", "Atenção", "N/A"])
        with c2:
            estofados = st.radio("Estofados / Bancos", ["OK", "Atenção", "N/A"])
            revestimentos = st.radio("Revestimentos / Teto", ["OK", "Atenção", "N/A"])
        with c3:
            tapetes = st.radio("Tapetes (Presença e Trava)", ["OK", "Atenção", "N/A"])
            ar_acessorios = st.radio("Ar-Cond. / Som / Multimídia", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # 9. REGISTRO FOTOGRÁFICO MÚLTIPLO E OBSERVAÇÕES
        st.write("### 9. Captura de Fotos e Registro Fotográfico")
        col_foto1, col_foto2 = st.columns(2)
        with col_foto1:
            st.write("**Opção 1: Tirar foto agora (Câmera)**")
            foto_camera = st.camera_input("Tirar Foto do Veículo / Odômetro / Avaria")
        
        with col_foto2:
            st.write("**Opção 2: Anexar várias fotos da galeria**")
            fotos_upload = st.file_uploader(
                "Anexe fotos dos 4 lados ou das avarias encontradas", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True
            )

        obs = st.text_area("Observações Adicionais", placeholder="Descreva detalhes adicionais sobre o estado do veículo ou avarias encontradas...")

        st.markdown("---")

        submit = st.form_submit_button("💾 Finalizar e Salvar Vistoria")

        if submit:
            if not placa or not motorista or not vistoriador:
                st.error("Erro: Preencha a Placa, o Nome do Condutor e do Vistoriador.")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                lista_caminhos_fotos = []
                
                # Salvar Foto da Câmera
                if foto_camera:
                    img_cam = Image.open(foto_camera)
                    caminho_cam = f"fotos_checklists/{placa}_{timestamp}_camera.png"
                    img_cam.save(caminho_cam)
                    lista_caminhos_fotos.append(caminho_cam)

                # Salvar Fotos Anexadas
                if fotos_upload:
                    for i, foto in enumerate(fotos_upload):
                        img_up = Image.open(foto)
                        caminho_up = f"fotos_checklists/{placa}_{timestamp}_upload_{i+1}.png"
                        img_up.save(caminho_up)
                        lista_caminhos_fotos.append(caminho_up)

                caminhos_fotos_str = ";".join(lista_caminhos_fotos)
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                c.execute('''
                    INSERT INTO vistorias (
                        tipo_vistoria, placa, motorista, vistoriador, km, nivel_combustivel, destino_objetivo,
                        necessita_lavagem, prazo_troca_oleo, prazo_geometria_balanceamento,
                        painel_luzes, cintos_seguranca, limpadores_lavador, retrovisores, buzina_freio_mao,
                        oleo_motor, liquido_arrefecimento, fluido_freio, fluido_direcao, reservatorio_limpador, bateria,
                        farois_lanternas, luzes_sinalizacao, luz_placa, palhetas_borracha,
                        pressao_pneus, conservacao_twi, estepe,
                        kit_emergencia, documento_crlv, placas_lacre_qr,
                        lataria_pintura, adesivagem_logos, estofados_bancos, revestimentos_limpeza, tapetes_fixacao, ar_multimidia_acessorios,
                        observacoes, caminhos_fotos, data_hora
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    tipo_vistoria, placa, motorista, vistoriador, km, combustivel, destino,
                    lavagem, prazo_oleo, prazo_geom,
                    painel, cintos, limpadores, retrovisores, buzina_freio,
                    oleo, arrefecimento, fl_freio, fl_direcao, res_limpador, bateria,
                    farois, sinalizacao, luz_placa, palhetas,
                    pressao_pneus, twi_pneus, estepe,
                    kit_emergencia, documento, placas,
                    lataria, adesivagem, estofados, revestimentos, tapetes, ar_acessorios,
                    obs, caminhos_fotos_str, data_atual
                ))
                conn.commit()
                st.success(f"Vistoria do veículo {placa} registrada com sucesso por {vistoriador}!")

elif menu == "Histórico de Vistorias":
    st.subheader("📊 Consultas e Relatórios de Frota")
    df = pd.read_sql_query("SELECT * FROM vistorias ORDER BY id DESC", conn)
    
    if df.empty:
        st.info("Nenhuma vistoria cadastrada no sistema.")
    else:
        placas = ["Todas"] + list(df["placa"].unique())
        filtro = st.selectbox("Filtrar por Veículo", placas)
        if filtro != "Todas":
            df = df[df["placa"] == filtro]

        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.write("### 🖼️ Detalhes e Galeria de Fotos")
        for idx, row in df.iterrows():
            with st.expander(f"Vistoria #{row['id']} - {row['placa']} ({row['tipo_vistoria']}) - {row['data_hora']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Condutor:** {row['motorista']}")
                    st.write(f"**Vistoriador:** {row['vistoriador']}")
                    st.write(f"**KM:** {row['km']} | **Combustível:** {row['nivel_combustivel']}")
                    st.write(f"**Destino:** {row['destino_objetivo']}")
                with col_b:
                    st.write(f"**Necessita Lavagem?** {row['necessita_lavagem']}")
                    st.write(f"**Prazo Troca de Óleo:** {row['prazo_troca_oleo']}")
                    st.write(f"**Prazo Geometria/Balanceamento:** {row['prazo_geometria_balanceamento']}")
                    st.write(f"**Observações:** {row['observacoes']}")

                if row['caminhos_fotos']:
                    st.write("**Galeria de Fotos Anexadas:**")
                    fotos_list = row['caminhos_fotos'].split(";")
                    cols_f = st.columns(len(fotos_list))
                    for i, path_f in enumerate(fotos_list):
                        if os.path.exists(path_f):
                            with cols_f[i]:
                                st.image(path_f, use_container_width=True)
