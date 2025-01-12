import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from adapters.pdf_loader import PDFContextLoader
from adapters.chatbot_adapter import ChatBotAdapter

# Carrega variáveis de ambiente
load_dotenv()

# Função principal
def main():
    st.set_page_config(page_title="Fretai Bot", page_icon="🤖")
    st.title("Fretai Bot")

    # Inicializa sessão
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pdf_context" not in st.session_state:
        st.session_state.pdf_context = ""

    # Carrega contexto dos PDFs (somente na primeira execução)
    if not st.session_state.pdf_context:
        pdf_loader = PDFContextLoader(folder_path="data")
        st.session_state.pdf_context = pdf_loader.load_context()
        st.success("Contexto dos PDFs carregado com sucesso!")

    # Configura o chatbot
    chatbot = ChatBotAdapter(st.session_state.pdf_context)

    # Exibe histórico de mensagens
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    # Processa entrada do usuário
    user_query = st.chat_input("Sua Mensagem")
    if user_query and user_query.strip():
        st.session_state.chat_history.append(HumanMessage(user_query))
        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = chatbot.generate_response(user_query, st.session_state.chat_history)
            st.markdown(ai_response)

        st.session_state.chat_history.append(AIMessage(ai_response))


# Ponto de entrada do Streamlit
if __name__ == "__main__":
    main()
