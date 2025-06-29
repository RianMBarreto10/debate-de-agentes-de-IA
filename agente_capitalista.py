from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory

def criar_agente_capitalista(llm):
    """
    Cria e configura o Agente Executor para o debatedor Capitalista.
    """
    # Base de Conhecimento Capitalista
    docs_capitalista = [
        "Fonte: A Riqueza das Nações (Adam Smith): A 'mão invisível' do mercado guia os indivíduos que buscam seu próprio interesse a promover, sem intenção, um fim que beneficia a todos. A divisão do trabalho aumenta drasticamente a produtividade.",
        "Fonte: Capitalismo e Liberdade (Milton Friedman): A liberdade econômica é um fim em si mesmo e um meio indispensável para a obtenção da liberdade política. A grande ameaça à liberdade é a concentração de poder.",
        "Fonte: O Caminho da Servidão (F. Hayek): O planejamento central, ao tentar dirigir a sociedade, inevitavelmente leva à tirania e à perda da liberdade individual, pois destrói a ordem espontânea e complexa do mercado."
    ]

    # Criação do Retriever
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    textos_divididos = text_splitter.create_documents(docs_capitalista)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(textos_divididos, embeddings)
    retriever_capitalista = vectorstore.as_retriever()

    # Ferramenta
    tool_capitalista = create_retriever_tool(retriever_capitalista, "busca_fontes_capitalistas", "Busca em textos de Adam Smith, Milton Friedman e F. Hayek sobre livre mercado, liberdade econômica e os perigos do coletivismo.")
    
    # Prompt
    prompt = hub.pull("hwchase17/react-chat")
    prompt.template = "Você é um debatedor IA Capitalista. Use a ferramenta `busca_fontes_capitalistas` para embasar seus argumentos. Defenda o livre mercado, a propriedade privada e a liberdade individual como motores do progresso. Critique o socialismo e o planejamento central. Refute diretamente os pontos do seu oponente. " + prompt.template

    # Memória do Agente
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=6,
        return_messages=True
    )

    # Criação do Agente Executor com memória interna
    agent = create_react_agent(llm, [tool_capitalista], prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=[tool_capitalista], 
        memory=memory,
        verbose=True, 
        handle_parsing_errors=True
    )
    
    return agent_executor
