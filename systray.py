import logging
from multiprocessing import shared_memory

import rumps

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class TranslaterApp(rumps.App):
    def __init__(self) -> None:
        super(TranslaterApp, self).__init__(
            name="Translater", quit_button=None, icon="icon.png"
        )
        logging.debug("Starting systray icon")
        self.shm = shared_memory.SharedMemory(name="Translator")
        self.shm.buf[:10] = "Yandex    ".encode()
        self.yandex = rumps.MenuItem(title="Yandex")
        self.yandex.state = True
        self.google = rumps.MenuItem(title="Google")
        self.google.state = False
        self.promt = rumps.MenuItem(title="Promt")
        self.promt.state = False
        self.exit_button = rumps.MenuItem(title="Exit")
        self.menu = [
            self.yandex,
            self.google,
            self.promt,
            rumps.separator,
            self.exit_button,
        ]

    @rumps.clicked("Yandex")
    def yandex_onoff(self, sender) -> None:
        """
        For select yandex
        """
        logging.debug("You selected Yandex for default translator")
        for m in [self.yandex, self.google, self.promt]:
            m.state = False
        self.shm.buf[:10] = "Yandex    ".encode()
        sender.state = True

    @rumps.clicked("Google")
    def google_onoff(self, sender) -> None:
        """
        For select google
        """
        logging.debug("You selected Google for default translator")
        for m in [self.yandex, self.google, self.promt]:
            m.state = False
        self.shm.buf[:10] = "Google    ".encode()
        sender.state = True

    @rumps.clicked("Promt")
    def promt_onoff(self, sender) -> None:
        """
        For select promt
        """
        logging.debug("You selected Promt for default translator")
        for m in [self.yandex, self.google, self.promt]:
            m.state = False
        self.shm.buf[:10] = "Promt     ".encode()
        sender.state = True

    @rumps.clicked("Exit")
    def exit_button_click(self, sender) -> None:
        """
        For exit button
        """
        logging.debug("The application is shutting down")
        self.shm.unlink()
        rumps.quit_application()
