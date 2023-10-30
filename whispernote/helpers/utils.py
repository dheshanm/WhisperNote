from configparser import ConfigParser
import subprocess
import os
import sys
import logging

from rich.console import Console
from rich.logging import RichHandler


MODULE_NAME = "utils"

logger = logging.getLogger(MODULE_NAME)
logargs = {
    "level": logging.INFO,
    # "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
    "format": "%(message)s",
    "handlers": [RichHandler(rich_tracebacks=True)],
}
logging.basicConfig(**logargs)

console = Console()


def config(filename: str, section: str) -> dict:
    parser = ConfigParser()
    parser.read(filename)

    conf = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            conf[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return conf


def get_repo_root() -> str:
    """
    Returns the root directory of the current Git repository.

    Uses the command `git rev-parse --show-toplevel` to get the root directory.
    """
    repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
    repo_root = repo_root.decode("utf-8").strip()
    return repo_root


def get_config_file() -> str:
    """
    Returns the path to the config file.

    The config file is located at the root of the repository.
    """
    repo_root = get_repo_root()
    config_file = os.path.join(repo_root, "config.ini")
    return config_file


def execute_commands(
    command_array: list,
    shell: bool = False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
) -> subprocess.CompletedProcess:
    """
    Executes a command and returns the result.

    Args:
        command_array (list): The command to execute as a list of strings.
        shell (bool, optional): Whether to execute the command in a shell. Defaults to False.

    Returns:
        subprocess.CompletedProcess: The result of the command execution.

    Raises:
        SystemExit: If the command fails, the function exits with status code 1.

    """
    logger.info("\nExecuting command:")
    logger.info(" ".join(command_array))

    if shell:
        result = subprocess.run(
            " ".join(command_array),
            stdout=stdout,
            stderr=stderr,
            shell=True,
        )
    else:
        result = subprocess.run(command_array, stdout=stdout, stderr=stderr)

    if result.returncode != 0:
        logger.error("=====================================")
        logger.error("Command: " + " ".join(command_array))
        logger.error("=====================================")
        logger.error("stdout:")
        logger.error(result.stdout.decode("utf-8"))
        logger.error("=====================================")
        logger.error("stderr:")
        logger.error(result.stderr.decode("utf-8"))
        logger.error("=====================================")
        logger.error("Exit code: " + str(result.returncode))
        sys.exit(1)
