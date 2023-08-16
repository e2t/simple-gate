from locale import LC_ALL, setlocale
from tkinter import Tk

from app import App


def main() -> None:
    setlocale(LC_ALL, "")
    root = Tk()
    _ = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
