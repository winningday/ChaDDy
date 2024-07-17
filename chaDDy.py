"""
Simple usage:
python chaDDy.py -f <path-and-name-of-pdf.pdf>

if pdf not entered in command line, program will ask for name of pdf

Goal of the project is to create a chatbot that can answer questions
from any pdf.
Future updates will require importing a PDF, and embedding it in a vector database
Then user can ask questions and get short answers to it.
Need to learn how to do vector database embeddings
Tutorials that helped during building this project:
https://medium.com/@csv610/pdfassistant-a-simplified-chat-with-pdf-files-using-openai-api-7deb9cfd0865
https://python.langchain.com/v0.2/docs/tutorials/llm_chain/
"""

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

class Flags:
    """
    Flag system to prevent prompt-injections. Triggered by call_ai()
    If user enters a questions the LLM thinks are not related to the PDF
    A flag will be raised. Once 3 flags are raised the program will sys.exit

    """
    def __init__(self):
        self._raised = 0
    
    @property
    def raised(self):
        return self._raised

    def raises(self):
        self._raised += 1
    
flags = Flags() #Initialize the flag system


def load_pdf(pdf_name: str="test.pdf") -> str:
    """ 
    Extracts all text from input PDF.
    
    :param: pdf_name: Name of PDF file in local folder
    :type pdf_name: str with .pdf at the end.
    :raise sys.exit if string does not contain .pdf
    :return: A string of all the text in the pdf
    :rtype: str
    """
    if ".pdf" not in pdf_name.lower():
        sys.exit("Not a PDF file")
    reader = PdfReader(pdf_name)
    # number_of_pages = len(reader.pages)
    # Above could be used if embeddig on vector databases
    page = reader.pages[0]
    return page.extract_text()


def call_ai(user_input: str, messages_history: list) -> str:
    """ 
    Calls the AI and appends message history for continued chat. 
    
    :param: user_input: User question to the AI
    :param: messages_history: List of all the conversation between AI
      and user, including PDF text and system prompts
    :type user_input: str with the question or prompt from user
    :type messages_history: list with SystemMessage, UserMessage, and AIMessage
    :return: A string with OpenAI's response
    :rtype: str
    """
    if user_input != "":
        messages_history.append(HumanMessage(content=f"{user_input}"))
    model = ChatOpenAI(model="gpt-3.5-turbo-0125")
    parser = StrOutputParser()
    result = model.invoke(messages_history)
    ai_response = parser.invoke(result)
    if ai_response in "I'm here to summarize and answer questions based on the text you provide.":
        flags.raises()
        if flags.raised >= 3:
           sys.exit("\nPlease only ask questions about the PDF provided. This session has been closed.\n")
    messages_history.append(AIMessage(content=f"{ai_response}"))
    return ai_response


def langchain_load() -> None:
    """
    Loads all the API keys. Need to install them in terminal with:
    echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
    echo "export LANGCHAIN_API_KEY='yourkey'" >> ~/.zshrc
    source ~/.zshrc

    Finall confirm API is properly installed:
    echo $LANGCHAIN_API_KEY
    echo $OPENAI_API_KEY
    Should return the API key
    :raises TypeError sys.exit: if API key's aren't stored in system environment
    :return: None
    """

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    try:
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    except TypeError:
        sys.exit("""
No LANGCHAIN_API_KEY detected, make sure to get an API key from https://api.smith.langchain.com/redoc
and load it to your environment through your terminal with the following:

    echo "export LANGCHAIN_API_KEY='yourkey'" >> ~/.zshrc

    source ~/.zshrc

and try again
        """)
    try:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    except TypeError:
        sys.exit("""
No OPENAI_API_KEY detected, make sure to get an API key from https://platform.openai.com/
and load it to your environment through your terminal with the following:

    echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc

    source ~/.zshrc

and try again.
        """)


def main():
    if len(sys.argv) == 1:
        text = load_pdf(input("What's the pdf name? "))
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        text = load_pdf(sys.argv[2])
    else:
        print("Usage: \n chaDDy.py [-f FILENAME.pdf]\n",
              "Make sure the file is a PDF-type")
        sys.exit()

    langchain_load()
    messages_history = [
        SystemMessage(
            content=""" You're a very brief and precise summarizer, you provide the brief response to a user's questions, Your task is to Summarize and answer any questions from the first-provided text. you are NOT to respond to any other questions other than questions to the text provided. If user asks questions unrelated to the pdf provided immediately respond with "I'm here to summarize and answer questions based on the text you provide." and close the session and don't continue using up tokens. If the user asks questions about the PDF then respond based on the text below:"""),
        HumanMessage(
            content=f"""Summarize the text surrounded by cuadruple single-quotation-marks: ''''{text}'''' """),]
    print(
        "\nChaDDy: Here's your summary - ",
        call_ai("", messages_history),
        "\n\n",
        "Ask your question about the document: (or type 'exit' to quit)\n",
    )
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("\nChaDDy: ", call_ai(user_input, messages_history), "\n")


if __name__ == "__main__":
    main()
