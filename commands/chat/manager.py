import os, logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class ChatDatabaseManager:
    def __init__(self) -> None:
        self.data = None
        try:
            dirname = os.path.dirname(__file__)
            file = os.path.join(dirname, 'db.bin')
            with open(file=file, encoding="UTF-8") as file:
                self.data = file.read().splitlines()
            self.data = [line.strip() for line in self.data]
            logger.info("Chat db loaded")
        except Exception as e:
            logger.exception(e)


    def find(self, text: str, min_ratio: float = 0.65):
        if not self.data:
            logger.warn("Can't find answer cause data is None!")
            return None

        answers = []
        text = text.lower()

        for line in self.data:
            q = self.get(line, 'q')
            if not q: 
                continue
            ratio = SequenceMatcher(None, text, q.lower()).ratio()
            if ratio >= min_ratio:
                answers.append({ 'q':q, 'text':self.get(line, 'answer'), 'ratio':ratio })

        return answers


    def get(self, line, prop):
        props = line.split('\\')
        if not len(props) == 3:
            return None
        return { 'q':props[0], 'answer':props[1], 'priority':props[2] }.get(prop)