"""Интерфейс программы, ввод и вывод данных."""
import sys
from tkinter import Tk, W, E, N, DISABLED, Event
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter.scrolledtext import ScrolledText
from simplegate import SimpleGate, InputData
sys.path.append(f'{sys.path[0]}/..')
from dry.allgui import MyFrame, print_in_disabled_text, format_params
from dry.allcalc import InputDataError


class MainForm(MyFrame):
    """Главное окно программы."""

    def __init__(self, root: Tk) -> None:
        """Конструктор формы."""
        root.title('Расчет шандора (v1.2.0)')
        super().__init__(root)

        ENT_W = 7

        subframe = Frame(self)
        subframe.grid(row=0, column=0, sticky=W + N)

        row = 0
        Label(subframe, text='Ширина рамы:').grid(row=row, column=0, sticky=W)
        self._ent_frame_w = Entry(subframe, width=ENT_W)
        self._ent_frame_w.grid(row=row, column=1, sticky=W + E)
        Label(subframe, text='мм').grid(row=row, column=2, sticky=W)

        row += 1
        Label(subframe, text='Высота щита:').grid(row=row, column=0, sticky=W)
        self._ent_gate_h = Entry(subframe, width=ENT_W)
        self._ent_gate_h.grid(row=row, column=1, sticky=W + E)
        Label(subframe, text='мм').grid(row=row, column=2, sticky=W)

        self._memo = ScrolledText(self, state=DISABLED, height=4, width=30)
        self._memo.grid(row=0, column=1, sticky=W + E)

        Button(self, text='Расчет', command=self._run).grid(row=2, column=1,
                                                            sticky=E)
        self.bind_all('<Return>', self._on_press_enter)

        self._add_pad_to_all_widgets(self)
        self._focus_first_entry(self)

    def _output(self, text: str) -> None:
        print_in_disabled_text(self._memo, text)

    def _print_error(self, text: str) -> None:
        print_in_disabled_text(self._memo, text)

    def _run(self) -> None:
        try:
            frame_w = self._get_mm_from_entry(self._ent_frame_w)
            gate_h = self._get_mm_from_entry(self._ent_gate_h)
        except ValueError:
            return

        input_data = InputData(frame_w=frame_w, gate_h=gate_h)
        try:
            sg = SimpleGate(input_data)
        except InputDataError as excp:
            self._print_error(str(excp))
            return

        output = sg.designation + '\n'
        lines = []
        lines.append(('Общая масса', '{:.0f} кг'.format(sg.mass)))
        lines.append(('Рама', '{:.0f} кг'.format(sg.frame_mass)))
        lines.append(('Щит', '{:.0f} кг'.format(sg.gate_mass)))
        output += format_params(lines)
        self._output(output)

    def _on_press_enter(self, _: Event) -> None:
        self._run()
