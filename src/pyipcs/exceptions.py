"""
pyIPCS Warnings and Exceptions
"""

from pyipcs.response import TsoResponse, IpcsResponse


class TsoError(Exception):
    """
    Base level exception for TSO/E errors.
    """

    def __init__(self, message: str) -> None:
        """
        Args:
            message: Error message.
        """
        super().__init__(message)


class TsoInvalidReturnCodeError(TsoError):
    """
    TSO/E error for an invalid return code from a TSO command.
    """

    def __init__(self, response: TsoResponse) -> None:
        """
        Args:
            response: TSO response.
        """
        self._response = response
        message = (
            f"TSO command {response.cmd} "
            f"(authorized={response.authorized}) "
            f"exited with an invalid return code {response.rc}."
        )
        if response.output:
            message += f"\n[OUTPUT]:\n{response.output}"
        super().__init__(message)

    @property
    def response(self) -> TsoResponse:
        """The TSO response that triggered this error."""
        return self._response


class IpcsError(TsoError):
    """
    Base level exception for IPCS errors.
    """


class IpcsInvalidReturnCodeError(IpcsError):
    """
    IPCS error for an invalid return code while trying to run an IPCS subcommand.
    """

    def __init__(self, response: IpcsResponse) -> None:
        """
        Args:
            response: IPCS response.
        """
        self._response = response
        message = (
            f"IPCS subcommand {response.subcmd!r} "
            f"(authorized={response.authorized}) "
            f"exited with an invalid return code {response.rc}."
        )
        if response.output:
            message += f"\n[OUTPUT]:\n{response.output}"
        super().__init__(message)

    @property
    def response(self) -> IpcsResponse:
        """The IPCS response that triggered this error."""
        return self._response


class TsoWarning(UserWarning):
    """
    Base level warning for TSO/E conditions.
    """

    def __init__(self, message: str) -> None:
        """
        Args:
            message: Warning message.
        """
        super().__init__(message)


class TsoInvalidReturnCodeWarning(TsoWarning):
    """
    TSO/E warning for an invalid return code from a TSO command.
    """

    def __init__(self, response: TsoResponse) -> None:
        """
        Args:
            response: TSO response.
        """
        self._response = response
        super().__init__(
            f"TSO command {response.cmd} "
            f"(authorized={response.authorized}) "
            f"exited with a return code {response.rc}."
        )

    @property
    def response(self) -> TsoResponse:
        """The TSO response that triggered this warning."""
        return self._response


class IpcsWarning(TsoWarning):
    """
    Base level warning for IPCS conditions.
    """


class IpcsInvalidReturnCodeWarning(IpcsWarning):
    """
    IPCS warning for an invalid return code while trying to run an IPCS subcommand.
    """

    def __init__(self, response: IpcsResponse) -> None:
        """
        Args:
            response: IPCS response.
        """
        self._response = response
        super().__init__(
            f"IPCS subcommand {response.subcmd!r} "
            f"(authorized={response.authorized}) "
            f"exited with a return code {response.rc}."
        )

    @property
    def response(self) -> IpcsResponse:
        """The IPCS response that triggered this warning."""
        return self._response


class DdirDeletedError(IpcsError):
    """
    Exception raised when an operation is attempted on a deleted dump directory (DDIR).
    """

    def __init__(self) -> None:
        super().__init__("This dump directory (DDIR) has already been deleted")
