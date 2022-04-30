from typing import TYPE_CHECKING

from takler.logging import get_logger

if TYPE_CHECKING:
    from logging import Logger


logger = get_logger("core")  # type: Logger
