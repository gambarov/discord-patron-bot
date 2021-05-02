cells_emoji = { '1':'1️⃣', '2':'2️⃣', '3':'3️⃣', '4':'4️⃣', '5':'5️⃣', '6':'6️⃣', '7':'7️⃣', '8':'8️⃣', '9':'9️⃣' }


class GameGrid():
    def __init__(self, size = 3) -> None:
        self.matrix = [[0 for x in range(size)] for y in range(size)]
        self.size = size
        self.move_count = 0
        index = 1
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = { 'emoji':cells_emoji[str(index)] }
                index += 1

    def __str__(self):
        string = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                string += self.matrix[i][j]['emoji']
            string += '\n'
        return string

    def has(self, emoji):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j]['emoji'] == emoji:
                    return True

    def replace(self, cell_emoji, player_emoji):
        index = 1
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                emoji = self.matrix[i][j]['emoji']
                if emoji == cell_emoji:
                    self.matrix[i][j] = { 'emoji':player_emoji }
                    self.move_count += 1
                    return True
        return False