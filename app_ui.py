import streamlit as st
import pandas as pd
import os
from io import BytesIO
from app import extract_tables_from_pdf
import time


def get_theme_css(dark_mode=False):
    """Retorna o CSS baseado no tema selecionado"""
    if dark_mode:
        return """
        <style>
        /* Hide Streamlit header and menu */
        header[data-testid="stHeader"] {
            background: none !important;
            height: 0 !important;
        }
        
        .main > div {
            padding-top: 0 !important;
        }
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            padding: 1rem 0;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            border-bottom: 3px solid #64B5F6;
            box-shadow: 0 2px 10px rgba(100, 181, 246, 0.2);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .header-title {
            color: #64B5F6;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 0 0 15px rgba(100, 181, 246, 0.4);
            margin: 0;
        }
        
        .header-icon {
            font-size: 3rem;
            text-shadow: 0 0 20px rgba(100, 181, 246, 0.3);
            animation: pulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes pulse {
            from { transform: scale(1); }
            to { transform: scale(1.1); }
        }
        
        .subtitle {
            text-align: center;
            color: #B0BEC5;
            font-size: 1.1rem;
            margin: -1rem 0 2rem 0;
            padding: 1rem;
            background: rgba(100, 181, 246, 0.1);
            border-radius: 10px;
        }
        
        /* Footer Dark Mode */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #B0BEC5;
            text-align: center;
            padding: 10px 0;
            border-top: 2px solid #64B5F6;
            z-index: 999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
        }
        
        .footer a {
            color: #64B5F6;
            text-decoration: none;
            font-weight: bold;
        }
        
        .footer a:hover {
            text-shadow: 0 0 5px rgba(100, 181, 246, 0.8);
        }
        </style>
        """
    else:
        return """
        <style>
        /* Hide Streamlit header and menu */
        header[data-testid="stHeader"] {
            background: none !important;
            height: 0 !important;
        }
        
        .main > div {
            padding-top: 0 !important;
        }
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem 0;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            border-bottom: 3px solid #2E86AB;
            box-shadow: 0 2px 10px rgba(46, 134, 171, 0.3);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .header-title {
            color: #2E86AB;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(46, 134, 171, 0.2);
            margin: 0;
        }
        
        .header-icon {
            font-size: 3rem;
            text-shadow: 0 0 20px rgba(46, 134, 171, 0.2);
            animation: pulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes pulse {
            from { transform: scale(1); }
            to { transform: scale(1.1); }
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.1rem;
            margin: -1rem 0 2rem 0;
            padding: 1rem;
            background: rgba(46, 134, 171, 0.1);
            border-radius: 10px;
        }
        
        /* Footer Light Mode */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
            text-align: center;
            padding: 10px 0;
            border-top: 2px solid #2E86AB;
            z-index: 999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        
        .footer a {
            color: #2E86AB;
            text-decoration: none;
            font-weight: bold;
        }
        
        .footer a:hover {
            text-shadow: 0 0 5px rgba(46, 134, 171, 0.6);
        }
        </style>
        """


