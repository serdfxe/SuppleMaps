from dataclasses import dataclass

@dataclass
class Notification:
    name: str
    discription: str
    type: str
    show: bool = False
    content: tuple = ()

    def __call__(self):
        return self.discription
