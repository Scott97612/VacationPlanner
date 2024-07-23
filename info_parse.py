from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import json

class Location(BaseModel):
    start: str = Field(description='The starting location of the trip')
    end: str = Field(description='The end location of the trip')
    waypoints: List[str] = Field(description='A list of waypoints on the trip')
    transport: str = Field(description='the transportation method')

class LocationParserTemplate():
    def __init__(self) -> None:
        self.system_instruction = """
        You an agent who converts detailed travel plans into a simple list of locations and transportations used.

        The itinerary will be denoted by ## at the beginning and the end. Convert it into
        list of places that they should visit. Try to include the specific address of each location.

        Your output should always contain the start and end point of the trip, and may also include a list
        of waypoints. It should also include a mode of transit. The number of waypoints cannot exceed 20.
        If you can't infer the mode of transit, make a best guess given the trip location.

        Transit can be only one of the following options: "driving", "walking", "cycling", "public transit", "flight".

        If there are more than 25 waypoints, make sure you only select less than 15 waypoints that you think are the most suitable.

        You should only output a clean json and nothing else, and you don't need to mark it with "```json ```".

        {format_instructions}
    """
        self.user_request = """
        ##{request}##
        """
        
        self.parser = PydanticOutputParser(pydantic_object=Location)
        self.system_message = SystemMessagePromptTemplate.from_template(
            self.system_instruction,
            partial_variables={'format_instructions': self.parser.get_format_instructions()}
        )
        self.user_message = HumanMessagePromptTemplate.from_template(self.user_request, input_variables=['request'])

        self.prompt_template = ChatPromptTemplate.from_messages([self.system_message, self.user_message])

class ParserAgent():
    def __init__(self, model, api_key, temp=0):
        self.model = ChatOpenAI(model=model, temperature=temp, openai_api_key=api_key)
        self.prompt = LocationParserTemplate()
        self.chain = RunnablePassthrough() | self.prompt.prompt_template | self.model | StrOutputParser()

    def parse(self, request):
        result = self.chain.invoke(
            {'request': request, 'format_instructions': self.prompt.parser.get_format_instructions()}
        )
        ###################
        """The output of the function call is like:
            ```json\n
            {...}
            ```\n
            Therefore it needs to be trimmed [8, -4], and load as json so 
            it can be converted into a dictionary.

            This output format may change due to model change.
        """
        try:
            return json.loads(result)
        except Exception as e:
            print(f"It's likely the output format has changed due to model updates. Exact error message: {e}")
