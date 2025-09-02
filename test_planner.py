import pytest
import json

from datetime import datetime, timezone

from unittest.mock import MagicMock, patch, mock_open

from models import Task
from file_utils import get_task, save_file
from planner import add, list, done, delete


@pytest.fixture
def database_data():
    return {"id": 1, 
            "title": "title", 
            "deadline": datetime.now(timezone.utc).isoformat(), 
            "done": False}


@pytest.fixture
def model_data_list():
    return [Task(id=1, 
             title="title", 
             deadline=datetime.now(), 
             done=False)]


def test_get_task_with_valid_id(database_data):
    data_list: list[dict] = [database_data]
    
    mock_file = mock_open(read_data=json.dumps(data_list))
    with patch("builtins.open", mock_file):
        result = get_task(1)
                
    assert result == Task(**database_data)
    mock_file.assert_called_once_with("tasks.json", "r")


def test_get_task_with_no_id(database_data):
    data_list: list[dict] = [database_data]
    
    mock_file = mock_open(read_data=json.dumps(data_list))
    with patch("builtins.open", mock_file):
        result = get_task()
        assert result == [Task(**database_data)]
        
        result = get_task(-1)
        assert result == [Task(**database_data)]
    
    mock_file.assert_called_with("tasks.json", "r")


def test_get_task_with_wrong_id(database_data, capsys):
    data_list: list[dict] = [database_data]
    
    mock_file = mock_open(read_data=json.dumps(data_list))
    with patch("builtins.open", mock_file):
        result = get_task(-2)
                
    assert result == None
    mock_file.assert_called_once_with("tasks.json", "r")


def test_get_task_with_empty_file(capsys):
        mock_file = mock_open(read_data="")
        with patch("builtins.open", mock_file):
            result = get_task()
            captured = capsys.readouterr()
        
        assert "JSONDecodeError" in captured.out
        assert result == None


def test_get_task_with_unkown_exception(capsys):
        with patch("builtins.open", side_effect=RuntimeError("Something went wrong!")):
            result = get_task()
            captured = capsys.readouterr()
        
        assert result is None
        assert "Exception: Something went wrong!" in captured.out


def test_save_file(model_data_list, capsys):    
    with patch("builtins.open", mock_open()) as mock_file:
        with patch("json.dump") as mock_json_dump:
            result = save_file(model_data_list)
    captured = capsys.readouterr()
    assert "File is saved" in captured.out
    assert result == None
    mock_file.assert_called_once_with("tasks.json", "w")
    mock_json_dump.assert_called_once()


def test_save_file_with_exception(capsys):
        with patch("json.dump", side_effect=Exception("Unkown exception")) as mock_json_dump:
            save_file([])
            captured = capsys.readouterr()
            assert "Exception: Unkown exception" in captured.out


def test_add_with_gotten_list(model_data_list):
    with patch("builtins.input", return_value="title") as mock_input:
        with patch("planner.date_input", return_value=datetime.now()) as mock_date_input:
            with patch("planner.get_task", return_value=model_data_list.copy()) as mock_get_task:
                with patch("planner.save_file") as mock_save_file:
                    add()
    
    mock_input.assert_called_once()
    mock_date_input.assert_called_once()
    mock_get_task.assert_called_once()
    saved_tasks = mock_save_file.call_args[0][0]  # The first argument passed to save_file
    assert len(saved_tasks) == len(model_data_list) + 1
    assert saved_tasks[-1].title == "title"
    assert saved_tasks[-1].done is False


def test_add_with_empty_list():
    with patch("builtins.input", return_value="title") as mock_input:
        with patch("planner.date_input", return_value=datetime.now()) as mock_date_input:
            with patch("planner.get_task", return_value=None) as mock_get_task:
                with patch("planner.save_file") as mock_save_file:
                    add()
    
    mock_input.assert_called_once()
    mock_date_input.assert_called_once()
    mock_get_task.assert_called_once()
    saved_tasks = mock_save_file.call_args[0][0]  # The first argument passed to save_file
    assert len(saved_tasks) == len([]) + 1
    assert saved_tasks[-1].title == "title"
    assert saved_tasks[-1].done is False
    

def test_list(model_data_list, capsys):
    with patch("planner.get_task", return_value=model_data_list) as mock_get_task:
        list()
    
    captured = capsys.readouterr()
    assert "id | title | deadline | done" in captured.out 


def list_empty_db(capsys):
    with patch("planner.get_task", return_value=None) as mock_get_task:
        list()
    
    captured = capsys.readouterr()
    assert "Database is empty." in captured.out
    mock_get_task.assert_called_once()


def test_done(model_data_list) -> None:
    with patch("planner.get_task", return_value=model_data_list) as mock_get_task:
        with patch("builtins.input", return_value="1") as mock_id_input:
            with patch("planner.save_file") as mock_save_file:
                done()
                                
    mock_get_task.assert_called_once()
    mock_id_input.assert_called_once()
    mock_save_file.assert_called_once_with(mock_get_task.return_value)


@pytest.mark.parametrize("input", [ "", "exit", "6"])
def test_done_wrong_input(input, model_data_list) -> None:
    with patch("planner.get_task", return_value=model_data_list) as mock_get_task:
        with patch("builtins.input", return_value=input):
            with patch("planner.save_file") as mock_save_file:
                done()

    mock_save_file.assert_not_called()


def test_done_empty_db(capsys) -> None:
    with patch("planner.get_task", return_value=[]):
        with patch("planner.save_file") as mock_save_file:
                done()

    captured = capsys.readouterr()
    assert "Database is empty." in captured.out

    mock_save_file.assert_not_called()


def test_done_not_found_id(capsys, model_data_list) -> None:
    with patch("planner.get_task", return_value=model_data_list) as mock_get_task:
        with patch("planner.save_file") as mock_save_file:
            with patch("builtins.input", return_value="5"):
                done()

    captured = capsys.readouterr()
    assert "Id is not found." in captured.out

    mock_save_file.assert_not_called()


def test_delete_empty_db(capsys):
    with patch("planner.get_task", return_value=[]):
        with patch("planner.save_file") as mock_save_file:
                delete()

    captured = capsys.readouterr()
    assert "Database is empty." in captured.out

    mock_save_file.assert_not_called()


@pytest.mark.parametrize("input", [ "", "exit", "6"])
def test_delete_wrong_input(input, ):
    with patch("planner.get_task", return_value=[]):
        with patch("planner.save_file") as mock_save_file:
            with patch("builtins.input", return_value = input):
                delete()

    mock_save_file.assert_not_called()


def test_delete(model_data_list):
    with patch("planner.get_task", return_value=model_data_list):
        with patch("planner.save_file") as mock_save_file:
            with patch("builtins.input", return_value = "1"):
                delete()

    mock_save_file.assert_called_once()