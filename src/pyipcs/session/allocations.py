"""
IpcsAllocations Object
"""


import copy
from ..error_handling import ArgumentTypeError

class IpcsAllocations:
    """
    IpcsAllocations Object

    Manages TSO allocations for IPCS Session.

    Methods
    -------
    __init__(init_allocations)
        Constructor for pyIPCS IpcsAllocations Object. 
        Sets TSO initial allocations for your IPCS session.

    get()
        Get TSO allocations for your IPCS session.

    set(dd_name, specification, extend=False)
        Set a single TSO allocation for your IPCS session.

    drop(dd_name)
        Remove a specific TSO allocation from your IPCS session by DD name if it exists.

    update(new_allocations, clear=True, extend=False)
        Update multiple TSO allocations for your IPCS session.
        
    clear()
        Clear all TSO allocations for your IPCS session.
    """

    def __init__(
        self,
        init_allocations: dict[str, str | list[str]]
    ) -> None:
        """
        Constructor for pyIPCS IpcsAllocations Object.

        Sets TSO initial allocations for your IPCS session.

        Parameters
        ----------
        init_allocations : dict[str,str|list[str]]
            Dictionary of allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.

        Returns
        -------
        None    
        """
        # Set Initial Allocations
        self._allocations = {}
        self.update(init_allocations)

    def get(self) -> dict[str, str | list[str]]:
        """
        Get TSO allocations for your IPCS session.

        Returns
        -------
        dict[str,str|list[str]]
            Returns dictionary of all allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.
        """
        return copy.deepcopy(self._allocations)

    def set(self, dd_name: str, specification: str | list[str], extend: bool = False) -> None:
        """
        Set a single TSO allocation for your IPCS session.

        Parameters
        ----------
        dd_name : str

        specification : str | list[str]
            String data set allocation request or list of cataloged datasets.

        extend : bool, optional
            If `True` and DD name `dd_name` already exists,
            will add list of datasets from `specification` to `dd_name`.
            Default is `False`.
        
        Returns
        -------
        None
        """
        if not isinstance(dd_name, str):
            raise ArgumentTypeError("dd_name", dd_name, str)
        if not isinstance(specification, (list, str)):
            raise ArgumentTypeError("specification", specification, (str, list))
        if (
            isinstance(specification, list)
            and not all(isinstance(dsname, str) for dsname in specification)
        ):
            raise TypeError("Elements of 'specification' list must be of type str")
        if not isinstance(extend, bool):
            raise ArgumentTypeError("extend", extend, bool)
        # SYSEXEC must be of type list to add pyIPCS specific SYSEXEC dataset
        if dd_name == "SYSEXEC" and not isinstance(specification, list):
            raise TypeError("DD name 'SYSEXEC' specification must be of type list[str]")

        dd_name = copy.deepcopy(dd_name)
        specification = copy.deepcopy(specification)
        if extend and dd_name in self._allocations:
            # Check both specification and new specification are of type list[str]
            if not isinstance(self._allocations[dd_name], list):
                raise TypeError(
                    f"DD name '{dd_name}' exists and its specification is of type str,"
                    " cannot extend"
                )
            if not isinstance(specification, list):
                raise TypeError(
                    f"DD name '{dd_name}' exists, 'specification' must be of type list[str]"
                    " to extend"
                )
            # Extend dd_name with more datasets
            self._allocations[dd_name].extend(specification)
        else:
            # If not extend or dd_name doesn't already exist just set the specification
            self._allocations[dd_name] = specification

    def drop(self, dd_name: str) -> None:
        """
        Remove a specific TSO allocation from your IPCS session by DD name if it exists.

        Parameters
        ----------
        dd_name : str

        Returns
        -------
        None
        """
        if dd_name in self._allocations:
            self._allocations.pop(dd_name)

    def update(
            self,
            new_allocations: dict[str, str | list[str]],
            clear: bool = True,
            extend: bool = False
        ) -> None:
        """
        Update multiple TSO allocations for your IPCS session.

        Parameters
        ----------
        new_allocations : dict[str,str|list[str]]
            Dictionary of allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.

        clear : bool, optional
            If `True` will clear all allocations before update. Default is `True`.

        extend : bool, optional
            If `True`, and `clear` is `False`, and DD name already exists,
            will add list of datasets from specification to DD name.
            Default is `False`.
        
        Returns
        -------
        None
        """
        if not isinstance(new_allocations, dict):
            raise ArgumentTypeError("new_allocations", new_allocations, dict)
        if not isinstance(clear, bool):
            raise ArgumentTypeError("clear", clear, bool)
        if not isinstance(extend, bool):
            raise ArgumentTypeError("extend", extend, bool)

        if clear:
            self.clear()
        for dd_name, specification in new_allocations.items():
            self.set(dd_name, specification, extend=extend)

    def clear(self) -> None:
        """
        Clear all TSO allocations for your IPCS session.

        Returns
        -------
        None
        """
        self._allocations = {}
