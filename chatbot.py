from anthropic import Anthropic
from config import IDENTITY, TOOLS, MODEL, get_sum, get_mean, get_col_names
from dotenv import load_dotenv
from zetalogger import logger

load_dotenv()

class ChatBot:
    def __init__(self, session_state, uploaded_file):
        self.anthropic = Anthropic()
        self.session_state = session_state
        self.uploaded_file = uploaded_file # upload user data, but don't send to AI.

    def generate_message(self, messages, max_tokens):
        try:
            response = self.anthropic.messages.create(
                    model=MODEL,
                    system=IDENTITY,
                    max_tokens=max_tokens,
                    messages=messages,
                    tools=TOOLS
            )
            return response
        except Exception as e:
            return{"error": str(e)}

    def process_user_input(self, user_input):
        self.session_state.messages.append({"role": "user", "content": user_input})
          
        response_message = self.generate_message(
                messages=self.session_state.messages,
                max_tokens=2048
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        if response_message.content[-1].type == "tool_use":
            logger.debug("++++++++++++++++++ TOOL USE ++++++++++++++++++")
            tool_use = response_message.content[-1]
            func_name = tool_use.name
            func_params = tool_use.input
            tool_use_id = tool_use.id

            result = self.handle_tool_use(func_name, func_params)
            self.session_state.messages.append(
                    {"role": "assistant", "content": response_message.content}
            )
            self.session_state.messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": f"{result}"
                }]
            })

            follow_up_response = self.generate_message(
                    messages=self.session_state.messages,
                    max_tokens=2048
            )

            if "error" in follow_up_response:
                return f"An error occurred: {follow_up_response['error']}"

            response_text = follow_up_response.content[0].text
            self.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
            )
            return response_text

        elif response_message.content[0].type == "text":
            response_text = response_message.content[0].text
            self.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
            )
            return response_text

        else:
            raise Exception("An error occured: Unexpected response type")


    def handle_tool_use(self, func_name, func_params):
        if func_name == "get_sum":
            logger.debug(f"Calling tool: get_sum, with params: {func_params}")
            sum_value = get_sum(**func_params)
            return f"The sum of {func_params['num1']} and {func_params['num2']} is {sum_value}"
        if func_name == "get_mean":
            logger.debug(f"Calling tool: get_mean, with params: {func_params}")
            mean_value = get_mean(**func_params)
            return f"The mean is {mean_value}"
        if func_name == "get_col_names":
            logger.debug("Calling tool: get_col_names")
            col_names = get_col_names(self.uploaded_file)
            return f"Columns: {col_names}"
        raise Exception("An unexpected tool was used")



