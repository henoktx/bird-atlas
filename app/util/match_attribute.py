from typing import Optional


class Matcher:
    @staticmethod
    def match_str_attribute(value: Optional[str], target: Optional[str]) -> bool:
        if not value:
            return True

        return value.lower() in target.lower()

    @staticmethod
    def match_numeric_attribute(value: Optional[float | int], target: Optional[float | int]) -> bool:
        if not value:
            return True

        return value == target