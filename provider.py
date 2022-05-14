import logging
import webbrowser
from abc import ABC, abstractmethod

import pyperclip

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Provider(ABC):
    """
    Abstract class for translate providers
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.url = self.get_url()

    @abstractmethod
    def get_url(self) -> str:
        """
        Return url for translate service
        """
        return "https://egorovegor.ru"

    def open(self) -> None:
        """
        Open default browser with new tab
        """
        webbrowser.open_new_tab(self.url + self.text)


class Yandex(Provider):
    def get_url(self) -> str:
        return "https://translate.yandex.ru/?text="


class Google(Provider):
    def get_url(self) -> str:
        return "https://translate.google.com/?text="


class Promt(Provider):
    def get_url(self) -> str:
        return "https://www.translate.ru/?text="


def translate(name="Yandex") -> None:
    """
    Proccesed clipboard to webbrowser
    """
    clipboard = str(pyperclip.paste())
    if name == "Yandex":
        provider = Yandex
    elif name == "Google":
        provider = Google
    elif name == "Promt":
        provider = Promt
    else:
        provider = Yandex
    p = provider(clipboard)
    p.open()
