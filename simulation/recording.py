import datetime
import os
import pybullet as p

class Recording:
    def __init__(self):
        self.log_id = None
        self.output_dir = self._get_output_dir()
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_output_dir(self):
        timestamp = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        output_dir = os.getenv("SEOCITS_OUTPUT_DIR")
        if output_dir:
            return output_dir + "/" + timestamp
            
        xdg_videos_dir = os.getenv("XDG_VIDEOS_DIR")
        if xdg_videos_dir:
            return xdg_videos_dir + "/SEOCITS/" + timestamp
            
        return os.path.expanduser("~/Videos/SEOCITS/" + timestamp)

    def start(self):
        title = "recording.mp4"
        self.log_id = p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, f"{self.output_dir}/{title}")

    def stop(self):
        if self.log_id is not None:
            p.stopStateLogging(self.log_id)
            self.log_id = None

    def save_prompts(self, model="unknown", system="", tasks=[], commands=[]):
        with open(self.output_dir + "/prompts.md", "w") as f:
            f.write("# System prompt\n\n")
            f.write(f"Model: {model}\n\n")
            f.write(f"```\n{system}\n```\n\n")
            f.write("# Task prompts\n")
            for i, task in enumerate(tasks):
                f.write(f"## Task {i+1}\n\n```\n" + task + "\n```\n")
            f.write("# Commands executed\n")
            for cmd in commands:
                f.write("- `" + cmd + "`\n")