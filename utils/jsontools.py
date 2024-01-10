"""
The stringify function converts a list, dictionary, or tuple into a string representation, handling nested structures
and various data types. If unsupported types are encountered, it raises a TypeError.
"""


def stringify(value: list | dict | tuple) -> str:
    __temp = value
    if type(value) in [list, tuple]:
        __temp = "[ "
        for val in value:
            if type(val) == str:
                __temp += f'"{val}", '
            elif type(val) == int:
                __temp += f'{val}, '
            elif type(val) == bool:
                __temp += f'{str(val).lower().replace("none", "null")}, '
            elif type(val) in [list, dict, tuple]:
                __temp += stringify(val) + ", "
            else:
                raise TypeError(f"The type '{type(val)}' is not supported!")
        __temp = __temp[:-2] + " ]"
        if len(__temp) == 2:
            __temp = "[]"

    elif type(value) == dict:
        __temp = "{ "
        for key in value:
            pre_and_suffix_of_key = "" if type(key) in [float, int] else "\""
            if type(value[key]) == str:
                __temp += f'{pre_and_suffix_of_key}{key}{pre_and_suffix_of_key}: "{value[key]}", '
            elif type(value[key]) in [int, float]:
                __temp += f'{pre_and_suffix_of_key}{key}{pre_and_suffix_of_key}: {value[key]}, '
            elif type(value[key]) == bool:
                __temp += f'{pre_and_suffix_of_key}{key}{pre_and_suffix_of_key}: {str(value[key]).lower().replace("none", "null")}, '
            elif type(value[key] in [list, dict, tuple]):
                __temp += f'{pre_and_suffix_of_key}{key}{pre_and_suffix_of_key}: ' + stringify(value[key]) + ", "
            else:
                raise TypeError(f"The type '{type(value[key])}' is not supported!")

        __temp = __temp[:-2] + " }"
        if len(__temp) == 2:
            __temp = "{}"

    return str(__temp)
