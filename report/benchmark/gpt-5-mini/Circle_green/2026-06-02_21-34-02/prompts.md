# System prompt

Model: gpt-5.3-chat

```

# ROLE
You are a developer, writing code to control a robot in an unknown environment.

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn_right(angle in degrees)
- turn_left(angle in degrees)
- finish(reason) // Ends mission. Call when complete.

# CRITICAL EXECUTION RULES
1. Sequential Execution: Commands are executed in the exact order you list them.
2. Unless instructed otherwise, keep a distance of 1 meter to not drive into objects.

# SENSOR INFO
You will receive info about the distance and angle of objects in your vicinity.
Angles are in degrees and increase clockwise and decrease counter-clockwise

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

```

# Task prompts
## Task 1

```
Walk around the green object. The following objects are in your vicinity:
 - rgba(0, 1, 0, 1) cube of width 1.0, height 2 and length 1.0.
  Corner 1: 2.12 meters away at -315.0 degrees.
Corner 2: 2.92 meters away at -329.04 degrees.
Corner 3: 2.92 meters away at -300.97 degrees.
Corner 4: 3.54 meters away at -315.0 degrees.

- rgba(1, 0, 0, 1) cube of width 1.0, height 2 and length 1.0.
  Corner 1: 2.92 meters away at -59.04 degrees.
Corner 2: 3.54 meters away at -45.0 degrees.
Corner 3: 2.12 meters away at -45.0 degrees.
Corner 4: 2.92 meters away at -30.96 degrees.

- rgba(0, 0, 1, 1) cube of width 1.0, height 2 and length 1.0.
  Corner 1: 2.55 meters away at -168.69 degrees.
Corner 2: 1.58 meters away at -161.56 degrees.
Corner 3: 2.55 meters away at -191.31 degrees.
Corner 4: 1.58 meters away at -198.44 degrees.


```
# Commands executed
- `turn_right(45)`
- `move_forward(1.1)`
- `turn_left(45)`
- `move_forward(2)`
- `turn_right(90)`
- `move_forward(2)`
- `turn_right(90)`
- `move_forward(2)`
- `turn_right(90)`
- `move_forward(2)`
- `turn_right(90)`
