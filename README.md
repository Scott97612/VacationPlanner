### Travel Planner

A fun weekend project where user can give a short vacation idea and it can generate a detailed plan based on the user request and constraints, and also display a interactive map with important stops and route marked.

This project uses LLM through LangChain for validating request, genrating vacation plan as well as parsing important locations from the generated plan. In this case, I used `gpt-4o-mini`. I wanted to try out this new model which according to @sama is "intelligence too cheap to meter". This model is very good for normal use cases and is incredibly CHEAP! The locations suggested by the LLM will be passed to Google Maps API to get relevant coordinates for charting and mapping.

I included a `main.py` file to directly use it in the terminal. For a GUI, you can access it via `webui.py` instead. The front end is built using flask, html, css, and javascript.

## How to use:

`conda create --name EnvName python=3.11`

`conda activate EnvName`

`conda install --file requirements.txt`

create a `.env` file in the root dir, the content see `env_example.txt`

`python main.py` if you want to use terminal or

`python webui.py` to use the Web UI