asterisk = '_'

class Word():
    def __init__(self, source: str) -> None:
        self.original = source
        self.encrypted = asterisk * len(source)

    def guess(self, letter: str) -> bool:
        letter = letter.lower()
        new_encrypted = ""
        for i in range(len(self.original)):
            original_letter = self.original[i]
            if letter == original_letter.lower():
                new_encrypted += original_letter
            else:
                new_encrypted += self.encrypted[i]
        guessed = self.encrypted != new_encrypted
        self.encrypted = new_encrypted
        return guessed

    @property
    def completed(self) -> bool:
        return self.original == self.encrypted

    @property
    def formatted_encrypted(self):
        result = ""
        for letter in self.encrypted:
            result += letter + ' '
        return f"```{result.upper()}```"

    @property
    def formatted_original(self):
        return f"```{[' '.join(letter) for letter in self.original]}```".upper()

    def __str__(self) -> str:
        return self.original