from argparse_prompt import PromptParser
from dotenv import load_dotenv
from langchain.llms import OpenAI


def get_cli():
    parser = PromptParser()
    parser.add_argument("--question", help="The question you want to ask")
    parser.add_argument(
        "--randomness",
        help="A number between 0-1 representing the randomness of the AI's answers. 0 means responses will be very straight-forward, but potentially less creative. Moving towards 1 will increase randomness in answers",
        type=float,
        default=0.5,
    )
    return parser


load_dotenv()
user_input = get_cli().parse_args()

language_learning_model = OpenAI(temperature=user_input.randomness)
answer = language_learning_model.predict(user_input.question)

print(f"Answer from AI: {answer}")
