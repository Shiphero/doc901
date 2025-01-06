import pytest
from doc901 import main


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setenv("COLOR", "0")
    monkeypatch.setenv("COLUMNS", "120")


def test_default(capsys):
    with pytest.raises(SystemExit):
        main(["./tests/assets/example.py"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [
        "tests/assets/example.py:8: `complex_method_without_docstring` is too complex (5 > 4). Add a docstring.",
        "tests/assets/example.py:38: `complex_function_without_docstring` is too complex (7 > 4). Add a docstring.",
    ]


def test_lower_max(capsys):
    with pytest.raises(SystemExit):
        main(["./tests/assets/example.py", "--max-complexity", "3"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [
        "tests/assets/example.py:8: `complex_method_without_docstring` is too complex (5 > 3). Add a docstring.",
        "tests/assets/example.py:38: `complex_function_without_docstring` is too complex (7 > 3). Add a docstring.",
    ]


def test_higher_max(capsys):
    with pytest.raises(SystemExit):
        main(["./tests/assets/example.py", "--max-complexity", "5"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [
        "tests/assets/example.py:38: `complex_function_without_docstring` is too complex (7 > 5). Add a docstring."
    ]


def test_dir(capsys):
    with pytest.raises(SystemExit):
        main(["./tests/assets/"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [
        "tests/assets/example.py:8: `complex_method_without_docstring` is too complex (5 > 4). Add a docstring.",
        "tests/assets/example.py:38: `complex_function_without_docstring` is too complex (7 > 4). Add a docstring.",
        "tests/assets/example2.py:1: `another_complex_function` is too complex (5 > 4). Add a docstring.",
    ]



def test_multiple_inputs(capsys):
    with pytest.raises(SystemExit):
        main(["./tests/assets/example2.py", "./tests/assets/example.py"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [
        "tests/assets/example.py:8: `complex_method_without_docstring` is too complex (5 > 4). Add a docstring.",
        "tests/assets/example.py:38: `complex_function_without_docstring` is too complex (7 > 4). Add a docstring.",
        "tests/assets/example2.py:1: `another_complex_function` is too complex (5 > 4). Add a docstring.",
    ]


def test_unknown_path(capsys):
    with pytest.raises(SystemExit):
        main(["./messi.py"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == ["messi.py:1: No such file or directory (os error 2)"]


def test_no_errors(capsys):
    main(["./tests/assets/example3.py"])
    result = capsys.readouterr().out.strip().split("\n")
    assert result == [""]

