import tkinter as tk
from ui import UI
from checklist import JobManager
from voice import VoiceHandler

root = tk.Tk()
job_manager = JobManager()
voice_handler = VoiceHandler()

app = UI(root, job_manager, voice_handler)
root.mainloop()
