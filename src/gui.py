"""Интерфейс программы, ввод и вывод данных."""
from tkinter import Tk, W, E, N, DISABLED, Event
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter.scrolledtext import ScrolledText
from simplegate import SimpleGate, InputData
from dry.allgui import MyFrame, print_in_disabled_text, fstr, handle_ctrl_shortcut
from dry.allcalc import InputDataError


class MainForm(MyFrame):
    """Главное окно программы."""

    def __init__(self, root: Tk) -> None:
        """Конструктор формы."""
        root.title('Расчет шандора (v1.2.1)')
        super().__init__(root)

        ent_w = 7

        subframe = Frame(self)
        subframe.grid(row=0, column=0, sticky=W + N)

        row = 0
        Label(subframe, text='Ширина рамы (мм):').grid(row=row, column=0, sticky=W)
        self._ent_frame_w = Entry(subframe, width=ent_w)
        self._ent_frame_w.grid(row=row, column=1, sticky=W + E)

        row += 1
        Label(subframe, text='Высота щита (мм):').grid(row=row, column=0, sticky=W)
        self._ent_gate_h = Entry(subframe, width=ent_w)
        self._ent_gate_h.grid(row=row, column=1, sticky=W + E)

        self._memo = ScrolledText(self, state=DISABLED, height=5, width=30)
        self._memo.grid(row=0, column=1, sticky=W + E)

        Button(self, text='Рассчитать', command=self._run).grid(row=2, column=1, sticky=E)
        self.bind_all('<Return>', self._on_press_enter)

        self._add_pad_to_all_widgets()
        self._focus_first_entry(self)
        root.bind_all('<Key>', handle_ctrl_shortcut, '+')

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
            smpg = SimpleGate(input_data)
        except InputDataError as excp:
            self._print_error(str(excp))
            return

        output = [smpg.designation,
                  'Масса {} кг'.format(fstr(smpg.mass, '%.0f')),
                  '- рама {} кг'.format(fstr(smpg.frame_mass, '%.0f')),
                  '- щит {} кг'.format(fstr(smpg.gate_mass, '%.0f'))]
        self._output('\n'.join(output))

    def _on_press_enter(self, _: Event) -> None:
        self._run()
