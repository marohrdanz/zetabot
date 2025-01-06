# ZetaBot

ZetaBot was created as a learning exercise to understand how to use the
Anthropic API.

In particular, I wanted to understand how to write a tool that
lets users upload a file, and do some basic analysis on the file, but does not
send the file data to the AI--the tools do the analysis, not the AI.

## Current features of ZetaBot:

- Upload a data file
- Get list of column names in file (from a tool)
- Get mean of a column (from a tool)

As this is just a toy, there's no error handling, tests, etc.

## Quickstart

1. Create python virtual environment with `python3 -m venv venv`
2. Activate the virtual environment with `source venv/bin/activate`
3. Install the requirements with `pip install -r requirements.txt`
4. Run the steamlit app with `streamlit run app.py`
5. Open your browser and go to `http://localhost:8501`

Note: An Anthropic API key is required to run this chatbot.

## Reference

This is chatbot is the result of following
[Anthropic's customer support chatbot tutorial](https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat)
and modifying it slightly to be a very basic statistics chatbot.
