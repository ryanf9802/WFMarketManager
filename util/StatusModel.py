import logging
import sys

logger = logging.getLogger(__name__)


class StatusModel:
    _instance = None

    @staticmethod
    def get_instance():
        if StatusModel._instance is None:
            logger.debug("Returning new StatusModel instance")
            StatusModel._instance = StatusModel()
        else:
            logger.debug("Returning existing StatusModel instance")
        return StatusModel._instance

    def __init__(self):
        if StatusModel._instance is not None:
            raise Exception("StatusModel is a singleton")
        self.status_message: str = ""
        self.numerator: int = 0
        self.denominator: int = 0

    @staticmethod
    def get_status_message() -> str:
        return StatusModel.get_instance().status_message

    @staticmethod
    def set_status_message(message: str) -> None:
        StatusModel.get_instance().status_message = message

    @staticmethod
    def get_numerator() -> int:
        return StatusModel.get_instance().numerator

    @staticmethod
    def get_denominator() -> int:
        return StatusModel.get_instance().denominator

    @staticmethod
    def set_numerator(numerator: int) -> None:
        StatusModel.get_instance().numerator = numerator

    @staticmethod
    def set_denominator(denominator: int) -> None:
        StatusModel.get_instance().denominator = denominator

    @staticmethod
    def get_percentage() -> str:
        return StatusModel.get_instance().percentage

    @staticmethod
    def display() -> None:
        sys.stdout.write(
            f"\r{StatusModel.get_instance().status_message} {StatusModel.get_percentage()} ({StatusModel.get_numerator()}/{StatusModel.get_denominator()})"
        )
        sys.stdout.flush()

    @property
    def percentage(self) -> str:
        """
        Return a string with the percentage with two decimal places
        """
        return (
            f"{(self.numerator / self.denominator) * 100:.2f}%"
            if self.denominator != 0
            else "0.00%"
        )

    def __str__(self) -> str:
        return f"{self.status_message} ({self.numerator}/{self.denominator})"

    def __repr__(self) -> str:
        return (
            f"StatusModel<{self.status_message} ({self.numerator}/{self.denominator})>"
        )
