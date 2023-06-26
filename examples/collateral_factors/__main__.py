from argparse_prompt import PromptParser
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import create_pandas_dataframe_agent

from index_data.collateral_factor import load_collateral_factor_data


def get_cli():
    parser = PromptParser()
    parser.add_argument("--token", help="The token to get collateral factor for")
    parser.add_argument(
        "--target-date",
        help="The target date/time to get the collateral factor. Use ISO8601 format. Defaults to now",
    )
    parser.add_argument(
        "--randomness",
        help="A number between 0-1 representing the randomness of the AI's answers. 0 means responses will be very straight-forward, but potentially less creative. Moving towards 1 will increase randomness in answers",
        type=float,
        default=0.5,
    )
    return parser


load_dotenv()
user_input = get_cli().parse_args()
token = user_input.token
target_time = (
    parse_datetime(user_input.target_date) if user_input.target_date else datetime.now()
)

llm = OpenAI(temperature=user_input.randomness)
collateral_factor_data = load_collateral_factor_data(token, target_time, "14 days")

collateral_factor_predictor = create_pandas_dataframe_agent(
    llm=llm,
    df=[collateral_factor_data["collateral_factors"], collateral_factor_data["prices"]],
)
question = f"You are a crypto lending pool. What should the collateral factor for {token} be on {target_time}?"
print(collateral_factor_predictor.run(question))
