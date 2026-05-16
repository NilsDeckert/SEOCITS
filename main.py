from numpy.lib import scimath
import pybullet as p
from simulation import Simulation
from robot import SimpleRobot
from llm import OpenAIOperator, Task, ImageTask

MAX_ATTEMPTS = 0

def spawn_obstacles(sim):
    sim.spawn_cube_at([2, 2, 1], color=sim.green)
    sim.spawn_cube_at([-2, 2, 1], color=sim.red)

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
    sim.sleep(2.0)
    r2d2.get_rgb_image()

    operator = OpenAIOperator()
    
    # task = Task(f"Drive to the nearest object and identify its color. Your current lidar scan is the following: {r2d2.get_lidar_scan()}. Index 0 is right in front. All other distances are in 45° steps, counter-clockwise.")
    task = Task(f"Find a red object and touch it. Your current lidar scan is the following: {r2d2.get_lidar_scan()}.")

    for _ in range(MAX_ATTEMPTS):
        new_task = None
        
        # Task is parent type, so we check for ImageTask first
        if isinstance(task, ImageTask):
            response = operator.instruct_with_image(task.get_task(), task.get_image())
        elif isinstance(task, Task):
            response = operator.instruct(task.get_task())
        else:
            raise ValueError("Invalid task type")

        response = process_response(response)
        commands = response.split("\n")
        print("=======================")
        print(f"Task: {task.get_task()}")
        for cmd in commands:
            print(f" - {cmd}")
        print("=======================")
        print("\n")
        done = False
        message = ""

        for command in commands:
            if "(" in command and command.endswith(")"):
                parts = command[:-1].split("(")
                
                match parts:
                    case ["move_forward", steps]:
                        print(f"Moving forward by {steps} units.")
                        r2d2.move_forward(float(steps))
                        operator.add_command_to_history(f"move_forward({steps})")
                        
                    case ["turn", degrees]:
                        print(f"Turning by {degrees} degrees.")
                        r2d2.turn(float(degrees))
                        operator.add_command_to_history(f"turn({degrees})")

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

                    case ["finish", *msgs]:
                        msg = "(".join(msgs)
                        print(f"Mission finished with message: {msg}")
                        done = True
                        message = msg
                        break
                        
                    case [unknown_action, _]:
                        print(f"Error: Recognized format, but unknown action '{unknown_action}'")
                        
            else:
                print("Error: Invalid command syntax.")
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

    sim.sleep(10)

    # Clean up
    sim.disconnect()

if __name__ == "__main__":
    main()
