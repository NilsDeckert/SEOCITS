class Task:
    def __init__(self, task):
        self.task = task
    
    def get_task(self):
        return self.task
    
class ImageTask(Task):
    def __init__(self, task, image):
        super().__init__(task)
        self.image = image

    def get_image(self):
        return self.image
    