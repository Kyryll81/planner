from datetime import datetime

from file_utils import get_task, save_file, get_task
from models import Task


def date_input() -> datetime | None:
    try:
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        if date_entry:
            return datetime.strptime(date_entry, '%Y-%m-%d')
        else:
            return datetime.now()
    except ValueError as e:
        print(f"ValueError: {e}")
        return None


def add() -> None:
    title: str = input("Enter task title: ")
    
    while True:
        deadline: datetime | None = date_input()
        if deadline:
            break
    
    tasks: list[Task] | None = get_task()
    if not tasks:
        tasks = []
    id: int = max(map(lambda task: task.id, tasks)) + 1 if tasks else 0
    tasks.append(Task(id=id, title=title, deadline=deadline, done=False))
    save_file(tasks)


def list() -> None:
    tasks: list[Task] | None = get_task()
    
    if not tasks:
        print("Database is empty.")
        return
        
    print("id | title | deadline | done")
    for task in tasks:
        print(*task.model_dump().values(), sep=" | ")


def done() -> None:
    counter: int = 0
    tasks: list[Task] | None = get_task()
    
    if not tasks:
        print("Database is empty.")
        return

    while True:
        id_input: str = input("Enter id of task you had done exit if you want to exit: ")  
        if id_input.isdigit():
            id: int = int(id_input)
            break
        elif id_input == "exit" or counter >= 5:
            return
        counter += 1
    
    for i, task in enumerate(tasks):
        if task.id == id:
            task.done = True
            print("Task is marked!")
            save_file(tasks)
            return
    print("Id is not found.")



def delete():
    counter: int = 0
    tasks: list[Task] | None = get_task()
    
    if not tasks:
        print("Database is empty.")
        return
    
    while True:
        id_input: str = input("Enter id of task you want to delete or exit if you want to exit: ")  
        if id_input.isdigit():
            id: int = int(id_input)
            break
        elif id_input == "exit" or counter >= 5:
            return
        counter += 1
        
    for i, task in enumerate(tasks):
        if task.id == id:
            tasks.pop(i)
            print("Succesfy deleted!")
            save_file(tasks)
            return 
    print("Id is not found.")


if __name__ == "__main__":
    while True:
        print("")
        print("""Hello, user this is console task planner!  
add -> to add task
list -> to list all tasks
done -> to mark task as done
delete -> delete task
exit -> to quit the program""")
        match input():
            case "add":
                add()
            case "list":
                list()
            case "done":
                done()
            case "delete":
                delete()
            case "exit":
                exit()




