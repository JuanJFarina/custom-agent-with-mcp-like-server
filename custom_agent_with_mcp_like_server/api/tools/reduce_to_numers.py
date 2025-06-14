MAPPING: dict[tuple[str, str, str] | tuple[str, str], str] = {
    ("a", "j", "s"): "1",
    ("b", "k", "t"): "2",
    ("c", "l", "u"): "3",
    ("d", "m", "v"): "4",
    ("e", "n", "w"): "5",
    ("f", "o", "x"): "6",
    ("g", "p", "y"): "7",
    ("h", "q", "z"): "8",
    ("i", "r"): "9",
}


def reduce_to_numbers(string: str) -> str:
    """
    Return a number representation of the given string according to numerology rules.

        Parameters:
                string (str): Any string

        Returns:
                numeric_representation (str): A numeric representation
    """
    result = ""
    for char in string:
        for key, value in MAPPING.items():
            if char in key:
                result += value
                break
    return result
