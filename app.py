import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import time
import random
import streamlit.components.v1 as components

# Importa as funções de criação dos nossos módulos de agentes
from agente_marxista import criar_agente_marxista
from agente_capitalista import criar_agente_capitalista

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Debate de IAs", page_icon="💡", layout="wide")

# --- CSS FINAL PARA A INTERFACE PROFISSIONAL ---
st.markdown("""
<style>
    /* Reset e fundo da página */
    body, #root {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .block-container { 
        padding-top: 1rem !important; 
    }
    
    /* Container principal da aplicação */
    .main-container {
        max-width: 950px;
        margin: auto;
        background-color: #161A21;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        padding: 1rem 1.5rem;
    }

    h1 { 
        text-align: center; 
        color: #FAFAFA;
        padding-bottom: 0.5rem;
        font-weight: 300;
        letter-spacing: 2px;
    }

    /* Painel de Informações do Debate */
    .info-panel {
        text-align: center;
        padding: 0.8rem;
        background-color: rgba(49, 51, 63, 0.5);
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: #FFFFFF; /* Texto branco */
    }
    .info-panel strong {
        color: #00A896; /* Cor de destaque */
    }

    /* Painel de Controle */
    .control-panel {
        padding: 1rem;
        border: 1px solid #31333F;
        background-color: #0E1117;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .control-panel .stButton>button {
        background-color: #00A896;
        color: white;
        font-weight: bold;
        width: 100%;
    }

    /* Janela de chat com altura fixa e rolagem interna */
    .chat-window {
        height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        background-color: #0E1117;
        border-radius: 8px;
        border: 1px solid #31333F;
        display: flex;
        flex-direction: column;
    }
    
    .msg-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }
    .msg-bubble {
        max-width: 85%;
        padding: 14px 20px;
        border-radius: 18px;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 1em;
        color: #212121;
    }
    .marxist-bubble { background-color: #F8BBD0; border: 1px solid #F48FB1; border-bottom-left-radius: 5px; }
    .capitalist-bubble { background-color: #BBDEFB; border: 1px solid #90CAF9; border-bottom-right-radius: 5px; }
    .capitalist-container { justify-content: flex-end; flex-direction: row-reverse; }
    .avatar { font-size: 2rem; margin: 0 10px; }
</style>
""", unsafe_allow_html=True)

# --- INÍCIO DO CONTAINER PRINCIPAL DA UI ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("💡 DEBATE DE AGENTES")

with st.sidebar:
    st.header("⚙️ Configuração")
    google_api_key = st.text_input("Sua Google API Key", key="api_key", type="password")
    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        try:
            genai.configure(api_key=google_api_key)
            st.success("API Key Válida!")
        except Exception:
            st.error("API Key Inválida.")
            google_api_key = None

@st.cache_resource
def inicializar_agentes():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.4)
    return {"Marxista": criar_agente_marxista(llm), "Capitalista": criar_agente_capitalista(llm)}

if 'etapa_debate' not in st.session_state:
    st.session_state.etapa_debate = "INICIO"
    st.session_state.tema = "A automação no trabalho levará à libertação ou a uma maior precarização?"
    st.session_state.historico_dialogo = []
    st.session_state.turno_atual = ""
    st.session_state.ordem = []
    st.session_state.processing = False

def scroll_to_bottom():
    components.html("<script>parent.document.querySelector('.chat-window').scrollTop = parent.document.querySelector('.chat-window').scrollHeight;</script>", height=0)

if not google_api_key:
    st.info("Por favor, insira sua Google API Key na barra lateral para começar.")
