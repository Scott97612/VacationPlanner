from dotenv import load_dotenv
import os
from validation import ValidationAgent
from plan import PlanningAgent
from info_parse import ParserAgent
from map import Map

load_dotenv('./.env')
openai_api_key = os.getenv('OpenAI_API_Key')
google_maps_api_key = os.getenv('Google_Maps_API_Key')

llm_model = 'gpt-4o-mini'

if __name__ == '__main__':  
    v_agent = ValidationAgent(model=llm_model, api_key=openai_api_key)
    #request = 'I live in south of Dublin, I want to go to famous tourist sites in Italy. I will go around Christmas this year for 3 days. I really enjoy nature and rich culture.'
    request = input('State your travel idea: \n')
    validation = v_agent.validate(request)
    if validation['is_valid'] == 'yes':
        p_agent = PlanningAgent(model=llm_model, api_key=openai_api_key)
        parse_agent = ParserAgent(model=llm_model, api_key=openai_api_key)
        plan = p_agent.plan(request)
        print(f'\nHere is the travel plan: \n{plan}')
        parsed_info = parse_agent.parse(plan)
        start, end, waypoints, transport = parsed_info['start'], parsed_info['end'], parsed_info['waypoints'], parsed_info['transport']
        map = Map(start, end, waypoints, transport, google_maps_api_key)
        map.draw_map()
    else:
        print(f"\nYour plan may be unfeasible, here's the suggestion: \n{validation['revised_plan']}")
    
    