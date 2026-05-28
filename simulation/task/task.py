from simulation.task import Solution

class Task:
    def __init__(self, task: str, solution: Solution | None = None, output_dir=None):
        self.task: str = task
        self.solution: Solution | None = solution

        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = "_".join(task.split(" ")[:3])
    
    def get_task(self) -> str:
        return self.task

    def get_dir(self):
        return self.output_dir

    def quick_validate(self, proposal) -> bool:
        """
        Check if commands are in list of accepted solutions.
        """
        if self.solution is not None:
            return self.solution.validate(proposal)
        else:
            return False

    def validate(self) -> bool:
        """
        Ask user for feedback if task was solved
        """
        i = None
        while i not in ["y", "n"]:
            print("\n" * 5)
            print("============")
            print(self.task)
            print("============")
            print("\n" * 5)
            i = input("Was this task solved? (y/n):")

        if i == "y":
            print("✅ Task was solved successfully!")
            return True
        else:
            print("❌ Task was not solved!")
            return False

    def __str__(self):
        return self.task

    def __repr__(self):
        return self.task

    
class ImageTask(Task):
    def __init__(self, task, image):
        super().__init__(task)
        self.image = image

    def get_image(self):
        return self.image
    