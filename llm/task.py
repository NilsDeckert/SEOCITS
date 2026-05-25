class Task:
    def __init__(self, task, output_dir=None):
        self.task = task
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = "_".join(task.split(" ")[:3])
    
    def get_task(self):
        return self.task

    def get_dir(self):
        return self.output_dir

    
class ImageTask(Task):
    def __init__(self, task, image):
        super().__init__(task)
        self.image = image

    def get_image(self):
        return self.image
    