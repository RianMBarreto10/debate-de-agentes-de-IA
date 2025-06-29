from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Importa o componente de memória novamente
from langchain.memory import ConversationBufferWindowMemory

def criar_agente_marxista(llm):
    """
    Cria e configura o Agente Executor para o debatedor Marxista.
    """
    # Base de Conhecimento Marxista
    docs_marxista = [
        "Fonte: Manifesto Comunista (Marx & Engels): A história de todas as sociedades existentes é a história das lutas de classes. A sociedade burguesa moderna... simplificou os antagonismos de classes em burguesia e proletariado.",
        "Fonte: O Capital (Marx): A mais-valia é a diferença entre o valor que o trabalhador produz e o valor de sua força de trabalho (salário). É a fonte do lucro e da acumulação de capital, e representa o trabalho não pago, ou seja, a exploração.",
        "Fonte: Manuscritos de 1844 (Marx): Alienação é o processo pelo qual o trabalhador se torna estranho ao produto de seu trabalho, a si mesmo e aos outros, perdendo sua essência humana sob o capitalismo."
    ]

    # Criação do Retriever
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    textos_divididos = text_splitter.create_documents(docs_marxista)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(textos_divididos, embeddings)
    retriever_marxista = vectorstore.as_retriever()
    
    # Ferramenta
    tool_marxista = create_retriever_tool(retriever_marxista, "busca_fontes_marxistas", "Busca em textos de Marx e Engels sobre luta de classes, mais-valia, alienação e materialismo histórico.")
    
    # Prompt
    prompt = hub.pull("hwchase17/react-chat")
    prompt.template = "Você é um debatedor IA Marxista. Use a ferramenta `busca_fontes_marxistas` para embasar seus argumentos. Critique o capitalismo, a propriedade privada e o individualismo. Analise tudo pela ótica da luta de classes e da exploração. Refute diretamente os pontos do seu oponente. " + prompt.template

    # Memória do Agente
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=6, # Lembra das últimas 6 trocas
        return_messages=True
    )

    # Criação do Agente
    agent = create_react_agent(llm, [tool_marxista], prompt)
    
    # O AgentExecutor agora terá sua própria memória interna
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=[tool_marxista], 
        memory=memory, # Adicionamos a memória aqui
        verbose=True, 
        handle_parsing_errors=True
    )
    
    return agent_executor
