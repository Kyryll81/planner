import json
from models import Task


def save_file(tasks: list[Task]) -> None:
    try:
        with open("tasks.json", "w") as file:
            json.dump([task.model_dump() for task in tasks], file, default=str)
            print("File is saved")
    except Exception as e:
        print("Problem in save stage.")
        print(f"Exception: {e}")



# must be throw try-except
def get_task(id: int = -1) -> list[Task] | Task | None:
    """Returns task if id is given. In other case return all tasks"""
    try:
        with open("tasks.json", "r") as file:
            tasks: list[dict]  = json.load(file)
 
            if id == -1:
                return [Task(**task) for task in tasks]
            
            for task in tasks:
                if task.get("id") == id:
                    return Task(**task)
            
            print("Task id is not found.")
            return None
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None
