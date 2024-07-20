# ChaDDy
### Video Demo:
None Yet

### Description:
This program uses langchain and OpenAI's API to process
and take a small-sized PDF you give it and return a summary of the document.
After the summary then the user can ask questions about the document.
While OpenAI's algorithms aren't perfect, it does give fairly decent
anwers and summaries.

PDF must be in the same folder, or relatively referenced.

Also. there is a limit in size the PDF can be. Right now that is capped
by the token size in whichever GPT engine one chooses. For the GPT3 turbo
it won't take more than 16,000 total tokens, which is around 12,000 words.
This includes the system prompts, the user prompt and all the chat history.
So that means a PDF of larger than 3000 to 5000 words will probably start failing.

The next steps would be to learn how to implement vector embedding to split
the PDF content into several documents that are stored in a vector database,
and show the LLM how to access them. But that would probably make this a month
project. But for now i'm very proud that I got it to summarize the PDF, and
keep a conversation going with the user. It maintains memory of the conversation.

## Usage:

First install all dependencies listed in requirements.txt. as follows:

```sh
pip install -r requirements.txt
```

Next, you will need to get a Langchain and an OpenAI API and
load them to your OS Environmvent:


## Getting the APIs needed:

One needs a couple APIs from the following links:

Langchain: https://api.smith.langchain.com/redoc

OpenAI: https://platform.openai.com/

Copy the API keys down.

Once you have the API keys, run the following shell command to store them in your OS environment variables as per documentation on API safety: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

For Mac/Linux

1. Run the following command in your terminal, replacing yourkey with your API key.
    ```
    echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
    ```
2. Now do the same for the Langchain API
    ```
    echo "export LANGCHAIN_API_KEY='yourkey'" >> ~/.zshrc
    ```

3. Update the shell with the new variables
    ```
    source ~/.zshrc

    ```
4. Finally, confirm that you have set your environment variables properly
using the following command.
    ```
    echo $OPENAI_API_KEY

    ```
    This should return the same OPENAI API KEY and:

    ```
    echo $LANGCHAIN_API_KEY

    ```
    Should return the same Langchain API Key...

## Running the Program:

To use the program run with:

```shell
python chaDDy.py -f <optional-pdf-name.pdf>
```
note: if PDF name isn't declared in the command-line, ChaDDy will ask for the name of the PDF.

## Suggestions for Further Improvements:

If one wishes to improve this further and has the funds, they could change
the OpenAI model to ChatGpt-4o by chaning the following code:

```python
def call_ai(text, user_input, messages_history):
    model = ChatOpenAI(model="gpt-3.5-turbo-0125")
```

Change it to:

```python
def call_ai(text, user_input, messages_history):
    model = ChatOpenAI(model="gpt-4o")
```

Note that the gpt-4o model charges a higher rate per token, so expenses will go up.

Alternatively applying some prompt engineering can improve the results.

Suggested next steps:

1. Prompt engineering improvements: Give it a persona, tell it to think in step-by-step, give context.
2. Code efficiency, if do not like the langchain library, can fix to call OpenAI directly
3. Can also remove langchain tracing, which is a way to see the results from the LLM through https://smith.langchain.com/
    ```python
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY"))
    ```
4. We tried to prevent prompt-injection by copying the text with quadruple single-quotes, and triggering keywords that will 
sys.exit. It's not super robust, but it seems to quit it if user asks non-related questions, although occasinally it wants to quit even if a question is related to the PDF. So we put in a Flags class in place that gets triggered whenever it thinks the person isn't asking questions related to the PDF (through method flags.raises()). The system allows 3 flags before it sys.exit. One can try other methods, as well as coming up with more robust prompts. Or setting up more attack detections, but it's working decently so far.
5. Implement RAG by embedding in vector database, as there is a token-size limit right now, so can only work on small PDFs
6. Ideally setup a system to allow multiple PDFs, text files, word docs, and libraries and stores the info in a database for future access. Building up a library of content from which to get info from. ie like a GPT based on our knowledgebase. Allow the program to take multiple file, docs, text, etc, libraries, once the RAG has been implemented, (using *args andd **kwargs) to process the text and send to the vector database.

## Testing the Code:
Pytest test file included, To run do the following:

```python
pytest test_chaDDy.py
```

## Sources:

For more tutorials on using langchain and langsmith refer to:
https://python.langchain.com/v0.2/docs/tutorials/llm_chain/

Best Practices for API usage:
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

