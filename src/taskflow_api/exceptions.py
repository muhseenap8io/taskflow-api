class TaskNotFoundException(Exception):
    def __init__(self,task_id:int):
        self.task_id = task_id        