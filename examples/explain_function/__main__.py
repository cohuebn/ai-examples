import inspect
from argparse_prompt import PromptParser
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


def get_function_source(function_name):
    matching_function = locals().get(function_name) or globals().get(function_name)
    return inspect.getsource(matching_function)


def get_cli():
    parser = PromptParser()
    parser.description = "Given a function name for an in-scope function, get that function's source and describe it in plain English"
    parser.add_argument("--function-name", help="The name of the function to explain")
    parser.add_argument(
        "--randomness",
        help="A number between 0-1 representing the randomness of the AI's answers. 0 means responses will be very straight-forward, but potentially less creative. Moving towards 1 will increase randomness in answers",
        type=float,
        default=0.5,
    )
    return parser


load_dotenv()
user_input = get_cli().parse_args()

llm = OpenAI(temperature=user_input.randomness)
template = """Given a function name and source code, generate an English explanation of that function.

Function name: {function_name}
Source:
{function_source}

Function explanation in plain English:
"""
prompt_template = PromptTemplate(
    input_variables=["function_name", "function_source"], template=template
)
function_name = user_input.function_name
function_source = get_function_source(function_name)
chain = LLMChain(llm=llm, prompt=prompt_template)
print(chain.run(function_name=function_name, function_source=function_source))
