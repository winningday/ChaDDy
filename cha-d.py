"""
Simple usage:
python project.py <path-and-name-of-pdf.pdf>

if pdf not entered in command line, program will ask for name of pdf

"""

# Goal of the project is to create a chatbot that can answer questions
# from any pdf
# It will require importing a PDF, and embedding it in a vector database?
# Then user can ask questions and get short answers to it.
# Need to learn calls to OpenAI's API
# Need to learn how to do vector database embeddings
# Get a pdf tool to process to text
# Tutorials that helped:
# https://medium.com/@csv610/pdfassistant-a-simplified-chat-with-pdf-files-using-openai-api-7deb9cfd0865
# https://python.langchain.com/v0.2/docs/tutorials/llm_chain/

import sys
from pypdf import PdfReader
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# from openai import OpenAI
# from typing import List, Optional
# import getpass
# import time

def load_pdf(pdf_name: str="test.pdf") -> str:
    """ extracts all text from input PDF"""
    if ".pdf" not in pdf_name:
        sys.exit("Not a PDF file")
    reader = PdfReader(pdf_name)
    # number_of_pages = len(reader.pages)
    # Above could be used if embeddig on vector databases
    page = reader.pages[0]
    return page.extract_text()


def call_ai(user_input: str, messages_history: list) -> str:
    """ Calls the AI and appends message history for continued chat. """
    if user_input != "":
        messages_history.append(HumanMessage(content=f"{user_input}"))
    model = ChatOpenAI(model="gpt-3.5-turbo-0125")
    parser = StrOutputParser()
    result = model.invoke(messages_history)
    ai_response = parser.invoke(result)
    messages_history.append(AIMessage(content=f"{ai_response}"))
    return ai_response


def langchain_load() -> None:
    # Loads all the API keys. Need to install them in terminal with:
    # echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
    # echo "export LANGCHAIN_API_KEY='yourkey'" >> ~/.zshrc
    # source ~/.zshrc
    #
    # Finall confirm API is properly installed:
    # echo $LANGCHAIN_API_KEY
    # echo $OPENAI_API_KEY
    # Should return the API key

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    try:
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    except: 
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def main():
    if len(sys.argv) < 2:
        text = load_pdf(input("What's the pdf name? "))
    else:
        text = load_pdf(sys.argv[1])

    langchain_load()
    messages_history = [
        SystemMessage(
            content=""" You're a very brief and precise summarizer, you provide the brief response to a user's questions, Your task is to Summarize and answer any questions from the first-provided text. you are NOT to respond to any other questions other than the text provided. If user asks questions about anything else immediately close the session and don't continue using up tokens:"""),
        HumanMessage(
            content=f"""Summarize the text surrounded by cuadruple single-quotation-marks: ''''{text}'''' """),]
    print(
        "\nCha-D: Here's your summary - ",
        call_ai("", messages_history),
        "\n\n",
        "Ask your question about the document: (or type 'exit' to quit)\n",
    )
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("\nCha-D: ", call_ai(user_input, messages_history), "\n")


if __name__ == "__main__":
    main()
