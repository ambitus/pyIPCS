"""
IpcsJsonEncoder Object
"""

import json


class IpcsJsonEncoder(json.JSONEncoder):
    """
    Custom pyIPCS JSON Encoder.
    """

    def default(self, o):
        if hasattr(o, "__pyipcs_json__"):
            return o.__pyipcs_json__()
        return super().default(o)
