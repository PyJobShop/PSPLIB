from pathlib import Path
from typing import Union

from .parse_mplib import parse_mplib
from .parse_patterson import parse_patterson
from .parse_psplib import parse_psplib
from .ProjectInstance import ProjectInstance


def parse(
    loc: Union[str, Path],
    instance_format: str = "psplib",
) -> ProjectInstance:
    """
    Parses a project instance from a file location.

    Parameters
    ----------
    loc
        The location of the instance.
    instance_format
        The format of the instance.

    Returns
    -------
    ProjectInstance
        The parsed project instance.
    """
    if instance_format == "psplib":
        return parse_psplib(loc)
    elif instance_format == "patterson":
        return parse_patterson(loc)
    elif instance_format == "mplib":
        return parse_mplib(loc)

    raise ValueError(f"Unknown instance format: {instance_format}")
