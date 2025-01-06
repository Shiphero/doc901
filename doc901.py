"""
Enforce docstrings on complex function and methods
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys
from rich import print

__version__ = "0.1"
here = Path.cwd().resolve()


def analyze_complexity_with_docstrings(files: list, complexity: int):
    """
    Run Ruff with a custom config to check methods with high complexity
    and missing docstrings.
    """
    # Run Ruff with the specified configuration
    result = subprocess.run(
        [
            "ruff",
            "check",
            "-e",
            "--config",
            f"lint.mccabe.max-complexity={complexity}",
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
            *files,
        ],
        capture_output=True,
        text=True,
    )
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

    # Extract complexity issues and docstring violations with both row and filename
    complexity_issues = {
        (issue["filename"], int(issue["noqa_row"])): issue["message"] for issue in issues if issue["code"] == "C901"
    }
    docstring_issues = {(issue["filename"], issue["noqa_row"]) for issue in issues if issue["code"].startswith("D1")}
    # Identify violations: complexity issues without corresponding docstring rows
    violations = sorted(set(complexity_issues.keys()) & docstring_issues)

    if violations:
        for violation in violations:
            print(
                f"[bold]{Path(violation[0]).relative_to(here)}:{violation[1]}[/bold]: {complexity_issues[violation]}. Add a docstring."
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
    args = parser.parse_args(argv)

    analyze_complexity_with_docstrings(args.files, args.max_complexity)


if __name__ == "__main__":
    main()
