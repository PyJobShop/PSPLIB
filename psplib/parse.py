from pathlib import Path
from typing import Union

from .parse_aslib import parse_aslib
from .parse_mplib import parse_mplib
from .parse_patterson import parse_patterson
from .parse_psplib import parse_psplib
from .parse_rcpsp_max import parse_rcpsp_max
from .parse_rcpsp_ps import parse_rcpsp_ps
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
    elif instance_format == "rcpsp_max":
        return parse_rcpsp_max(loc)
    elif instance_format == "mplib":
        return parse_mplib(loc)
    elif instance_format == "rcpsp_ps":
        return parse_rcpsp_ps(loc)
    elif instance_format == "aslib":
        return parse_aslib(loc)

    raise ValueError(f"Unknown instance format: {instance_format}")
