class Asset:
    def __init__(self, name: str = None, filetype: str = None,
                 value: any = None, mimetype: str = None):
        self.name, self.filetype, self.value, self.mimetype = name, filetype, value, mimetype
