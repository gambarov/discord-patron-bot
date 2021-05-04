asterisk = '_'

class HangmanWord():
    def __init__(self, source: str) -> None:
        self.original = source
        self.encrypted = asterisk * len(source)
        self.used = set()

    def guess(self, letter: str) -> bool:
        letter = letter.lower()
        new_encrypted = ""
        guesses = 0
        for i in range(len(self.original)):
            original_letter = self.original[i]
            if letter == original_letter.lower():
                new_encrypted += original_letter
                guesses += 1
            else:
                new_encrypted += self.encrypted[i]
        self.used.add(letter)
        self.encrypted = new_encrypted
        return guesses

    def guess_completely(self, word: str) -> bool:
        if word.lower() == self.original.lower():
            guesses = sum(1 for a, b in zip(self.encrypted, self.original) if a != b)
            self.encrypted = self.original
            return guesses
        return 0

    @property
    def completed(self) -> bool:
        return self.original == self.encrypted

    @property
    def formatted_encrypted(self):
        return f"```{' '.join(self.encrypted.upper())}```".upper()

    @property
    def formatted_original(self):
        return f"```{' '.join(self.original.upper())}```".upper()

    def __len__(self) -> int:
        return len(self.original)

    def __str__(self) -> str:
        return self.original