from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

class PlanningTemplate():
    def __init__(self) -> None:
        self.system_instruction = """
        You are a travel agent who helps users make exciting travel plans.

        The user's request will be denoted by ## at the beginning and the end. Generate
        a detailed itinerary describing the places the user should visit and the things they should do, based on the user request.

        Try to include the specific address of each location.

        Remember to take the user's preferences and timeframe into account,
        and give them an itinerary that would be fun and feasible given their constraints.

        Return the itinerary as plain text of a bulleted list with clear start and end locations.
        Be sure to mention the type of transit for the trip.
        If specific start and end locations are not given, choose ones that you think are suitable and give specific locations.
        
        You should make sure the travel plan number of waypoints don't exceed 15.

        Your output must be only the list and nothing else.
    """
        self.user_request = """
        ##{request}##
        """

        self.system_message = SystemMessagePromptTemplate.from_template(self.system_instruction)
        self.user_message = HumanMessagePromptTemplate.from_template(self.user_request, input_variables=['request'])
        
        self.prompt_template = ChatPromptTemplate.from_messages([self.system_message, self.user_message])

class PlanningAgent():
    def __init__(self, model, api_key, temp=0) -> str:
        self.model = ChatOpenAI(model=model, temperature=temp, openai_api_key=api_key)
        self.prompt = PlanningTemplate()
        self.chain = RunnablePassthrough() | self.prompt.prompt_template | self.model | StrOutputParser()

    def plan(self, request):
        return self.chain.invoke(
            {'request': request}
        )