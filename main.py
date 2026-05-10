import pybullet as p
from simulation import Simulation
from robot import SimpleRobot
from llm import OpenAIOperator

def main():
    # 1. Initialize the simulation environment
    sim = Simulation()
    
    # 2. Create our robot object
    startPos = [0, 0, 1]
    startOrientation = p.getQuaternionFromEuler([0, 0, 0])
    r2d2 = SimpleRobot("r2d2.urdf", startPos, startOrientation, sim)
    sim.spawn_cube_at([0, -2, 1])
    # sim.spawn_cube_at([-1, -2, 0.5])
    # sim.spawn_cube_at([0, 2, 0.5], color=sim.green)
    # sim.spawn_cube_at([-1, 2, 0.5], color=sim.green)
    # sim.spawn_cube_at([2, 0, 0.5], color=sim.yellow)
    # sim.spawn_cube_at([-2, 0, 0.5], color=sim.yellow)


    #set the center of mass frame (loadURDF sets base link frame)
    p.resetBasePositionAndOrientation(r2d2.id, startPos, startOrientation)
    sim.sleep(2.0)
    r2d2.get_rgb_image()

    operator = OpenAIOperator()

    for _ in range(4):
        task = f"Drive to the nearest object and touch it. Your current lidar scan is the following: {r2d2.get_lidar_scan()}. Index 0 is right in front. All other distances are in 45° steps, counter-clockwise."
        response = operator.new_mission(task)
        commands = response.split("\n")
        print(f"{response=}")
        done = False

        for command in commands:
            if "(" in command and command.endswith(")"):
                parts = command[:-1].split("(")
                
                match parts:
                    case ["move_forward", steps]:
                        print(f"Moving forward by {steps} units.")
                        r2d2.move_forward(float(steps))
                        
                    case ["turn", degrees]:
                        print(f"Turning by {degrees} degrees.")
                        r2d2.turn(float(degrees))

                    case ["finish", msg]:
                        print(f"Mission finished with message: {msg}")
                        done = True
                        break
                        
                    case [unknown_action, _]:
                        print(f"Error: Recognized format, but unknown action '{unknown_action}'")
                        
            else:
                print("Error: Invalid command syntax.")
                sim.sleep(1)

        if done == True:
            break

    sim.sleep(10)

    # Clean up
    sim.disconnect()

if __name__ == "__main__":
    main()
