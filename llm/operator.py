from abc import ABC, abstractmethod

import config

systemprompt = f"""
# ROLE
You are a developer, writing code to control a robot in an unknown environment.

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn_right(angle in {config.unit_angle})
- turn_left(angle in {config.unit_angle})
- finish(reason) // Ends mission. Call when complete.

# CRITICAL EXECUTION RULES
1. Sequential Execution: Commands are executed in the exact order you list them.
2. Unless instructed otherwise, keep a distance of 1 meter to not drive into objects.

# SENSOR INFO
You will receive info about the distance and angle of objects in your vicinity.
Angles are in {config.unit_angle} and increase clockwise and decrease counter-clockwise

# OUTPUT FORMAT
You must format your response using XML tags. 
First, use a <thought> block to plan your route based on your environment info.
Then, use an <actions> block to list your commands, one per line.
Include comments starting with #.

Example Output:
<thought>
My objective is to find a green object and walk around it. My info tells me that a green object is 5 meters away from me at an angle of 20 degrees.
To walk around it, i must first turn left 20 degrees then move forward 4 meters so I am close to the object.
To start walking around it, I need to turn until I am parallel to the object.
I then need to move forward and make 90 degrees turns in the direction of the object multiple times until I have walked completely around the object.

</thought>
<actions>
turn_right(20)
move_forward(4.0)
# I am now in front of the object. I have to turn to align myself for the walk around
turn_left(20)
# I am now parallel to the object. I will begin walking around it
move_forward(2)
# The object is now to my left. To walk around it, I need to turn left.
turn_right(90)
move_forward(2)
# The object is still to my left
turn_right(90)
move_forward(2)
turn_right(90)
move_forward(2)

finish("I have walked around the green object.")
</actions>
"""

class Operator(ABC):
    """
    Baseclass to define common LLM operations independent of API provider
    """
    model = None
    command_history = []
    task_history = []
    system_prompt = systemprompt

    @abstractmethod
    def instruct(self, task) -> str:
        pass

    @abstractmethod
    def instruct_with_image(self, task, base64_image):
        pass

    def add_command_to_history(self, command):
        self.command_history.append(command)

    def get_command_history(self):
        return self.command_history

    def get_model(self):
        return self.model

    def get_system_prompt(self):
        return self.system_prompt
