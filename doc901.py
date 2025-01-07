"""
Enforce docstrings on complex function and methods
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import re


from rich import print

__version__ = "0.2"
here = Path.cwd().resolve()


def parse_name(message):
    """parse the function name from a message"""
    if match := re.search(r"`([^`]*)`", message):
        return match.group(1)


def parse_complexity(message):
    """parse the complexity from a message"""
    if match := re.search(r"\b(\d+)\b", message):
        return int(match.group(1))


def analyze_complexity_with_docstrings(
    files: list, max_complexity: int, excludes: list, ignored_violations: set = set(), as_json: bool = False
):
    """
    Run Ruff with a custom config to check methods with high complexity
    and missing docstrings.
    """
    # Run Ruff with the specified configuration
    command = [
        "ruff",
        "check",
        "-e",
        "--config",
        f"lint.mccabe.max-complexity={max_complexity}",
        "--select",
        "C901",
        "--select",
        "D102",
        "--select",
        "D103",
        "--select",
        "E902",
        "--output-format",
        "json",
    ]
    for exclude in excludes:
        command += ["--exclude", exclude]
    command += files

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode not in [0, 1]:
        print("Error running Ruff:", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    # Parse Ruff results
    issues = json.loads(result.stdout)

    # special case, path not found
    if issues and issues[0]["code"] == "E902":
        print(
            f"[bold red]{Path(issues[0]['filename']).relative_to(here)}:{issues[0]['location']['row']}[/bold red]: {issues[0]['message']}"
        )
        sys.exit(1)

    new_complexity_issues = {
        (issue["filename"], int(issue["noqa_row"])): issue["message"]
        for issue in issues
        if issue["code"] == "C901"
        if (str(Path(issue["filename"]).relative_to(here)), parse_name(issue["message"])) not in ignored_violations
    }

    docstring_issues = {(issue["filename"], issue["noqa_row"]) for issue in issues if issue["code"].startswith("D1")}
    # Identify violations: complexity issues without corresponding docstring rows
    violations = sorted(set(new_complexity_issues.keys()) & docstring_issues)

    if violations:
        if as_json:
            ignore_data = [
                {
                    "path": str(Path(violation[0]).relative_to(here)),
                    "row": violation[1],
                    "name": parse_name(new_complexity_issues[violation]),
                    "complexity": parse_complexity(new_complexity_issues[violation]),
                }
                for violation in violations
            ]
            print(json.dumps(ignore_data, indent=2))
        else:
            for violation in violations:
                print(
                    f"[bold]{Path(violation[0]).relative_to(here)}:{violation[1]}[/bold]: {new_complexity_issues[violation]}. Add a docstring."
                )
            sys.exit(1)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check methods with high complexity for missing docstrings using Ruff."
    )
    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        default=".",
        help="List of files or directories to check.",
    )
    parser.add_argument(
        "--max-complexity",
        type=int,
        default=4,
        help="Maximum complexity without docstrings to allow.",
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="+",
        help="List of paths, used to omit files and/or directories from analysis",
    )

    parser.add_argument(
        "--ignore",
        type=Path,
        help="Path to containing violations to ignore in --json format.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output json for --ignore",
    )
    args = parser.parse_args(argv)
    ignored_violations = {(i["path"], i["name"]) for i in json.loads(args.ignore.read_text())} if args.ignore else set()

    analyze_complexity_with_docstrings(
        args.files,
        args.max_complexity,
        excludes=args.exclude or [],
        ignored_violations=ignored_violations,
        as_json=args.json,
    )


if __name__ == "__main__":
    main()
