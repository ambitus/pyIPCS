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

    def iterencode(self, o, _one_shot=False):
        def convert(obj):
            if hasattr(obj, "__pyipcs_json__"):
                return convert(obj.__pyipcs_json__())
            if isinstance(obj, dict):
                new_dict = {}
                for key, value in obj.items():
                    new_dict[convert(key)] = convert(value)
                return new_dict
            if isinstance(obj, (list, tuple)):
                return [convert(i) for i in obj]
            return obj

        return super().iterencode(convert(o), _one_shot)
