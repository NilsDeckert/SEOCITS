import pybullet as p
from simulation import Simulation
from robot import SimpleRobot

def main():
    # 1. Initialize the simulation environment
    sim = Simulation()
    
    # 2. Create our robot object
    startPos = [0, 0, 1]
    startOrientation = p.getQuaternionFromEuler([0, 0, 0])
    r2d2 = SimpleRobot("r2d2.urdf", startPos, startOrientation, sim)
    sim.spawn_cube_at([0, -2, 0.5])
    sim.spawn_cube_at([-1, -2, 0.5])
    sim.spawn_cube_at([0, 2, 0.5], color=sim.green)
    sim.spawn_cube_at([-1, 2, 0.5], color=sim.green)
    sim.spawn_cube_at([1, 0, 0.5], color=sim.yellow)
    sim.spawn_cube_at([-1, 0, 0.5], color=sim.yellow)


    #set the center of mass frame (loadURDF sets base link frame)
    p.resetBasePositionAndOrientation(r2d2.id, startPos, startOrientation)
    sim.sleep(2.0)

    r2d2.get_rgb_image()
    sim.sleep(1)

    # 3. Programmatic API usage
    r2d2.move_forward(2.0)
    r2d2.turn(90.0)
    r2d2.move_forward(2.0)
    r2d2.turn(45.0)
    r2d2.move_forward(2.0)

    print("Done! Closing in 2 seconds...")
    sim.sleep(2.0)
    # Clean up
    sim.disconnect()

if __name__ == "__main__":
    main()
