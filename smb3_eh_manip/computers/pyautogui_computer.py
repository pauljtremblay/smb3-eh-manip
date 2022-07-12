import logging

from timeit import default_timer as timer

import pyautogui


class PyautoguiComputer:
    def compute():
        start = timer()
        result = None
        i = 0
        iterations = 10
        while i != iterations:
            result = pyautogui.locateCenterOnScreen("data/smb3FceuxFrame106.png")
            i += 1
        if result:
            buttonx, buttony = result
        else:
            buttonx = -1
            buttony = -1
        end = timer()
        logging.info(f"x {buttonx} y {buttony} duration {(end-start)/iterations}s")
        return buttonx, buttony