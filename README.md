# planner
CLI-застусунок який реалізує планувальник завдань. Які зберігаються у форматі JSON.

## Функціонал
* Додавння завдання з дедлайном.
* Перегляд списку завдань.
* Позначення виконаних завдань.
* Видалення завдань.
* Збереження у файлі "tasks.json"

## Як встановити
Після встановлення репозитоію необхідно у директорії застусунку встановити файл .venv (За умов що попередньо встановлений Python)
```
python3 -m venv .venv
```
Після необхідно запустити вірутальне середовище за допомогою
```
source .venv/bin/activate # для linux-систем
```
або
```
source .venv/Scripts/activate # для Windows  
```
І встановити залежності.
```
pip install -r requirements.txt
```
Встановлення програми можна вважати завершеним.

## Як запустити

За допомогою команди:
```
python planner.py
```
Інтерфейс складається з п'яти команд:
```
add -> додати завдання
list -> вивести всі завдання у консоль
done -> позначити завдання як  виконане
delete -> видалити завдання
exit -> завершити програму
```

## Приклад використання
```
(.venv) kyrylo@kyrylo-VivoBook-ASUSLaptop-X570ZD-X570ZD:/media/kyrylo/Новий том1/Python_projects/planner$ python planner.py

Hello, user this is console task planner!  
add -> to add task
list -> to list all tasks
done -> to mark task as done
delete -> delete task
exit -> to quit the program
list
id | title | deadline | done
0 | 5 | 2012-11-23 00:00:00 | True

Hello, user this is console task planner!  
add -> to add task
list -> to list all tasks
done -> to mark task as done
delete -> delete task
exit -> to quit the program
```

###  Команда add
```
add
Enter task title: t
Enter a date in YYYY-MM-DD format: 2020-10-02
File is saved
```

###  Команда list
```
list
id | title | deadline | done
0 | 5 | 2012-11-23 00:00:00 | True
```

###  Команда done
```
done
Enter id of task you had done exit if you want to exit: 1
Task is marked!
File is saved
```

### Команда exit
Завершує програму

## Як тестувати

 ```
 pytest
 ```
 Або якщо потрібно запустити конкрентий тест
 ```
 pytest test_planner.py::test_delete
 ```