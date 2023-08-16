import os
from abc import ABC, abstractmethod
from configparser import ConfigParser
from tkinter import END, Event, Menu, Misc, StringVar, Text, Tk
from tkinter.ttk import Button, Frame, Scrollbar
from typing import Any, Callable

from appdirs import user_config_dir

from dry.l10n import ENG, LIT, RUS, UKR, MsgFormat
from dry.tkutils import PAD

_LANG_CAPTIONS = {ENG: "English", UKR: "Українська", RUS: "Русский", LIT: "Lietuvių"}
_RUN_CAPTIONS = {ENG: "Run", UKR: "Рахувати", RUS: "Расчет", LIT: "Skaičiuoti"}
_UILANG_MENU = {ENG: "Interface", UKR: "Інтерфейс", RUS: "Интерфейс", LIT: "Sąsaja"}
_OUTLANG_MENU = {
    ENG: "Calculation",
    UKR: "Розрахунок",
    RUS: "Расчет",
    LIT: "Skaičiavimas",
}
_GUI_SECTION = "Interface"
_OPT_UILANG = "uilang"
_OPT_OUTLANG = "outlang"

_Langs = tuple[str, ...]


class MsgQueue:
    def __init__(self) -> None:
        self.__queue: list[str | Callable[[str], str]] = []
        self.__msg: dict[str, list[str]] = {}

    def __bool__(self) -> bool:
        return bool(self.__queue)

    def __getitem__(self, lang: str) -> list[str]:
        if lang not in self.__msg:
            self.__msg[lang] = []
            for i in self.__queue:
                if callable(i):
                    self.__msg[lang].append(i(lang))
                else:
                    self.__msg[lang].append(i)
        return self.__msg[lang]

    def append(self, msg: MsgFormat, *args: object) -> None:
        def localize(lang: str) -> str:  # crutch for mypy
            assert isinstance(msg, dict)
            return msg[lang].format(*args)

        if isinstance(msg, dict):
            self.__queue.append(localize)
        else:
            self.__queue.append(msg.format(*args))

    def clear(self) -> None:
        self.__queue.clear()
        self.__msg.clear()


