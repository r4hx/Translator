import logging
from multiprocessing import freeze_support, shared_memory
from threading import Thread

from handler import HotKeyHandler
from systray import TranslaterApp

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


freeze_support()  # pyinstaller fix for use thread

try:
    shm = shared_memory.SharedMemory(name="Translator", create=True, size=1)
except FileExistsError:
    pass

if __name__ == "__main__":
    Thread(target=HotKeyHandler().run).start()
    TranslaterApp().run()
