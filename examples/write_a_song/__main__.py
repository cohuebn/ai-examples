from argparse_prompt import PromptParser
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def get_cli():
    parser = PromptParser()
    parser.add_argument("--words", help="Words to include in the song")
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
template = """You are a song writer. Given a list of words, you must write a song using all of those words.

Words:
{words}

Song:
"""
prompt_template = PromptTemplate(input_variables=["words"], template=template)
recipe = LLMChain(llm=llm, prompt=prompt_template)
print(recipe.run(user_input.words))