class CalcApp(ABC):
    def __init__(
        self,
        root: Tk,
        appname: str,
        appvendor: str,
        appversion: str,
        uilangs: _Langs,
        outlangs: _Langs,
        title: MsgFormat,
    ) -> None:
        self.__root = root
        self.__title = title
        self.__appname = appname
        self.__appversion = appversion

        self.__errors = MsgQueue()
        self.__results = MsgQueue()
        self._inpdata: dict[str, Any] = {}

        cfgdir = user_config_dir(appname, appvendor, roaming=True)
        if not os.path.exists(cfgdir):
            os.makedirs(cfgdir)
        self.__cfgfile = os.path.join(cfgdir, "settings.ini")
        self.__cfg = ConfigParser()
        self.__cfg.read(self.__cfgfile)
        if not self.__cfg.has_section(_GUI_SECTION):
            self.__cfg.add_section(_GUI_SECTION)

        self._uilang = self.__getcfg_lang(_OPT_UILANG, uilangs)
        self._outlang = self.__getcfg_lang(_OPT_OUTLANG, outlangs)

        self.__menubar = Menu(root)
        uimenu = Menu(root, tearoff=0)
        outmenu = Menu(root, tearoff=0)
        translate_ui_events = {
            ENG: lambda: self.__translate_ui_into(ENG),
            UKR: lambda: self.__translate_ui_into(UKR),
            RUS: lambda: self.__translate_ui_into(RUS),
            LIT: lambda: self.__translate_ui_into(LIT),
        }
        translate_out_events = {
            ENG: lambda: self.__translate_out_into(ENG),
            UKR: lambda: self.__translate_out_into(UKR),
            RUS: lambda: self.__translate_out_into(RUS),
            LIT: lambda: self.__translate_out_into(LIT),
        }
        self.__uimenuvar = StringVar(value=self._uilang)
        self.__outmenuvar = StringVar(value=self._outlang)
        for i in uilangs:
            uimenu.add_radiobutton(
                label=_LANG_CAPTIONS[i],
                command=translate_ui_events[i],
                value=i,
                variable=self.__uimenuvar,
            )
        for i in outlangs:
            outmenu.add_radiobutton(
                label=_LANG_CAPTIONS[i],
                command=translate_out_events[i],
                value=i,
                variable=self.__outmenuvar,
            )
        self.__menubar.add_cascade(menu=uimenu)
        self.__menubar.add_cascade(menu=outmenu)
        root.config(menu=self.__menubar)

        mainframe = Frame(root)
        mainframe.grid(sticky="WENS", padx=PAD, pady=PAD)
        self._widgetframe = Frame(mainframe)
        self._widgetframe.grid(row=0, column=0, sticky="WN")
        self._outputframe = Frame(mainframe)
        self._outputframe.grid(row=0, column=1, columnspan=2, sticky="WENS")
        self.__memo = Text(self._outputframe, state="disabled", font="TkDefaultFont")
        vsb = Scrollbar(self._outputframe, command=self.__memo.yview, orient="vertical")
        self.__memo.configure(yscrollcommand=vsb.set)
        self.__memo.grid(row=0, column=0, sticky="WENS", padx=(PAD, 0), pady=PAD)
        vsb.grid(row=0, column=1, sticky="NS", padx=(0, PAD), pady=PAD)
        bottom_row = 10
        self.__runbutton = Button(mainframe, command=self.__on_run)
        self.__runbutton.grid(row=bottom_row, column=2, sticky="E", padx=PAD, pady=PAD)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(1, weight=1)
        self._outputframe.grid_rowconfigure(0, weight=1)
        self._outputframe.grid_columnconfigure(0, weight=1)

        root.protocol("WM_DELETE_WINDOW", self.__on_close)
        root.bind("<Return>", self.__event_run)

    def _translate_ui(self) -> None:
        self.__cfg.set(_GUI_SECTION, _OPT_UILANG, self._uilang)
        if isinstance(self.__title, dict):
            title = self.__title[self._uilang]
        else:
            title = self.__title
        self.__root.title(f"{title} — {self.__appname} {self.__appversion}")
        self.__runbutton["text"] = _RUN_CAPTIONS[self._uilang]
        self.__menubar.entryconfigure(1, label=_UILANG_MENU[self._uilang])
        self.__menubar.entryconfigure(2, label=_OUTLANG_MENU[self._uilang])
        if self.__errors:
            self.__print_errors()

    def _print_result(self) -> None:
        self.__print_to_memo("\n".join(self.__results[self._outlang]))

    def _translate_out(self) -> None:
        self.__cfg.set(_GUI_SECTION, _OPT_OUTLANG, self._outlang)
        if not self.__errors:
            self._print_result()

    def _adderror(self, msg: MsgFormat, *args: object) -> None:
        self.__errors.append(msg, *args)

    def _addline(self, msg: MsgFormat, *args: object) -> None:
        self.__results.append(msg, *args)

    def _resize_memo(self, width: int, height: int) -> None:
        self.__memo.configure(width=width, height=height)

    @abstractmethod
    def _get_inputdata(self) -> None:
        pass

    @abstractmethod
    def _runcalc(self) -> None:
        pass

    def __translate_ui_into(self, lang: str) -> None:
        self._uilang = lang
        self._translate_ui()

    def __translate_out_into(self, lang: str) -> None:
        self._outlang = lang
        self._translate_out()

    def __getcfg_lang(self, option: str, langs: _Langs) -> str:
        lang = self.__cfg.get(_GUI_SECTION, option, fallback=langs[0])
        return lang if lang in langs else langs[0]

    def __event_run(self, _: "Event[Misc]") -> None:
        self.__on_run()

    def __on_close(self) -> None:
        with open(self.__cfgfile, "w", encoding="utf-8") as file:
            self.__cfg.write(file)
        self.__root.destroy()

    def __print_to_memo(self, text: str) -> None:
        self.__memo.configure(state="normal")
        self.__memo.delete(1.0, END)
        self.__memo.insert(END, text)
        self.__memo.configure(state="disabled")

    def __print_errors(self) -> None:
        self.__print_to_memo("\n".join(self.__errors[self._uilang]))

    def __on_run(self) -> None:
        self.__errors.clear()
        self.__results.clear()
        self._inpdata.clear()

        self._get_inputdata()
        if self.__errors:
            self.__print_errors()
            return

        self._runcalc()
        if self.__errors:
            self.__print_errors()
        else:
            self._print_result()
