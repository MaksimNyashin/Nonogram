from tkinter import *
from typing import Union


class InputSolver(Tk):
    def __init__(self, n):
        def jump(dx=0):
            if dx == 0:
                return
            if dx >= 3 * n:
                to = dx - 3 * n
            else:
                to = (self.x + dx) % len(self.elements)
            # print(self.x, dx, to, self.n)
            sum_row, sum_col = self.__get_sum()
            if sum_row is None:
                self.sum_counter_str.set("E")
            else:
                self.sum_counter_str.set(f"{sum_row}\n{sum_col}")
            self.elements[to].focus_set()
            self.x = to

        super().__init__()
        self.n = n
        self.resizable(False, False)
        l_rows = Label(self, text="Строки")
        l_rows.grid(row=1, column=1, columnspan=2)
        self.rows = []
        for i in range(n):
            Label(self, text=str(i + 1) + ": ").grid(column=1, row=i + 2)
            row = Entry(self)
            row.setvar("id", n+1)
            self.rows.append(row)
            row.grid(column=2, row=i + 2)
        l_cols = Label(self, text="Столбцы")
        l_cols.grid(column=3, row=1, columnspan=2)
        self.cols = []
        for i in range(n):
            Label(self, text=str(i + 1) + ": ").grid(column=3, row=i + 2)
            col = Entry(self)
            col.setvar("id", n+i)
            self.cols.append(col)
            col.grid(column=4, row=i + 2)

        self.x = 0
        self.bind("<Down>", lambda event=None: jump(1))
        self.bind("<Tab>", lambda event=None: jump(1))
        self.bind("<Up>", lambda event=None: jump(-1))
        self.bind("<Shift-Tab>", lambda event=None: jump(-1))
        self.bind("<Return>", lambda event=None: jump(1) if self.x < 2 * self.n else self.elements[self.x].invoke())
        self.bind("<Control-q>", lambda event=None: self.destroy())
        self.bind("<Control-s>", lambda event=None: self.start_solving())

        self.need_slide = False

        def change_need_slide():
            self.need_slide ^= True

        self.slide_tick = Checkbutton(self, command=change_need_slide)
        self.slide_tick.grid(column=1, row=n + 2)

        self.solve = Button(self, text="Решить", command=lambda event=None: self.start_solving())
        self.solve.grid(column=2, row=n + 2, columnspan=1)

        self.sum_counter_str = StringVar(master=self, value="0\n0")
        self.sum_counter = Message(self, textvariable=self.sum_counter_str)
        self.sum_counter.grid(column=3, row=n+2)

        self.cancel = Button(self, text="Отмена", command=lambda event=None: self.destroy())
        self.cancel.grid(column=4, row=n + 2, columnspan=1)

        self.elements = self.rows + self.cols
        for i in self.elements:
            i.bind("<Button-1>", lambda event=None: jump(3*n + i.getvar("id")))
        self.elements += [self.solve, self.cancel]
        self.elements[0].focus_set()
        self.x = 0
        self.focus_force()
        self.mainloop()

    @staticmethod
    def __isdigit_with_spaces(num: str) -> bool:
        return all(map(lambda c: c.isdigit() or c == " ",  num))

    def __get_sum(self) -> Union[tuple[int, int], tuple[None, None]]:
        ans = []
        for lst in (self.rows, self.cols):
            ans.append(0)
            for val in lst:
                ans_str = val.get()
                if self.__isdigit_with_spaces(ans_str):
                    ans[-1] += sum(map(int, ans_str.split()))
                else:
                    return None, None
        return ans[0], ans[1]

    def start_solving(self):
        from tkinter import messagebox

        def ret(t, num):
            messagebox.showinfo("Ошибка", f"Вы не заполнили {'строку' if t == 0 else 'столбец'} номер {num}")

        def ret2(t, num, err):
            messagebox.showinfo("Ошибка", f"Вы заполнили {'строку' if t == 0 else 'столбец'} номер {num} не числами, "
                                          f"а \"{err}\"")
        rows_sum, cols_sum = self.__get_sum()
        if rows_sum != cols_sum:
            messagebox.showinfo("Ошибка", f"Сумма по строкам {rows_sum} "
                                          f"не совпадает с суммой по столбцам {cols_sum}")
            return

        parsed_rows = []
        parsed_cols = []
        for i in range(self.n):
            s = self.rows[i].get()
            if s == "":
                ret(0, i + 1)
                return
            if self.__isdigit_with_spaces(s):
                parsed_rows.append(list(map(int, s.split())))
            else:
                ret2(0, i + 1, s)
                return
            s = self.cols[i].get()
            if s == "":
                ret(1, i + 1)
                return
            if self.__isdigit_with_spaces(s):
                parsed_cols.append(list(map(int, s.split())))
            else:
                ret2(1, i + 1, s)
                return
        # from main import default_solution
        # result = default_solution(self.n, parsed_rows, parsed_cols)
        from stringsolver.stringSolver import Field
        from result_array import ResultArraySlide
        slide = ResultArraySlide()
        result = Field.solve_string_by_string(self.n, parsed_rows, parsed_cols, slide)

        from builder import Saver
        from show_field import ShowField
        from slide_show_field import SlideShowField

        def show_field_callback():
            msg_box = messagebox.askokcancel(title="Save", message="Do you want to save?")
            if msg_box:
                Saver.save(result)
            self.destroy()

        if self.need_slide:
            SlideShowField(self.n, slide, show_field_callback)
        else:
            ShowField(self.n, result, show_field_callback)


if __name__ == "__main__":
    InputSolver(5)
