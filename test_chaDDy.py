from chaDDy import load_pdf, call_ai, langchain_load
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

import pytest

def test_load_pdf():
    assert load_pdf("shirtificate.pdf") == "CS50 Shirtificate\nMarc Goodman took CS50"
    assert "Chapter 1 : A RUNAWAY REEF" in load_pdf("test.pdf")
    with pytest.raises(FileNotFoundError):
        load_pdf("no-file.pdf")
    with pytest.raises(SystemExit):
        load_pdf("test.py")

    # tests that it correctly reads the content of a PDF file.
    # with a small PDF file with known content checks that load_pdf returns
    # the correct text. You could also
    # Also tests how it handles non-existent files or files that aren't PDFs.


def test_call_ai():
    messages_history = [
        SystemMessage(
            content=""" You're a very brief and precise summarizer, you provide the brief response to a user's questions, Your task is to Summarize and answer any questions from the first-provided text. you are NOT to respond to any other questions other than questions to the text provided. If user asks questions unrelated to the pdf provided immediately respond with "I'm here to summarize and answer questions based on the text you provide." and close the session and don't continue using up tokens. If the user asks questions about the PDF then respond based on the text below:"""),
        HumanMessage(
            content="Summarize the text surrounded by cuadruple single-quotation-marks: ''''CS50 Shirtificate\nMarc Goodman took CS50'''' "),]
    assert "Marc Goodman" in call_ai("", messages_history)
    messages_history = [SystemMessage(content=""" You're a very brief and precise summarizer, you provide the brief response to a user's questions, Your task is to Summarize and answer any questions from the first-provided text. you are NOT to respond to any other questions other than questions to the text provided. If user asks questions unrelated to the pdf provided immediately respond with "I'm here to summarize and answer questions based on the text you provide." and close the session and don't continue using up tokens. If the user asks questions about the PDF then respond based on the text below:"""),
                        HumanMessage(content="Summarize the text surrounded by cuadruple single-quotation-marks: ''''CS50 Shirtificate\nMarc Goodman took CS50'''' "),
                        AIMessage(content='Marc Goodman earned a "CS50 Shirtificate" by completing CS50.'),
                        HumanMessage(content="Who earned it?"),
                        AIMessage(content='Marc Goodman earned the "CS50 Shirtificate" by completing CS50.'),]
    assert "Marc Goodman" in call_ai("Who got the shirtificate?", messages_history)
    flag = 2 # Mock test of global flags used to prevent prompt-injections.
    with pytest.raises(SystemExit):
        call_ai("What's the meaning of life?", messages_history)

    # tests that it correctly appends messages to the messages_history list.
    # using a known messages_history list and user_input,
    # checks that the list has been updated correctly.
    # also tests that it returns the expected output for a given input.

def test_langchain_load():
    langchain_load()
    assert os.environ["LANGCHAIN_API_KEY"] is not None
    assert os.environ["OPENAI_API_KEY"] is not None

    # tests that environment variables are being set correctly.
    # 1st calls langchain_load() and then checks os.environ has been changed

