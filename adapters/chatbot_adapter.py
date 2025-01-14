from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv(os.path.join("data", ".env"))

class ChatBotAdapter:
    def __init__(self, pdf_context):
        self.pdf_context = pdf_context
        self.template = """
            Você é um assistente virtual para esclarecer dúvidas sobre o aplicativo Fretai que está no contexto extraído dos PDFs. 
            Caso não saiba a resposta não cite os PDFs

            Contexto extraído dos PDFs:
            {pdf_context}

            Histórico de conversa:
            {chat_history}

            Pergunta do usuário:
            {user_question}
        """
        self.llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def generate_response(self, query, chat_history):
        """Gera uma resposta baseada no contexto e histórico."""
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke({
            "chat_history": chat_history,
            "pdf_context": self.pdf_context,
            "user_question": query
        })
