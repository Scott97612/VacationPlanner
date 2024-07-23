from flask import Flask, request, render_template, jsonify, url_for
from dotenv import load_dotenv
import os
from validation import ValidationAgent
from plan import PlanningAgent
from info_parse import ParserAgent
from map import Map

app = Flask(__name__)

def run_backend(user_request): # return validation, plan, map
    load_dotenv('./.env')
    openai_api_key = os.getenv('OpenAI_API_Key')
    google_maps_api_key = os.getenv('Google_Maps_API_Key')
    llm_model = 'gpt-4o-mini'

    v_agent = ValidationAgent(model=llm_model, api_key=openai_api_key)
    validation = v_agent.validate(user_request)
    if validation['is_valid'] == 'yes':
        p_agent = PlanningAgent(model=llm_model, api_key=openai_api_key)
        parse_agent = ParserAgent(model=llm_model, api_key=openai_api_key)
        plan = p_agent.plan(user_request)
        parsed_info = parse_agent.parse(plan)
        start, end, waypoints, transport = parsed_info['start'], parsed_info['end'], parsed_info['waypoints'], parsed_info['transport']
        map = Map(start, end, waypoints, transport, google_maps_api_key)
        map.draw_map()
        return 'Plan is feasible!', plan, url_for('route_map')
    else:
        return validation['revised_plan'], None, None

# pre-render the embedded htmls
@app.route('/default_map')
def default_map():
    return render_template('default_map.html')

@app.route('/route_map')
def route_map():
    return render_template('route_map.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        user_request = request.form.get('user_request')
        if user_request != None:
            validation, plan, map = run_backend(user_request=user_request)
        
        return jsonify({'validation': validation, 'plan':  plan, 'map': map})
    
if __name__ == '__main__':
    app.run()


