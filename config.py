from zetalogger import logger
import pandas as pd

IDENTITY = """You are ZetaBot, a friendly statistical assistent.
Your role is to warmly welcome researchers and provide some basic statitical results."""

MODEL="claude-3-5-sonnet-20241022"

STATIC_GREETINGS_AND_GENERAL = """
<static_context>
Basic Statistical Calculations

About:
This service provides basic statistical calculations to help you analyze and interpret data.
Some information can be obtained from an uploaded file, such as the column names and the mean of a column.
</static_context>
"""


EXAMPLES="""
<example 1>
H: Hi, What is the sum of 5 and 7?

A. The sum of 5 and 7 is 12.
</example 1>
<example 2>
H: Hi! What are the column names of the uploaded file?

A. The column names are "PTEN", "TP53", and "VEGF".
</example 2>
<example 3>
H: Hi! What is the mean of the column "PTEN" in the uploaded file?

A. The mean of the column "PTEN" is 0.5.
</example 3>
"""

ADDITIONAL_GUARDRAILS = """Please adhere to the following guardrails:
1. Only provide the mean and sum of the data.
2. Allow for reading of column names of file
3. Allow for getting the mean of a column in a file
3. If asked about other statistical calculations, inform the user
that we don't provide that service.
"""


TASK_SPECIFIC_INSTRUCTIONS = ' '.join([
   STATIC_GREETINGS_AND_GENERAL,
   EXAMPLES,
   ADDITIONAL_GUARDRAILS,
])


TOOLS = [
{
  "name": "get_sum",
  "description": "Calculate the sum of two numbers.",
  "input_schema": {
    "type": "object",
    "properties": {
      "num1": {"type": "number", "description": "The first number."},
      "num2": {"type": "number", "description": "The second number."}
    },
    "required": ["num1", "num2"]
  }
},
{
  "name": "get_col_names",
  "description": "List column names of .csv file",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_data": {"type": "string", "description": "csv file data."}
    },
    "required": []
  }
},
{
  "name": "get_mean_of_column",
  "description": "Get mean of a column in a .csv file",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_data": {"type": "string", "description": "csv file data."},
      "column_name": {"type": "string", "description": "Name of column from which to get mean."}
    },
    "required": ["column_name"]
  }
},
{
  "name": "get_mean",
  "description": "Calculate the mean of a list of numbers.",
  "input_schema": {
    "type": "object",
    "properties": {
      "numbers": {
        "type": "array",
        "items": {"type": "number"},
        "description": "A list of numbers."
      }
    },
    "required": ["numbers"]
  }
}
]


def get_sum(num1, num2):
    """Returns the sum of two numbers"""
    ret_value = num1 + num2
    return ret_value

def get_mean(numbers):
    """Returns the mean of a list of numbers"""
    ret_value = sum(numbers) / len(numbers)
    return ret_value

def get_col_names(uploaded_file):
    """Returns list of column names in file"""
    df = pd.read_csv(uploaded_file)
    columns = df.columns.tolist()
    return columns

def get_mean_of_column(uploaded_file, column_name):
    """Returns the mean of a column in a file"""
    df = pd.read_csv(uploaded_file)
    mean = df[column_name].mean()
    return mean

