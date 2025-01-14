import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from adapters.pdf_loader import PDFContextLoader
from adapters.chatbot_adapter import ChatBotAdapter

# Carrega variáveis de ambiente
load_dotenv()


def main():
    st.set_page_config(page_title="Fretai Bot", page_icon="🚌")
    st.title("Fretai Bot  🚌")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Lista para armazenar o histórico completo (perguntas e respostas)
    if "pdf_context" not in st.session_state:
        st.session_state.pdf_context = ""

    # Carrega contexto dos PDFs 
    if not st.session_state.pdf_context:
        pdf_loader = PDFContextLoader(folder_path="data")
        st.session_state.pdf_context = pdf_loader.load_context()

    if len(st.session_state.chat_history) == 0:
        welcome_message = "Bem-vindo ao chat do Fretai. Como posso te ajudar?"
        st.session_state.chat_history.append(AIMessage(welcome_message))

    # Configura o chatbot
    chatbot = ChatBotAdapter(st.session_state.pdf_context)

    # Exibe histórico completo de mensagens
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    user_query = st.chat_input("Digite sua mensagem aqui...")
    if user_query and user_query.strip():
        st.session_state.chat_history.append(HumanMessage(user_query)) # Mensagem do Usuário
        with st.chat_message("user"):
            st.markdown(user_query)

    
        with st.chat_message("assistant"):
            ai_response = chatbot.generate_response(user_query, st.session_state.chat_history)  # Gera e exibe a resposta do chatbot
            st.markdown(ai_response)

        # Adiciona a resposta do chatbot ao histórico
        st.session_state.chat_history.append(AIMessage(ai_response))



if __name__ == "__main__":
    main()
