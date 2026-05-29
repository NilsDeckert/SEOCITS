from abc import ABC
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
