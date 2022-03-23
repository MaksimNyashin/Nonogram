from tkinter import *
from basic_field import BasicCell, BasicField
from result_array import ResultArray


class Saver:
    @staticmethod
    def save(lst: ResultArray):
        """
        param lst: ResultArray
        return: rows and cols streak
"""
        size = len(lst)

        def get_line_list(sx, sy, dx, dy):
            to_return = [0]
            while 0 <= sx < size and 0 <= sy < size:
                if lst.get_num(sx, sy) == 2:
                    to_return[-1] += 1
                else:
                    if to_return[-1] != 0:
                        to_return.append(0)
                sx += dx
                sy += dy
            if to_return[-1] == 0:
                to_return.pop()
            return to_return

        rows = [get_line_list(i, 0, 0, 1) for i in range(size)]
        cols = [get_line_list(0, j, 1, 0) for j in range(size)]
        from os import path
        with open(path.join(path.dirname(__file__), "out_test.txt"), "a+") as fo:
            fo.write(f"{size}\n{rows}\n{cols}\n{Saver.list_to_string(lst)}\n\n")
            fo.close()
        return rows, cols

    @staticmethod
    def list_to_string(lst: ResultArray):
        return "\n".join("".join(lst.get_char(i, j) for j in range(len(lst))) for i in range(len(lst)))


class Cell(BasicCell):
    def __init__(self, master, callback, nxt):
        super(Cell, self).__init__(master=master)
        self.callback = callback
        self.nxt = nxt
        for i in range(3):
            self.bind(str(i), self.get_next(next_position=i, need_move=True))
        self.bind("<space>", self.get_next())
        self.bind("<Button-1>", self.get_next())
        self.bind("<FocusIn>", lambda event=None: self.change_focused(True))
        self.bind("<FocusOut>", lambda event=None: self.change_focused(False))

    def change_focused(self, new_focused):
        self.focused = new_focused
        self.next(self.position)

    def get_next(self, next_position=None, need_move=None):
        def return_next(event=None):
            if next_position is None:
                self.position = (self.position + 1) % 3
            else:
                self.position = next_position
            self.set_position()
            if need_move:
                self.nxt()
            self.callback()

        return return_next

    def next(self, next_position=None):
        return self.get_next(next_position)()


class Field(BasicField):
    def __init__(self, size):
        def cell_callback(x_id: int, y_id: int):
            def cell_callback_inner():
                self.modify_row(x_id)
                self.modify_col(y_id)

            return cell_callback_inner

        def nxt(event=None):
            change_foc(0 if self.y < self.size - 1 else 1, 1)

        def prv(event=None):
            change_foc(0 if self.y > 0 else -1, -1)

        super().__init__(size, cell_type=Cell,
                         cell_params=lambda _i, _j: {"callback": cell_callback(_i, _j), "nxt": nxt},
                         button_text=("Save",), button_command=(lambda event=None: self.check_all_colored(),))

        def change_foc(dx, dy):
            self.change_foc_abs((self.x + dx) % size, (self.y + dy) % size)

        change_foc(0, 0)

        # save = Button(self, text="Save", command=lambda event=None: self.check_all_colored())
        # save.place(x=size * self.SIZE + tab(size) + d_move, y=0 + d_move, width=self.SIZE, height=self.SIZE * 2)
        self.bind("<Control-s>", lambda event=None: self.check_all_colored())
        self.bind("<Down>", lambda event=None: change_foc(1, 0))
        self.bind("<Up>", lambda event=None: change_foc(-1, 0))
        self.bind("<Right>", nxt)
        self.bind("<Left>", prv)
        self.bind("<Tab>", nxt)
        self.bind("<Shift-Tab>", prv)
        self.bind("<Control-q>", lambda event=None: self.destroy())

        self.focus_force()
        self.mainloop()

    def change_foc_abs_pos(self, pos):
        self.change_foc_abs(pos // self.size, pos % self.size)

    def change_foc_abs(self, nx, ny):
        self.x = nx
        self.y = ny
        self.a[self.x][self.y].focus_set()

    def check_all_colored(self):
        to_send = []
        from tkinter import messagebox
        for i in range(self.size):
            to_send.append([])
            for j in range(self.size):
                p = self.a[i][j].position
                if p == 0:
                    messagebox.showinfo("Ошибка", "Вы НЕ закрасили все клетки")
                    self.change_foc_abs(i, j)
                    self.focus_force()
                    return
                elif p == 1:
                    to_send[-1].append(1)
                else:
                    to_send[-1].append(2)
        from result_array import ResultArray
        ra_to_send = ResultArray.build_list(to_send)
        if messagebox.askokcancel("Вы хотите сохранить?", Saver.list_to_string(ra_to_send).replace(".", "_")):
            r, c = Saver.save(ra_to_send)
            if messagebox.showinfo("Успешно сохранено", f"Данные для проверки:\n {str(r)}\n{str(c)}") == "ok":
                self.destroy()
        else:
            self.focus_force()
            self.change_foc_abs(0, 0)


class SetSize:
    def __init__(self):
        def show(x: Entry):
            from tkinter import messagebox
            if x.get().isdigit() and 0 < int(x.get()) <= 20:
                Field(int(x.get()))
            else:
                messagebox.showinfo("Ошибка", f"Вы ввели {x.get()} вместо натурального числа, которое не больше 20")

        top = Tk()
        top.resizable(False, False)
        size = Label(top, text="Размер")
        size.pack()
        entry = Entry(top)
        entry.focus_set()
        entry.bind("<Return>", lambda event=None: accept.invoke())
        entry.pack()
        accept = Button(top, text="Дальше", command=lambda event=None: show(entry))
        accept.pack()
        top.bind("<Control-q>", lambda event=None: top.destroy())
        top.focus_force()
        top.mainloop()


def main():
    SetSize()


if __name__ == "__main__":
    main()
