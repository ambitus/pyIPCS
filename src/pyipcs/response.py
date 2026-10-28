"""
TsoResponse, IpcsResponse, and IpcsParsedResponse Objects
"""

from typing import Optional


class TsoResponse:
    """
    Response from running a TSO/E command.
    """

    def __init__(self, cmd: str, rc: int, output: str, authorized: bool) -> None:
        self._cmd = cmd
        self._rc = rc
        self._output = output
        self._authorized = authorized

    @property
    def cmd(self) -> str:
        """The TSO/E command that was run."""
        return self._cmd

    @property
    def rc(self) -> int:
        """Return code of the TSO/E command."""
        return self._rc

    @property
    def output(self) -> str:
        """Output from the TSO/E command."""
        return self._output

    @property
    def authorized(self) -> bool:
        """Whether the command ran in an authorized environment."""
        return self._authorized

    def __repr__(self) -> str:
        return (
            f"TsoResponse(cmd={self._cmd!r}, rc={self._rc!r}, "
            f"authorized={self._authorized!r})"
        )


class IpcsResponse:
    """
    Response from running an IPCS subcommand.
    """

    def __init__(
        self,
        subcmd: str,
        rc: int,
        output: Optional[str],
        authorized: bool,
    ) -> None:
        self._subcmd = subcmd
        self._rc = rc
        self._output = output
        self._authorized = authorized

    @property
    def subcmd(self) -> str:
        """The IPCS subcommand that was run."""
        return self._subcmd

    @property
    def rc(self) -> int:
        """Return code of the IPCS subcommand."""
        return self._rc

    @property
    def output(self) -> Optional[str]:
        """Output from the IPCS subcommand, or ``None`` if a file object was provided."""
        return self._output

    @property
    def authorized(self) -> bool:
        """Whether the subcommand ran in an authorized environment."""
        return self._authorized

    def __repr__(self) -> str:
        return (
            f"IpcsResponse(subcmd={self._subcmd!r}, rc={self._rc!r}, "
            f"authorized={self._authorized!r})"
        )


class IpcsParsedResponse[T]:
    """
    Response from running an IPCS subcommand with parsed dump data.
    """

    def __init__(
        self,
        data: T,
        response: IpcsResponse,
    ) -> None:
        self._data = data
        self._response = response

    @property
    def data(self) -> T:
        """Data obtained by parsing subcommand output."""
        return self._data

    @property
    def response(self) -> IpcsResponse:
        """Raw IPCS subcommand response."""
        return self._response

    def __repr__(self) -> str:
        return (
            f"IpcsParsedResponse(data={self._data!r}, " f"response={self._response!r})"
        )
