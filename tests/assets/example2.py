def another_complex_function():
    for j in range(5):
        for i in range(10):
            if i % 2 == 0:
                if j % 3 == 0:
                    pass
    return "Complex function"


def yet_another_complex_without_docstring_but_skipped():  # noqa: D103
    for j in range(5):
        for i in range(10):
            if i % 2 == 0:
                if j % 3 == 0:
                    pass
    return "Complex function"
