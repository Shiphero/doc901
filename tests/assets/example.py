class ExampleClass:
    """This is an example class."""

    def simple_method(self):
        """This method has low complexity and a docstring."""
        return "Simple method"

    def complex_method_without_docstring(self):
        if True:
            for i in range(5):
                if i % 2 == 0:
                    print(i)
                else:
                    while i < 3:
                        print("Nested complexity")
        # This method has complexity > 5 and no docstring
        pass

    def complex_method_with_docstring(self):
        """
        This method has high complexity but includes a docstring.
        """
        for i in range(5):
            if i % 2 == 0:
                print(i)
            else:
                for j in range(3):
                    if j < 2:
                        print("Another nested loop")
        return "Complex method"


def simple_function():
    """This function has low complexity and a docstring."""
    return "Simple function"


def complex_function_without_docstring():
    for i in range(10):
        if i % 2 == 0:
            for j in range(5):
                if j % 3 == 0:
                    while True:
                        print("Complexity here")
                else:
                    for h in range(3):
                        print(h)
    # This function has complexity > 5 and no docstring
    pass


def complex_function_with_docstring():
    """
    This function has high complexity but includes a docstring.
    """
    for i in range(10):
        if i % 2 == 0:
            for j in range(5):
                if j % 3 == 0:
                    print("Complexity with docstring")
    return "Complex function"
