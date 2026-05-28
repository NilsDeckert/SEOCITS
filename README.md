# Seminar: Operating Complex IT systems

The repository explores the usage of relative coordinates for a LLM controlled robot. 
The idea is to provide a LLM with a simple api to control a robot, giving it tasks to complete in the environment.

## Usage

Install requirements, then run the `main.py` script:
```bash
pip install -r requirements.txt
python main.py
```

## Project Structure
- `llm` - Wrappers to interact with LLMs
  - `reviewer.py` - Review plans made by class below
  - `openai.py` - Main class to get robot control commands
- `simulation/` - Simulation environment
- `robot/` - Robot API and sensors
  - `sensors/` - Available robot sensors
  - `simple_robot.py` - Simple robot API wrapper
- `config.py` - File to save and edit settings
- `main.py` - Main script
