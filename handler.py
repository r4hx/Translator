import logging
from multiprocessing import shared_memory
from time import time

from pynput.keyboard import HotKey, Key, KeyCode, Listener

from provider import translate

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class HotKeyHandler:
    """
    Events handler
    """

    count = 0
    updated_at = time()

    def event_parser(self) -> None:
        """
        Parsing event for hotkey
        """
        if self.updated_at >= time() - 4:
            if self.count == 0:
                self.count = 1
                self.updated_at = time()
            elif self.count == 1:
                self.count = 0
                self.updated_at = time()
                logging.debug("Hotkey has been Triggered!")
                shm = shared_memory.SharedMemory(name="Translator")
                provider = shm.buf[:10].tobytes()
                shm.close()
                provider = provider.decode()
                provider = provider.strip()
                translate(name=provider)
            else:
                self.count = 0
                self.updated_at = time()
        else:
            self.count = 1
            self.updated_at = time()

    def for_canonical(self, f) -> str | KeyCode:
        """
        Key normalizer
        """
        return lambda k: f(self.l.canonical(k))

    def run(self) -> None:
        """
        Init persistent hotkey handler function
        """
        logging.debug("Starting listener for handling keyboard events")
        hotkey = HotKey(
            keys=[Key.cmd_l, KeyCode(char="c")],
            on_activate=self.event_parser,
        )
        with Listener(
            on_press=self.for_canonical(hotkey.press),
            on_release=self.for_canonical(hotkey.release),
        ) as self.l:
            self.l.join()
