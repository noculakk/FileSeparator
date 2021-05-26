class DirectoryNotExistError(ValueError):
    def __init__(self) -> None:
        super().__init__()


class EmptyFilesListError(ValueError):
    def __init__(self) -> None:
        super().__init__()