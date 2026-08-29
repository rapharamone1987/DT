import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas

# Configuração da página Streamlit
st.set_page_config(page_title="Checklist de Frota Completo", layout="wide")

# Criar diretórios necessários para armazenar arquivos e mídias
os.makedirs("fotos_checklists", exist_ok=True)
os.makedirs("assinaturas", exist_ok=True)
os.makedirs("croquis", exist_ok=True)

# Função para gerar a imagem base do croqui do veículo (silhueta) via PIL localmente
@st.cache_data
def gerar_croqui_base():
    caminho_local = "carro_croqui.png"
    
    # Se já existir localmente, reutiliza
    if os.path.exists(caminho_local):
        return Image.open(caminho_local)
    
    # Criar imagem base limpa caso não exista
    width, height = 600, 300
    img = Image.new("RGB", (width, height), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)
    
    # Desenho técnico vetorial simples da silhueta do veículo (Vista Superior e Laterais)
    draw.rectangle([5, 5, width-5, height-5], outline=(200, 200, 200), width=2)
    
    # Vista Superior do Carro (Centro)
    draw.rounded_rectangle([200, 50, 400, 250], radius=30, outline=(80, 80, 80), width=3) # Corpo
    draw.rounded_rectangle([230, 80, 370, 220], radius=15, outline=(120, 120, 120), width=2) # Teto/Vidros
    draw.line([(230, 110), (370, 110)], fill=(120, 120, 120), width=2) # Para-brisa dianteiro
    draw.line([(230, 190), (370, 190)], fill=(120, 120, 120), width=2) # Para-brisa traseiro
    
    # Pneus (Vista Superior)
    draw.rectangle([185, 70, 200, 110], fill=(50, 50, 50)) # Dianteiro Esq
    draw.rectangle([400, 70, 415, 110], fill=(50, 50, 50)) # Dianteiro Dir
    draw.rectangle([185, 190, 200, 230], fill=(50, 50, 50)) # Traseiro Esq
    draw.rectangle([400, 190, 415, 230], fill=(50, 50, 50)) # Traseiro Dir
    
    # Rótulos das Vistas
    draw.text((250, 20), "FRENTE", fill=(100, 100, 100))
    draw.text((250, 265), "TRASEIRA", fill=(100, 100, 100))
    draw.text((50, 140), "LADO ESQUERDO", fill=(100, 100, 100))
    draw.text((435, 140), "LADO DIREITO", fill=(100, 100, 100))
    
    img.save(caminho_local)
    return img

# Conexão com o Banco de Dados SQLite
conn = sqlite3.connect("frota_completa.db", check_same_thread=False)
c = conn.cursor()