def to_excel(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to an in-memory Excel file.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def main():
    """
    Main function to run the Streamlit application.
    """
    # Configuração da página com ícone personalizado
    st.set_page_config(
        page_title="Extrator de Tabelas PDF",
        page_icon="public/pumper.png",
        layout="wide"
    )

    # Inicialização do state para dark mode
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

    # Aplicar CSS baseado no tema
    theme_css = get_theme_css(st.session_state.dark_mode)
    st.markdown(theme_css, unsafe_allow_html=True)

    # Header customizado com ícones antes e depois do título
    st.markdown("""
    <div class="custom-header">
        <div class="header-content">
            <div class="header-icon">🏗️</div>
            <h1 class="header-title">Extrator de Tabelas PDF</h1>
            <div class="header-icon">📊</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        '<p class="subtitle">Faça o upload de um arquivo PDF e configure '
        'as colunas para extrair tabelas automaticamente</p>',
        unsafe_allow_html=True
    )

    # --- Coluna da Esquerda: Inputs do Usuário ---
    with st.sidebar:
        # Imagem no topo da barra lateral
        st.image(
            "public/pumper.png",
            width=200,
            caption="PDF Table Extractor"
        )
        
        # Toggle de dark mode
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("🎨")
        with col2:
            dark_mode_text = ("🌙 Dark Mode" if not st.session_state.dark_mode
                              else "☀️ Light Mode")
            if st.button(dark_mode_text, key="theme_toggle"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                # Compatibilidade com diferentes versões do Streamlit
                try:
                    st.rerun()
                except AttributeError:
                    try:
                        st.experimental_rerun()
                    except AttributeError:
                        st.info("🔄 Tema alterado! Recarregue a página.")
        
        st.markdown("---")
        st.header("Configurações de Extração")

        uploaded_file = st.file_uploader("1. Escolha o arquivo PDF", type="pdf", help="Clique para selecionar ou arraste o arquivo PDF aqui.")

        num_columns = st.number_input("2. Informe o número de colunas da tabela", min_value=1, value=1, step=1)

        column_names = []
        st.write("3. Digite o nome de cada coluna:")
        for i in range(num_columns):
            col_name = st.text_input(f"Nome da Coluna {i+1}", key=f"col_{i}")
            column_names.append(col_name)

        extract_button = st.button("Extrair Tabelas", type="primary", use_container_width=True)

    # --- Área Principal: Exibição dos Resultados ---
    
    # Exibe imagem central quando não há arquivo carregado
    if uploaded_file is None:
        st.markdown('<div class="pumper-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "public/pumper.png",
                width=350,
                caption="🛢️ PDF Table Extractor - Powered by AI"
            )
            st.markdown("### 📄 Aguardando arquivo PDF...")
            
            st.info("""
            **📋 Como usar:**
            
            1. **📁 Upload**: Faça upload do arquivo PDF na barra lateral
            2. **� Colunas**: Configure o número de colunas da tabela
            3. **✏️ Nomes**: Digite o nome de cada coluna
            4. **🚀 Extrair**: Clique em 'Extrair Tabelas' e aguarde
            
            **✨ Funcionalidades:**
            - 🧹 Remove cabeçalhos duplicados automaticamente
            - � Consolida linhas quebradas 
            - 📊 Múltiplos métodos de extração
            - 📥 Download direto em Excel
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Verifica se o botão foi clicado sem arquivo
    if extract_button and uploaded_file is None:
        st.error("⚠️ Por favor, faça o upload de um arquivo PDF antes de extrair as tabelas!")
        st.info("👆 Use o botão 'Escolha o arquivo PDF' na barra lateral")
        return
    
    # Verifica se há colunas vazias
    if extract_button and uploaded_file is not None:
        empty_columns = [i+1 for i, col in enumerate(column_names) if not col.strip()]
        if empty_columns:
            st.error(f"⚠️ Por favor, preencha o nome da(s) coluna(s): {empty_columns}")
            return
    
    if extract_button and uploaded_file is not None:
        # Cria barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Etapa 1: Preparação
            status_text.text('📁 Preparando arquivo... (10%)')
            progress_bar.progress(10)
            
            temp_dir = "temp_files"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            pdf_path = os.path.join(temp_dir, uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Etapa 2: Iniciando extração
            status_text.text('🔍 Iniciando extração de tabelas... (30%)')
            progress_bar.progress(30)
            
            # Etapa 3: Processamento
            status_text.text('⚙️ Processando PDF com múltiplos métodos... (60%)')
            progress_bar.progress(60)

            # Chama a função de extração
            df_table = extract_tables_from_pdf(pdf_path, column_names)

            # Etapa 4: Limpeza de dados
            status_text.text('🧹 Limpando dados e consolidando linhas... (80%)')
            progress_bar.progress(80)

            # Remove o arquivo temporário
            os.remove(pdf_path)
            
            # Etapa 5: Finalização
            status_text.text('✅ Processamento concluído! (100%)')
            progress_bar.progress(100)
            
            # Limpa a barra de progresso após um breve delay
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()

            if df_table is not None and not df_table.empty:
                st.success(f"🎉 Tabelas extraídas com sucesso! {df_table.shape[0]} linhas encontradas.")
                
                # Mostra estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total de Linhas", df_table.shape[0])
                with col2:
                    st.metric("📋 Total de Colunas", df_table.shape[1])
                with col3:
                    st.metric("📄 Arquivo", uploaded_file.name)
                
                st.dataframe(df_table, use_container_width=True)

                excel_bytes = to_excel(df_table)
                st.download_button(
                    label="📥 Baixar como Excel", 
                    data=excel_bytes, 
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_formatado.xlsx", 
                    mime="application/vnd.ms-excel", 
                    use_container_width=True
                )
            else:
                st.error("❌ Não foi possível extrair tabelas do PDF.")
                st.info("💡 **Dicas de troubleshooting:**")
                st.info("• Verifique se o PDF contém tabelas com bordas visíveis")
                st.info("• Confirme se o número de colunas está correto")
                st.info("• Teste com um PDF mais simples primeiro")
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Erro durante o processamento: {str(e)}")
            st.info("💡 Tente novamente ou verifique o arquivo PDF")

    # --- Rodapé ---
    st.markdown("""
    <div class="footer">
        <p>
            Created by Adalberto Ribeiro | 
            <a href="https://www.linkedin.com/in/adalberto-ramos-ribeiro-344092107/" target="_blank">LinkedIn</a> | 
            <a href="https://github.com/Beto1821/Extrator-de-Tabelas-PDF" target="_blank">GitHub Repository</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
