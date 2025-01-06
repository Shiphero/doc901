# doc901

`doc901` is a simple tool designed to ensure that Python methods and functions with a [high cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) have proper docstrings. It uses [`ruff`](https://docs.astral.sh/ruff/) to analyze complexity and missing docstring on the same line. 

## Why? How?

Maintaining clean and readable code is crucial. Methods or functions with high complexity can be challenging to understand, especially without documentation. 

While `ruff` provides rules for checking complexity ([`C901`](https://docs.astral.sh/ruff/rules/complex-structure/)) and missing docstrings on methods and functions ([`D102`](https://docs.astral.sh/ruff/rules/undocumented-public-method/) and [`D103`](https://docs.astral.sh/ruff/rules/undocumented-public-function/), respectively), there is no built-in way to link them together. Enabling `D10x` project-wide flagging all methods and functions without a docstring (even if they are simple and self-explanatory) could be overwhelming in large projects. 

`doc901` bridges this gap by flagging errors only when the complexity is enough to demand a docstring, so you can improve your code incrementally,  

Of course, the name comes after the C901 rule code ;-) 

## Use and install

The easiest way is via [`uvx`](https://docs.astral.sh/uv/guides/tools/). 

``` 
uvx doc901 path/to/file.py
```

To analyze an entire directory:

```bash
uvx doc901 path/to/directory/
```

The default allowed complexity is 4, meaning any function or method with McCabe 5 or more will require a docstring. 

```bash
uvx doc901 --max-complexity=3 path/to/file.py 
```

See `--help` for more options.

To install the tool permanently:

```bash
uv tool install doc901
```

## Example

Imagine you have a file `example.py` with the following methods:

```python
def complex_function_without_docstring():
    for i in range(10):
        if i % 2 == 0:
            for j in range(5):
                print(i, j)
```

Running `doc901` on this file:

```bash
python doc901.py example.py
```

Output:

```
example.py:1: `complex_function_without_docstring` is too complex (5 > 4). Add a docstring.
```

## Contribution

Feel free to open issues or submit pull requests if you encounter bugs or have suggestions for improvement. This tool is lightweight but can be extended to cover more advanced checks.

## License

This project is open-source and available under the MIT License. See the [LICENSE](./LICENSE) file for details.
