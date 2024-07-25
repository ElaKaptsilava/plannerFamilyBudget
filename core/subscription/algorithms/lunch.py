class LuhnAlgorithm:
    """Class to validate a card number using Luhn algorithm."""

    def __init__(self, input_value: str) -> None:
        self.card_number = input_value.replace(" ", "")

    @staticmethod
    def odd_digits_sum(digits: list[int]) -> int:
        odd_digits = digits[-1::-2]
        return sum(odd_digits)

    @staticmethod
    def even_digits_sum(digits: list[int]) -> int:
        even_digits = digits[-2::-2]
        return sum(map(lambda num: sum(map(int, list(str(num * 2)))), even_digits))

    def __checksum(self) -> bool:
        digits = list(map(int, self.card_number))
        checksum = self.odd_digits_sum(digits=digits) + self.even_digits_sum(
            digits=digits
        )
        return checksum % 10 == 0

    def verify(self) -> bool:
        return self.__checksum()
