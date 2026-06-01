from abc import ABC
import itertools
import config

class Solution(ABC):
    accepted: list[str]

    def validate(self, proposal: list[str]) -> bool:
        """
        Check if the proposal is in the list of accepted solutions

        @note: Returning False does not mean the solution is wrong!

        @param: proposal: The proposed solution
        @return: True or False
        """

        # Remove comments, finish()
        filtered = []
        for line in proposal:
            if line.startswith("#"):
                continue
            if line.startswith("finish("):
                continue
            filtered.append(line)
        proposal = "\n".join(filtered)

        if proposal in self.accepted:
            return True
        else:
            return False

class SolutionTurnLeft(Solution):
    """Optimal Solution for task 'turn left 90 degrees'"""
    def __init__(self):
        if config.use_degrees:
            self.accepted = [
                "turn_left(90)",
                "turn_left(90,0)",
                "turn_left(90.0)",
            ]
        else:
            self.accepted = [
                "turn_left(1,57)",
                "turn_left(1,570)",
                "turn_left(1,5708)",
                "turn_left(1.57)",
                "turn_left(1.570)",
                "turn_left(1.5708)",
            ]
class SolutionTurnRight(Solution):
    """Optimal Solution for task 'turn right 90 degrees'"""
    def __init__(self):
        if config.use_degrees:
            self.accepted = [
                "turn_right(90)",
                "turn_right(90,0)",
                "turn_right(90.0)",
            ]
        else:
            self.accepted = [
                "turn_right(1,57)",
                "turn_right(1,570)",
                "turn_right(1,5708)",
                "turn_right(1.57)",
                "turn_right(1.570)",
                "turn_right(1.5708)",
            ]

class SolutionBackForth(Solution):
    """Optimal Solution for task 'Walk 3 meters forward, then turn around and walk back to your original position.'"""

    def __init__(self):
        # 1. Define valid move commands
        moves = [
            "move_forward(3)",
            "move_forward(3.0)",
            "move_forward(3,0)"
        ]

        # 2. Define valid turn commands based on config
        if config.use_degrees:
            vals = ["180", "180.0", "180,0"]
        else:
            vals = ["3.14", "3.141", "3.1416", "3.14159", "3.141593", "3.1415926",
                    "3,14", "3,141", "3,1416", "3,14159", "3,141593", "3,1415926"]

        turns = [f"turn_left({v})" for v in vals] + [f"turn_right({v})" for v in vals]

        # 3. Generate all combinations cleanly
        self.accepted = []
        for m1, t1, m2, t2 in itertools.product(moves, turns, moves, turns):
            # Using join() ensures there is no accidental leading/trailing whitespace
            # from the Python code's own indentation level.
            solution_string = '\n'.join([m1, t1, m2, t2])

            self.accepted.append(solution_string)