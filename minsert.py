"""
Dynamic content insertion in markdown files.
Source: https://pypi.org/project/minsert/
"""

import logging
import os
from typing import Dict, Union


class MinsertConfig:
    """Configure tokens for minsert."""

    # pylint: disable=too-few-public-methods
    START = "start"
    END = "end"
    SEP = ":"
    COMMENT_START = "<!-- CSV"
    COMMENT_END = "-->"


def is_comment(line: str) -> bool:
    """Check if a line is a valid markdown comment."""
    line = line.strip()
    if line.startswith(MinsertConfig.COMMENT_START) and line.endswith(
        MinsertConfig.COMMENT_END
    ):
        return True
    return False


def is_starter(line: str) -> Union[str, None]:
    """Return the name of the block if the line is a starter, else None."""
    if is_comment(line):
        try:
            get1 = line.split(MinsertConfig.START)[-1].strip()
            return get1.split("-")[0].strip()
        except Exception as err:  # pylint: disable=broad-except
            logging.warning(err)
            return None
    return None


def is_ender(line: str) -> bool:
    """Check if the line is a block ender."""
    if is_comment(line):
        return MinsertConfig.END in line.split(" ")
    return False


class MarkdownFile:
    """Wrapper for markdown file."""

    # pylint: disable=too-few-public-methods
    def __init__(self, file_path: str) -> None:
        """Initialize Markdownfile object.

        Args:
            file_path (str): path of markdown file.
        """
        if os.path.isfile(file_path) and file_path.endswith(".md"):
            self.file_path = file_path
        else:
            raise FileNotFoundError("the path you gave is invalid")

    def insert(self, things: Dict[str, str]):
        """Dynamically insert content in markdown file."""
        new_lines = []
        with open(self.file_path) as file:
            lines = file.readlines()

        inside_a_block = False
        count = 0

        for line in lines:
            if not inside_a_block:
                new_lines.append(line)
                count += 1
                start_of = is_starter(line)
                if not start_of:
                    continue
                try:
                    lines = things[start_of].split("\n")
                    count += len(lines)
                except KeyError:
                    logging.warning(
                        "\t '%s' in line %i of %s not found.",
                        start_of,
                        count,
                        self.file_path,
                    )
                    lines = []
                content = [ln + "\n" for ln in lines]
                new_lines += content
                inside_a_block = True
            elif is_ender(line):
                new_lines.append(line)
                count += 1
                inside_a_block = False
            else:
                continue

        if inside_a_block:
            raise ValueError("block not closed")

        with open(self.file_path, "w") as file:
            file.writelines(new_lines)
