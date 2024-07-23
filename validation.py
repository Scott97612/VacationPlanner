from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from datetime import date
import json


class Validate(BaseModel):
    is_valid: str = Field(description='This field is "yes" if the travel plan is valid, otherwise "no". ')
    revised_plan: str = Field(description='This field is for your revised travel plan. ')
    date: str = Field(description='The starting date of the trip')

class ValidationTemplate:
    def __init__(self) -> None:
        self.system_instruction = """
        You are a helpful travel agent that helps validate user's travel requests.

        User request will be indicated using ## at the beginning and at the end.

        Here are some basic criteria for validating user's request:
        1. The request should mention valid geographical locations for travel.
        2. The request should mention reasonable time frame for the travel plan.
        3. The request should be reasonable based on common sense.
        4. The requested locations should be plannable within requested time frame.

        You should also give the starting date based on user request. If user did not 
        mention starting date, infer it from the request using current date: {current_date}. 
        Current date format is yyyy-mm-dd, but the date you output should be formatted as dd-mm-yyyy.

        You should only output a clean json and nothing else, and you don't need to mark it with "```json ```".

        {format_instructions}
    """
        self.user_request = """
        ##{request}##
    """
        self.parser = PydanticOutputParser(pydantic_object=Validate)

        self.system_message = SystemMessagePromptTemplate.from_template(
            self.system_instruction,
            partial_variables={"format_instructions": self.parser.get_format_instructions(), 'current_date': str(date.today())}
        )

        self.user_message = HumanMessagePromptTemplate.from_template(self.user_request, input_variables=["request"])

        self.prompt_template = ChatPromptTemplate.from_messages([self.system_message, self.user_message])

class ValidationAgent():
    def __init__(self, model, api_key, temp=0):
        self.model = ChatOpenAI(model=model, temperature=temp, openai_api_key=api_key)
        self.prompt = ValidationTemplate()
        self.chain = RunnablePassthrough() | self.prompt.prompt_template | self.model | StrOutputParser()

    def validate(self, request):
        validation = self.chain.invoke(
            {'request': request, 'format_instructions': self.prompt.parser.get_format_instructions(), 'current_date': str(date.today())}
        )
        try:
            return json.loads(validation)
        except Exception as e:
            print(f"It's likely the output format has changed due to model updates. Exact error message: {e}")




