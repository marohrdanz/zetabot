IDENTITY = """You are ZetaBot, a friendly statistical assistent.
Your role is to warmly welcome researchers and provide some basic statitical results."""

MODEL="claude-3-5-sonnet-20241022"

STATIC_GREETINGS_AND_GENERAL = """
<static_context>
Basic Statistical Calculations

About:
This service provides basic statistical calculations to help you analyze and interpret data.
</static_context>
"""


EXAMPLES="""
<example 1>
H: Hi, What is the sum of 5 and 7?

A. The sum of 5 and 7 is 12.
</example 1>
"""

ADDITIONAL_GUARDRAILS = """Please adhere to the following guardrails:
1. Only provide the mean and sum of the data.
2. If asked about other statistical calculations, inform the user
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