else:
    agentes_map = inicializar_agentes()

    # --- PAINEL DE INFORMAÇÕES DO DEBATE ---
    if st.session_state.etapa_debate != "INICIO":
        st.markdown(f"""
        <div class="info-panel">
            <strong>TEMA:</strong> <em>{st.session_state.tema}</em><br>
            <strong>ORDEM:</strong> 1º {st.session_state.ordem[0]} | 2º {st.session_state.ordem[1]}
        </div>
        """, unsafe_allow_html=True)

    # --- PAINEL DE CONTROLE ---
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    etapa_titulo = st.session_state.etapa_debate.replace('_', ' ').title()
    
    if st.session_state.etapa_debate == "INICIO":
        st.markdown("### Preparação do Debate")
        st.session_state.tema = st.text_input("Defina o tema central:", st.session_state.tema, label_visibility="collapsed")
        if st.button("SORTEAR ORDEM", type="primary", disabled=st.session_state.processing):
            ordem = ["Marxista", "Capitalista"]
            random.shuffle(ordem)
            st.session_state.ordem = ordem
            st.session_state.turno_atual = ordem[0]
            st.session_state.historico_dialogo = [] # Limpa o diálogo
            st.session_state.etapa_debate = "ARGUMENTO_INICIAL_1"
            st.rerun()
    elif st.session_state.etapa_debate != "FIM_DEBATE":
        st.markdown(f"### {etapa_titulo}")
        st.write(f"É a vez do **Agente {st.session_state.turno_atual}**.")
        if st.button(f"Dar a palavra ao {st.session_state.turno_atual}", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            st.rerun()
    else: # FIM_DEBATE
        st.markdown("### DEBATE ENCERRADO!")
        if st.button("Iniciar Novo Debate"):
            for agente_executor in agentes_map.values():
                agente_executor.memory.clear()
            st.session_state.etapa_debate = "INICIO"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- JANELA DE CHAT ---
    chat_placeholder = st.empty()
    
    # Definição da função que estava faltando
    def render_chat_window(streaming_content=""):
        # Constrói o HTML para o histórico de diálogo
        history_html = ""
        for msg in st.session_state.historico_dialogo:
            if msg['role'] == "Marxista":
                history_html += f'<div class="msg-container"><div class="avatar">🔴</div><div class="msg-bubble marxist-bubble">{msg["content"]}</div></div>'
            else: # Capitalista
                history_html += f'<div class="msg-container capitalist-container"><div class="msg-bubble capitalist-bubble">{msg["content"]}</div><div class="avatar">🔵</div></div>'
        
        # Renderiza a janela de chat inteira no placeholder
        chat_placeholder.markdown(f'<div class="chat-window">{history_html}{streaming_content}</div>', unsafe_allow_html=True)

    # Renderiza o chat estático inicial
    if not st.session_state.processing:
        render_chat_window()
    
    # --- LÓGICA DE GERAÇÃO (Executada quando o botão é pressionado) ---
    if st.session_state.processing:
        agente_nome = st.session_state.turno_atual
        agente_executor = agentes_map[agente_nome]
        
        # Construção dinâmica e segura do prompt
        etapa_atual = st.session_state.etapa_debate
        prompt_contexto = f"O tema do debate é: '{st.session_state.tema}'.\n"
        
        if etapa_atual == "ARGUMENTO_INICIAL_1":
            prompt_contexto += "Você é o primeiro a falar. Apresente seu argumento inicial."
        elif etapa_atual == "ARGUMENTO_INICIAL_2":
            if st.session_state.historico_dialogo:
                prompt_contexto += f"Seu oponente ({st.session_state.ordem[0]}) abriu o debate com: '{st.session_state.historico_dialogo[-1]['content']}'. Apresente seu argumento inicial."
        elif etapa_atual == "REPLICA":
            if len(st.session_state.historico_dialogo) >= 2:
                prompt_contexto += f"O argumento inicial do seu oponente ({st.session_state.ordem[0]}) foi: '{st.session_state.historico_dialogo[-2]['content']}'. Agora é sua vez de fazer a réplica direta a este ponto."
        elif etapa_atual == "TREPLICA":
             if st.session_state.historico_dialogo:
                prompt_contexto += f"Seu oponente respondeu com a seguinte réplica: '{st.session_state.historico_dialogo[-1]['content']}'. Apresente sua tréplica."
        elif etapa_atual == "SINTESE_FINAL_1":
            prompt_contexto += "O debate está chegando ao fim. Faça suas considerações finais, consolidando seus pontos principais."
        elif etapa_atual == "SINTESE_FINAL_2":
            prompt_contexto += "Para encerrar o debate, faça suas considerações finais."

        etapas_fluxo = {"ARGUMENTO_INICIAL_1": ("ARGUMENTO_INICIAL_2", st.session_state.ordem[1]), "ARGUMENTO_INICIAL_2": ("REPLICA", st.session_state.ordem[1]), "REPLICA": ("TREPLICA", st.session_state.ordem[0]), "TREPLICA": ("SINTESE_FINAL_1", st.session_state.ordem[0]), "SINTESE_FINAL_1": ("SINTESE_FINAL_2", st.session_state.ordem[1]), "SINTESE_FINAL_2": ("FIM_DEBATE", "Nenhum")}
        proxima_etapa, proximo_a_falar = etapas_fluxo[st.session_state.etapa_debate]

        with st.spinner(f"Agente {agente_nome} está processando..."):
            response = agente_executor.invoke({"input": prompt_contexto})
            resposta_agente = response['output']

        # Efeito de digitação no placeholder
        avatar = "🔴" if agente_nome == "Marxista" else "🔵"
        container_class = "capitalist-container" if agente_nome == "Capitalista" else ""
        bubble_class = "capitalist-bubble" if agente_nome == "Capitalista" else "marxist-bubble"
        
        full_response_text = ""
        # CORREÇÃO: Definindo a função que faltava
        def render_chat_history():
            history_html = ""
            for msg in st.session_state.historico_dialogo:
                if msg['role'] == "Marxista":
                    history_html += f'<div class="msg-container"><div class="avatar">🔴</div><div class="msg-bubble marxist-bubble">{msg["content"]}</div></div>'
                else: # Capitalista
                    history_html += f'<div class="msg-container capitalist-container"><div class="msg-bubble capitalist-bubble">{msg["content"]}</div><div class="avatar">🔵</div></div>'
            return history_html
            
        historico_html_estatico = render_chat_history()

        for chunk in resposta_agente.split():
            full_response_text += chunk + " "
            time.sleep(0.03)
            
            # Constrói o HTML da nova mensagem
            if agente_nome == "Capitalista":
                new_msg_html = f'<div class="msg-container {container_class}"><div class="msg-bubble {bubble_class}">{full_response_text + "▌"}</div><div class="avatar">{avatar}</div></div>'
            else:
                new_msg_html = f'<div class="msg-container {container_class}"><div class="avatar">{avatar}</div><div class="msg-bubble {bubble_class}">{full_response_text + "▌"}</div></div>'
            
            # Atualiza a janela de chat inteira
            render_chat_window(streaming_content=new_msg_html)
            scroll_to_bottom()
        
        # Adiciona a resposta completa ao histórico
        st.session_state.historico_dialogo.append({"role": agente_nome, "content": resposta_agente})
        
        # Atualiza o estado para o próximo turno
        st.session_state.etapa_debate = proxima_etapa
        st.session_state.turno_atual = proximo_a_falar
        st.session_state.processing = False
        
        # Limpa o placeholder e recarrega a página
        time.sleep(1)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # Fecha o main-container
