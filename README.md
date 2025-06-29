# 💡 Debate de Agentes de IA: Marxismo vs. Capitalismo

Este projeto é uma plataforma interativa que simula um debate formal entre dois agentes de IA autônomos, cada um incorporando uma ideologia distinta: um Marxista e um Capitalista. O usuário atua como moderador, definindo o tema e controlando o fluxo do debate, que segue as dinâmicas de um debate televisionado.

O objetivo é explorar até que ponto podemos criar "personas" de IA especializadas e consistentes, capazes de argumentar, refutar e defender pontos de vista complexos com base em uma base de conhecimento curada.

![image](https://github.com/user-attachments/assets/97552598-7e24-4461-bbca-36da0d35665b)


(https://imgur.com/a/9dj3Ca0)

---

### 🏛️ A Arquitetura por Trás do "Coliseu Intelectual"

Este projeto não se trata apenas de prompts; é uma arquitetura **multi-agente** orquestrada de forma robusta, onde cada componente tem uma função crítica:

#### 1. **LangChain: O Maestro do Debate**
O **LangChain** é o framework central que permite a criação e coordenação dos agentes. Ele é responsável por:
- **Criação de Agentes (`create_react_agent`):** Define o "cérebro" de cada debatedor, combinando um Modelo de Linguagem (LLM) com ferramentas e um prompt de sistema.
- **Orquestração (`AgentExecutor`):** Gerencia o ciclo de "Pensamento -> Ação -> Observação" de cada agente, permitindo que eles decidam quando usar suas ferramentas.
- **Memória (`ConversationBufferWindowMemory`):** Cada agente possui sua própria memória interna, permitindo que ele se lembre de seus próprios argumentos e mantenha a coerência ao longo do debate.

#### 2. **RAG (Retrieval-Augmented Generation): A "Biblioteca" de Cada Agente**
O núcleo da especialização de cada agente. Em vez de confiar no conhecimento genérico do LLM, cada debatedor tem acesso exclusivo à sua própria base de conhecimento:
- **Agente Marxista:** É alimentado com textos de Marx e Engels.
- **Agente Capitalista:** É alimentado com textos de Adam Smith, Milton Friedman e F. Hayek.

**O processo de RAG funciona assim:**
1.  **Vetorização:** Na inicialização, os textos de cada ideologia são divididos em trechos e transformados em vetores numéricos usando `sentence-transformers`.
2.  **Indexação:** Esses vetores são armazenados em um índice **FAISS**, um banco de dados vetorial ultrarrápido que permite buscas de similaridade semântica.
3.  **Recuperação em Tempo Real:** Quando um agente precisa formular um argumento, ele usa sua "ferramenta de busca" para consultar sua base de dados vetorial, recuperando os trechos mais relevantes da literatura para embasar sua resposta.

#### 3. **Google Gemini: O Processador de Linguagem**
Utilizamos o modelo `gemini-1.5-flash-latest` do Google como o LLM por trás de cada agente. Ele é responsável por interpretar o prompt (que inclui o contexto do debate e os dados recuperados pelo RAG) e gerar as respostas com a persona e o tom definidos.

#### 4. **Streamlit: O Estúdio de TV Virtual**
O **Streamlit** foi usado para construir a interface do usuário (UI) e gerenciar o estado da aplicação (`st.session_state`). Ele controla:
- O fluxo do debate (sorteio, blocos, turnos).
- A interação do moderador.
- A renderização dinâmica da transcrição do debate, incluindo o efeito de "digitação" e o auto-scroll, criando uma experiência de usuário fluida e imersiva.

---

### 🚀 Como Executar Localmente

1.  **Clone o repositório:**

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todos os pacotes necessários.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

5.  **Configure sua API Key:**
    Abra a aplicação no navegador, vá na barra lateral e insira sua chave da API do Google AI Studio.

---

### 💡 Possibilidades Futuras
- **Adicionar mais debatedores:** Um agente Anarquista? Um Keynesiano? A arquitetura modular permite isso facilmente.
- **Sistema de Pontuação:** Implementar a lógica para o placar do moderador influenciar um "resultado" final.
- **Análise Pós-Debate:** Uma IA que analisa a transcrição e aponta as principais falácias ou pontos fortes de cada debatedor.

Sinta-se à vontade para contribuir, abrir *issues* ou fazer um fork do projeto!
