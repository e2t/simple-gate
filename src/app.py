from locale import atof
from tkinter import Tk
from tkinter.ttk import Entry, Label

from dry.basecalc import CalcError
from dry.calcapp import CalcApp
from dry.l10n import ENG, LIT, RUS, UKR
from dry.tkutils import PAD
from dry.strutils import fstr

import text.error
import text.out
import text.ui
from calc import InputData, StoplogGate


class App(CalcApp):
    def __init__(self, root: Tk) -> None:
        super().__init__(
            root,
            appname="StoplogGate",
            appvendor="Esmil",
            appversion="23.1",
            uilangs=(ENG, UKR, LIT),
            outlangs=(ENG, UKR, RUS),
            title=text.ui.TITLE,
        )
        entrywid = 15

        self.__wlabel = Label(self._widgetframe)
        self.__wlabel.grid(row=0, column=0, padx=PAD, pady=PAD, sticky="W")
        self.__wbox = Entry(self._widgetframe, width=entrywid)
        self.__wbox.grid(row=0, column=1, padx=PAD, pady=PAD)
        self.__wbox.focus()

        self.__hlabel = Label(self._widgetframe)
        self.__hlabel.grid(row=1, column=0, padx=PAD, pady=PAD, sticky="W")
        self.__hbox = Entry(self._widgetframe, width=entrywid)
        self.__hbox.grid(row=1, column=1, padx=PAD, pady=PAD)

        self._translate_ui()
        self._resize_memo(51, 11)

    def _translate_ui(self) -> None:
        super()._translate_ui()
        self.__wlabel["text"] = text.ui.WIDTH[self._uilang]
        self.__hlabel["text"] = text.ui.HEIGHT[self._uilang]

    def _get_inputdata(self) -> None:
        widthtext = self.__wbox.get()
        try:
            self._inpdata["width"] = atof(widthtext)
        except ValueError:
            self._adderror(text.error.WIDTH)

        heighttext = self.__hbox.get()
        try:
            self._inpdata["height"] = atof(heighttext)
        except ValueError:
            self._adderror(text.error.HEIGHT)

    def _runcalc(self) -> None:
        try:
            scr = StoplogGate(InputData(**self._inpdata), self._adderror)
        except CalcError:
            return
        self._create_result(scr)

    def _create_result(self, scr: StoplogGate) -> None:
        self._addline(
            text.out.STOPLOG, fstr(scr.width, minf=1), fstr(scr.height, minf=1)
        )
        self._addline("")
        self._addline(text.out.WEIGHT, round(scr.mass))
        self._addline(text.out.FRAME, round(scr.frame_mass))
        self._addline(text.out.GATE, round(scr.gate_mass))
