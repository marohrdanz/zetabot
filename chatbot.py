from anthropic import Anthropic
from config import IDENTITY, TOOLS, MODEL, get_sum, get_mean
from dotenv import load_dotenv
import logging


## configure logging
UNDERLINE = '\033[4m'
END = '\033[0m'
YELLOW = '\033[93m'
FORMAT = f"{UNDERLINE}%(asctime)s{END} - {UNDERLINE}%(name)s{END} - {YELLOW}%(levelname)s{END} - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
logging.getLogger('httpcore').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)
logging.getLogger('anthropic').setLevel(logging.ERROR)


load_dotenv()

class ChatBot:
    def __init__(self, session_state):
        self.anthropic = Anthropic()
        self.session_state = session_state

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
        raise Exception("An unexpected tool was used")