# Inicialização da tabela com todos os campos do checklist
c.execute('''
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_vistoria TEXT,
        placa TEXT,
        motorista TEXT,
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
        caminho_croqui TEXT,
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
        # --- 1. DIÁRIO DE BORDO & IDENTIFICAÇÃO ---
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

        # --- 2. HIGIENIZAÇÃO E MANUTENÇÃO PREVENTIVA ---
        st.write("### 2. Higienização e Prazos de Manutenção Preventiva")
        c1, c2, c3 = st.columns(3)
        with c1:
            lavagem = st.selectbox("Necessita Lavagem?", ["Não", "Sim - Externa", "Sim - Interna", "Sim - Completa"])
        with c2:
            prazo_oleo = st.text_input("Prazo / KM para Troca de Óleo", placeholder="Ex: 50.000 KM ou 10/10/2026")
        with c3:
            prazo_geom = st.text_input("Prazo / KM Geometria e Balanceamento", placeholder="Ex: 10.000 KM ou 15/12/2026")

        st.markdown("---")

        # --- 3. INTERIOR DO VEÍCULO ---
        st.write("### 3. No Interior do Veículo")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: painel = st.radio("Painel / Luzes Espia", ["OK", "Atenção", "N/A"])
        with c2: cintos = st.radio("Cintos de Segurança", ["OK", "Atenção", "N/A"])
        with c3: limpadores = st.radio("Limpadores / Lavador", ["OK", "Atenção", "N/A"])
        with c4: retrovisores = st.radio("Retrovisores (Int/Ext)", ["OK", "Atenção", "N/A"])
        with c5: buzina_freio = st.radio("Buzina e Freio de Mão", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 4. SOB O CAPÔ ---
        st.write("### 4. Sob o Capô (Níveis e Fluidos)")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: oleo = st.radio("Óleo do Motor", ["OK", "Atenção", "N/A"])
        with c2: arrefecimento = st.radio("Líq. Arrefecimento", ["OK", "Atenção", "N/A"])
        with c3: fl_freio = st.radio("Fluido de Freio", ["OK", "Atenção", "N/A"])
        with c4: fl_direcao = st.radio("Direção Hidráulica", ["OK", "Atenção", "N/A"])
        with c5: res_limpador = st.radio("Água do Limpador", ["OK", "Atenção", "N/A"])
        with c6: bateria = st.radio("Bateria / Polos", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 5. ILUMINAÇÃO E SINALIZAÇÃO ---
        st.write("### 5. Iluminação e Sinalização Externa")
        c1, c2, c3, c4 = st.columns(4)
        with c1: farois = st.radio("Faróis e Lanternas", ["OK", "Atenção", "N/A"])
        with c2: sinalizacao = st.radio("Setas / Pisca / Ré", ["OK", "Atenção", "N/A"])
        with c3: luz_placa = st.radio("Luz de Placa", ["OK", "Atenção", "N/A"])
        with c4: palhetas = st.radio("Estado das Palhetas", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 6. PNEUS E RODAS ---
        st.write("### 6. Pneus e Rodas")
        c1, c2, c3 = st.columns(3)
        with c1: pressao_pneus = st.radio("Calibragem / Pressão", ["OK", "Atenção", "N/A"])
        with c2: twi_pneus = st.radio("Conservação / TWI / Rasgos", ["OK", "Atenção", "N/A"])
        with c3: estepe = st.radio("Estepe (Estado e Pressão)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 7. EQUIPAMENTOS OBRIGATÓRIOS E DOCS ---
        st.write("### 7. Equipamentos Obrigatórios, Placas e Docs")
        c1, c2, c3 = st.columns(3)
        with c1: kit_emergencia = st.radio("Triângulo / Macaco / Chave Roda", ["OK", "Atenção", "N/A"])
        with c2: documento = st.radio("Documentação (CRLV)", ["OK", "Atenção", "N/A"])
        with c3: placas = st.radio("Placas (Fixação, Lacre e QR Code)", ["OK", "Atenção", "N/A"])

        st.markdown("---")

        # --- 8. LATARIA, ADESIVAGEM E ESTOFADOS ---
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

        # --- 9. CROQUI DE AVARIAS ---
        st.write("### 9. Croqui para Marcação de Avarias na Lataria")
        st.caption("Risque/circule com o mouse ou toque na imagem abaixo para indicar pontos com riscos, amassados ou avarias:")
        
        img_croqui_base = gerar_croqui_base()
        
        canvas_croqui = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=3,
            stroke_color="#FF0000",
            background_image=img_croqui_base,
            height=300,
            width=600,
            drawing_mode="freedraw",
            key="canvas_croqui",
        )

        st.markdown("---")

        # --- 10. REGISTRO FOTOGRÁFICO MÚLTIPLO ---
        st.write("### 10. Captura de Fotos e Registro Fotográfico")
        
        col_foto1, col_foto2 = st.columns(2)
        with col_foto1:
            st.write("**Opção 1: Tirar foto na hora (Câmera)**")
            foto_camera = st.camera_input("Tirar Foto do Veículo / Odômetro")
        
        with col_foto2:
            st.write("**Opção 2: Anexar fotos da galeria / arquivo**")
            fotos_upload = st.file_uploader(
                "Selecione uma ou mais fotos", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True
            )

        obs = st.text_area("Observações Adicionais / Detalhes de Avarias", placeholder="Descreva aqui detalhes das avarias marcadas no croqui ou outros apontamentos...")

        st.markdown("---")
        st.write("### ✍️ Assinatura do Condutor")
        st.caption("Desenhe sua assinatura abaixo usando a tela sensível ao toque ou o mouse:")
        
        canvas_assinatura = st_canvas(
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
                st.error("Erro: Preencha a Placa e o Nome do Condutor.")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Salvar Fotos (Câmera + Galeria)
                lista_caminhos_fotos = []
                
                if foto_camera:
                    img_cam = Image.open(foto_camera)
                    caminho_cam = f"fotos_checklists/{placa}_{timestamp}_camera.png"
                    img_cam.save(caminho_cam)
                    lista_caminhos_fotos.append(caminho_cam)

                if fotos_upload:
                    for i, foto in enumerate(fotos_upload):
                        img_up = Image.open(foto)
                        caminho_up = f"fotos_checklists/{placa}_{timestamp}_upload_{i+1}.png"
                        img_up.save(caminho_up)
                        lista_caminhos_fotos.append(caminho_up)

                caminhos_fotos_str = ";".join(lista_caminhos_fotos)

                # Salvar Croqui
                caminho_croqui_str = ""
                if canvas_croqui.image_data is not None:
                    img_croqui = Image.fromarray(canvas_croqui.image_data.astype('uint8'))
                    caminho_croqui_str = f"croquis/{placa}_{timestamp}_croqui.png"
                    img_croqui.save(caminho_croqui_str)

                # Salvar Assinatura
                caminho_ass_str = ""
                if canvas_assinatura.image_data is not None:
                    img_ass = Image.fromarray(canvas_assinatura.image_data.astype('uint8'))
                    caminho_ass_str = f"assinaturas/{placa}_{timestamp}_ass.png"
                    img_ass.save(caminho_ass_str)

                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                c.execute('''
                    INSERT INTO vistorias (
                        tipo_vistoria, placa, motorista, km, nivel_combustivel, destino_objetivo,
                        necessita_lavagem, prazo_troca_oleo, prazo_geometria_balanceamento,
                        painel_luzes, cintos_seguranca, limpadores_lavador, retrovisores, buzina_freio_mao,
                        oleo_motor, liquido_arrefecimento, fluido_freio, fluido_direcao, reservatorio_limpador, bateria,
                        farois_lanternas, luzes_sinalizacao, luz_placa, palhetas_borracha,
                        pressao_pneus, conservacao_twi, estepe,
                        kit_emergencia, documento_crlv, placas_lacre_qr,
                        lataria_pintura, adesivagem_logos, estofados_bancos, revestimentos_limpeza, tapetes_fixacao, ar_multimidia_acessorios,
                        observacoes, caminhos_fotos, caminho_croqui, caminho_assinatura, data_hora
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    tipo_vistoria, placa, motorista, km, combustivel, destino,
                    lavagem, prazo_oleo, prazo_geom,
                    painel, cintos, limpadores, retrovisores, buzina_freio,
                    oleo, arrefecimento, fl_freio, fl_direcao, res_limpador, bateria,
                    farois, sinalizacao, luz_placa, palhetas,
                    pressao_pneus, twi_pneus, estepe,
                    kit_emergencia, documento, placas,
                    lataria, adesivagem, estofados, revestimentos, tapetes, ar_acessorios,
                    obs, caminhos_fotos_str, caminho_croqui_str, caminho_ass_str, data_atual
                ))
                conn.commit()
                st.success(f"Vistoria do veículo {placa} registrada com sucesso!")

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
        st.write("### 🖼️ Detalhes, Croqui, Assinatura e Galeria de Fotos")
        for idx, row in df.iterrows():
            with st.expander(f"Vistoria #{row['id']} - {row['placa']} ({row['tipo_vistoria']}) - {row['data_hora']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Motorista:** {row['motorista']}")
                    st.write(f"**KM:** {row['km']} | **Combustível:** {row['nivel_combustivel']}")
                    st.write(f"**Destino:** {row['destino_objetivo']}")
                    st.write(f"**Necessita Lavagem?** {row['necessita_lavagem']}")
                    st.write(f"**Prazo Troca de Óleo:** {row['prazo_troca_oleo']}")
                    st.write(f"**Prazo Geometria/Balanceamento:** {row['prazo_geometria_balanceamento']}")
                    st.write(f"**Observações:** {row['observacoes']}")
                
                with col_b:
                    if row['caminho_croqui'] and os.path.exists(row['caminho_croqui']):
                        st.image(row['caminho_croqui'], caption="Croqui com Marcação de Avarias", width=350)
                    if row['caminho_assinatura'] and os.path.exists(row['caminho_assinatura']):
                        st.image(row['caminho_assinatura'], caption="Assinatura Coletada", width=200)

                if row['caminhos_fotos']:
                    st.write("**Galeria de Fotos Anexadas:**")
                    fotos_list = row['caminhos_fotos'].split(";")
                    cols_f = st.columns(len(fotos_list))
                    for i, path_f in enumerate(fotos_list):
                        if os.path.exists(path_f):
                            with cols_f[i]:
                                st.image(path_f, use_container_width=True)
