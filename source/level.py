class Level:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        map = """
        xxxxxxxxxxxxxxxxxxxxxx
        x                    x
        x                    x
        x       xxxxx        x
        x                    x
        x                    x
        x          xxxxx     x
        x                    x
        x                    x
        x    xxxxxx          x
        x               p    x
        xxxxxxxxxxxxxxxxxxxxxx
        """
        self.tiles = []
