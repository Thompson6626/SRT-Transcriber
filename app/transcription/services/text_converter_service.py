from cutlet import cutlet


class TextConverterService:
    def __init__(self):
        self.cutlet = cutlet.Cutlet(system="hepburn")
        self.cutlet.use_foreign_spelling = False

    def to_romaji(self, text: str) -> str:
        """
        Transforms given japanese text into romaji.
        :param text: Expected japanese text
        :return: Converted romaji.
        """
        return self.cutlet.romaji(text)
