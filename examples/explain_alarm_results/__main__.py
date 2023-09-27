from argparse_prompt import PromptParser
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def get_cli():
    parser = PromptParser()
    parser.add_argument(
        "--alarm-definition-filename",
        help="The filename of the file that holds alarm definition JSON",
    )
    parser.add_argument(
        "--timeseries-filename",
        help="The filename of the file that holds the timeseries of evaluated alarm data",
    )
    parser.add_argument(
        "--randomness",
        help="A number between 0-1 representing the randomness of the AI's answers. 0 means responses will be very straight-forward, but potentially less creative. Moving towards 1 will increase randomness in answers",
        type=float,
        default=0.5,
    )
    return parser


def load_file_as_text(filename: str) -> str:
    with open(filename) as file:
        return file.read()


load_dotenv()
user_input = get_cli().parse_args()

rule_definition = load_file_as_text(user_input.alarm_definition_filename)
results_timeseries = load_file_as_text(user_input.timeseries_filename)


llm = OpenAI(temperature=user_input.randomness, model="davinci-002")
template = """You are a DeFi data analyst. You are given two pieces of information from a blockchain rule evaluation engine:
1. A rule definition: This is JSON representing a "rule". A rule is capable of querying blockchain data, returning that data as a timeseries of results,
and each datapoint in those results to a threshold. If that threshold is breached, an "alarm" should be triggered to indicate
an interesting event occurred at that point-in-time.
2. A timeseries of results: This is the actual blockchain data that was found using the "data" property on the alarm definition.
The alarm definition is a custom DSL that allows executing SQL queries

Your task is to:
1. Use the rule definition to understand what the rule is representing in plain English.
2. Translate the timeseries results into something a non-technical person could use to understand what happened.

Rule definition:
{rule_definition}

Timeseries of results:
{results_timeseries}

Results:
"""
prompt_template = PromptTemplate(
    input_variables=["rule_definition", "results_timeseries"], template=template
)
results = LLMChain(llm=llm, prompt=prompt_template)
print(
    results.run(rule_definition=rule_definition, results_timeseries=results_timeseries)
)
