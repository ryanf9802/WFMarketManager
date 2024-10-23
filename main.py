import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
from util.StatusModel import StatusModel
import asyncio
from dotenv import load_dotenv
import os
import tkinter as tk
import requests

load_dotenv()

# Clear log file
open("output.log", "w").close()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            "output.log",
        ),
    ],
)
logger = logging.getLogger(__name__)


async def main():
    auth = False
    root = tk.Tk()
    root.title("Warframe Market Manager")
    root.geometry("600x400")

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    username_label = tk.Label(root, text="Username")
    username_entry = tk.Entry(root, textvariable=username_var)

    password_label = tk.Label(root, text="Password")
    password_entry = tk.Entry(root, textvariable=password_var, show="*")

    session: wm.auth.models.Session
    wq: WFMQueue = None

    if auth and not WFMQueue.active_instance():
        wq = WFMQueue(session)
        await wq.start()

    def submit():
        try:
            session = wm.auth.signin(str(username_var), str(password_var))
        except requests.exceptions.HTTPError as e:
            pass
        except wm.exceptions.defs.WMError as e:
            pass

        if session:
            auth = True
            logger.info(f'User "{username_var}" successfully authorized')

        

    submit_btn = tk.Button(
        root,
        text="Submit",
        command=submit,
    )

    username_label.grid(row=0,column=0)
    username_entry.grid(row=0,column=1)
    password_label.grid(row=1,column=0)
    password_entry.grid(row=1,column=1)
    submit_btn.grid(row=2,column=1)

    root.mainloop()
    if wq:
        await wq.stop()


if __name__ == "__main__":
    asyncio.run(main())
