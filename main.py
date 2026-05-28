from datetime import datetime
import pybullet as p
import time

import config
from simulation import Simulation
from simulation.experiment import ExperimentSetup
from robot import SimpleRobot
from llm.azure import AzureModels
from llm.gemini import GeminiOperator, GeminiModels
from llm.reviewer import Reviewer
from simulation.task import Task, ImageTask
from simulation.task.solution import *

MAX_ATTEMPTS = 1

def spawn_obstacles(sim):
    """
    ..A...B..
    .........
    ....X....
    .........
    ....C....
    """
    sim.spawn_cube_at([2, 2, 1], color=sim.green) # A
    sim.spawn_cube_at([-2, 2, 1], color=sim.red) # B
    sim.spawn_cube_at([0, -2, 1], color=sim.blue) # C

def process_response(response):

    print("")
    print(f"Response: {response}")
    print("")
    
    # Remove everything up to <actions>
    response = response.split("<actions>")[1]
    # Remove everything after </actions>
    response = response.split("</actions>")[0].strip()
    return response

def main():
    # 1. Initialize the simulation environment
    sim = Simulation()
    
    # 2. Create our robot object
    startPos = [0, 0, 1]
    startOrientation = p.getQuaternionFromEuler([0, 0, 0])
    r2d2 = SimpleRobot("r2d2.urdf", startPos, startOrientation, sim)
    spawn_obstacles(sim)

    #set the center of mass frame (loadURDF sets base link frame)
    p.resetBasePositionAndOrientation(r2d2.id, startPos, startOrientation)
    sim.sleep(1.0)
    r2d2.get_rgb_image()
    
    tasks = [
        Task("Turn left 90 degrees", SolutionTurnLeft()),
        Task("Turn right 90 degrees", SolutionTurnRight()),
        Task(
            "Walk 3 meters forward, then turn around and walk back to you original position."
            + "Turn around until you are facing your starting position again.",
            output_dir="Back_forth"),
        Task("Find a green object and touch it. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Touch_Green_object"),
        Task("Find a red object and touch it. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Touch_Red_object"),
        Task("Find a blue object and touch it. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Touch_Blue_object"),
        Task("Walk around the green object. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Circle_green"),
        Task("Walk around the red object. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Circle_red"),
        Task("Walk around the blue object. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Circle_blue"),
        Task("Walk around the each of the objects. "
            + f"The following objects are in your vicinity:\n {sim.get_bodies(r2d2)}",
            output_dir="Circle_all")
    ]

    parent = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    for task in tasks:

        setup = ExperimentSetup(
            model=GeminiModels.FLASH,
            task=task.task,
            runs=[],
        )

        # operator = AzureOperator(MODEL_GPT_5_3_CHAT)
        operator = GeminiOperator(GeminiModels.FLASH)
        if config.review:
            reviewer = Reviewer(AzureModels.GPT_5_MINI)
        r2d2.reset_position()
        sim.reset_objects()

        print("\n"*5)
        print("======================================================")
        print(task.task)
        print("======================================================")
        print("\n"*5)
        sim.sleep(2)
        output = f"{parent}/{task.get_dir()}"
        sim.new_recording(output)

        for _ in range(MAX_ATTEMPTS):
            new_task = None

            print("=======================")
            print(f"Task: {task.get_task()}")
            
            # Task is parent type, so we check for ImageTask first
            if isinstance(task, ImageTask):
                response = operator.instruct_with_image(task.get_task(), task.get_image())
            elif isinstance(task, Task):
                start = time.time()
                response = operator.instruct(task.get_task())
                end = time.time()
                elapsed = end - start
                print(f"Elapsed time: {elapsed} seconds")
            else:
                raise ValueError("Invalid task type")

            response = process_response(response)
            if task.quick_validate(response):
                continue
            if config.review:
                response = reviewer.review(task, response.split("\n"))
                response = process_response(response)
            commands = response.split("\n")
            for cmd in commands:
                print(f" - {cmd}")
            print("=======================")
            print("\n")
            done = False
            message = ""

            for command in commands:
                if command.startswith("#"):
                    print(command)
                    continue
                elif "(" in command and command.endswith(")"):
                    parts = command[:-1].split("(")
                    
                    match parts:
                        case ["move_forward", steps]:
                            print(f"Moving forward by {steps} meters.")
                            r2d2.move_forward(float(steps))
                            operator.add_command_to_history(f"move_forward({steps})")
                            continue                        

                        case ["turn", degrees]:
                            print(f"Turning by {degrees} {config.unit_angle}.")
                            r2d2.turn(float(degrees))
                            operator.add_command_to_history(f"turn({degrees})")
                            continue

                        case ["turn_right", degrees]:
                            print(f"Turning right by {degrees} {config.unit_angle}.")
                            r2d2.turn_right(float(degrees))
                            operator.add_command_to_history(f"turn_right({degrees})")
                            continue

                        case ["turn_left", degrees]:
                            print(f"Turning left by {degrees} {config.unit_angle}.")
                            r2d2.turn_left(float(degrees))
                            operator.add_command_to_history(f"turn_left({degrees})")
                            continue

                        case ["get_lidar_scan", _]:
                            scan = r2d2.get_lidar_scan()
                            task_t = f"Your current lidar scan is: {r2d2.get_lidar_scan()}"
                            new_task = Task(task_t)
                            operator.add_command_to_history(f"get_lidar_scan()")
                            break

                        case ["get_rgb_image", _]:
                            image = r2d2.get_base64_image()
                            operator.add_command_to_history(f"get_rgb_image()")
                            new_task = ImageTask(
                                "Continue your task. This is your POV.",
                                image)
                            break

                        case ["get_environment", _]:
                            info = sim.get_bodies()
                            task_t = f"The current environment is: {info}"
                            new_task = Task(task_t)
                            operator.add_command_to_history(f"get_environment()")
                            break

                        case ["finish", *msgs]:
                            msg = "(".join(msgs)
                            print(f"Mission finished with message: {msg}")
                            done = True
                            message = msg
                            break
                            
                        case [unknown_action, _]:
                            print(f"Error: Recognized format, but unknown action '{unknown_action}'")
                            
                elif command == "":
                    continue
                else:
                    print(f"Error: Invalid command syntax: {command}")
                    sim.sleep(1)

            if new_task:
                task = new_task
            else:
                task_t = f"Continue your task. Your current lidar scan is: {r2d2.get_lidar_scan()}"
                task = Task(task_t)

            if done == True:
                print("\n" * 5)
                print("===============================")
                print("Mission completed successfully!")
                print(message)
                print("===============================")
                print("\n" * 5)
                break

        sim.sleep(3)

        sim.recording.save_prompts(operator)

    # Clean up
    sim.disconnect()

if __name__ == "__main__":
    main()
