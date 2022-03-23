from tkinter import *
from result_array import ResultArray
from typing import Callable, Dict, Any


class BasicCell(Button):
    EMPTY, CROSS, BLACK = ResultArray.EMPTY, ResultArray.CROSS, ResultArray.BLACK = 0, 1, 2

    def __init__(self, master, **kwargs):
        super(BasicCell, self).__init__(master=master, bg="white", width=30, height=30, relief=GROOVE, **kwargs)
        self.parent = master
        self.focused = False
        self.position = self.EMPTY
        self.set_empty()

    def set_pic(self, col):
        self.config(bg=col)

    def set_empty(self):
        r = "70" if self.focused else "80"
        empty = "gray" + r
        self.set_pic(empty)

    def set_cross(self):
        cross = "grey95" if self.focused else "white"
        self.set_pic(cross)

    def set_black(self):
        black = "gray25" if self.focused else "black"
        self.set_pic(black)

    def set_position(self, new_position=None):
        old_position = self.position
        if new_position is not None:
            self.position = new_position
        if self.position == self.EMPTY:
            self.set_empty()
        elif self.position == self.CROSS:
            self.set_cross()
        elif self.position == self.BLACK:
            self.set_black()
        else:
            self.position = old_position


class CurrentStrike(Message):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg="white", fg="black", relief=GROOVE, **kwargs)


class BasicField(Tk):
    SIZE = 30
    TAB_STEP = 5
    TAB_SIZE = 3

    @classmethod
    def tab(cls, x):
        return x // cls.TAB_STEP * cls.TAB_SIZE

    def __init__(self, size: int, cell_type, cell_params: Callable[[int, int], Dict[str, Any]],
                 button_text: tuple[str, ...], button_command: tuple[Callable[[], None], ...]):
        """
        Creates window with square field of Cells, Messages with current strike for each row and column
        and some buttons on the right
        :param size: size of field
        :param cell_type: instance of BasicCell
        :param cell_params: lambda from indexes of cell (row number, column number) to dict with parameters of cells
        :param button_text: tuple of button names that are placed pn the right
        :param button_command: tuple of button commands if its size
        """
        super().__init__()

        if len(button_command) < len(button_text):
            delta = len(button_text) - len(button_command)
            button_command = tuple(list(button_command) + [lambda *args: None] * delta)
        self.x = 0
        self.y = 0
        self.size = size
        self.resizable(False, False)
        d_move = self.SIZE * 2 + self.TAB_SIZE
        self.geometry("%dx%d" % ((size + 1) * self.SIZE + self.tab(size + 1) + d_move,
                                 max(size, 2 * len(button_text)) * self.SIZE + self.tab(size) + d_move))
        self.a = []
        for j in range(size):
            self.a.append([])
            for i in range(size):
                cell = cell_type(self, **cell_params(j, i))
                cell.place(x=i * self.SIZE + self.tab(i) + d_move, y=j * self.SIZE + self.tab(j) + d_move,
                           width=self.SIZE, height=self.SIZE)
                self.a[-1].append(cell)

        self.hor_lines, self.ver_lines = [], []
        self.hor_str_vals, self.ver_str_vals = [], []
        for i in range(size):
            self.hor_str_vals.append(StringVar(master=self, value="0'"))
            self.hor_lines.append(CurrentStrike(master=self, textvariable=self.hor_str_vals[-1]))
            self.hor_lines[-1].place(x=0, y=i * self.SIZE + self.tab(i) + d_move,
                                     width=self.SIZE * 2, height=self.SIZE)
            self.ver_str_vals.append(StringVar(master=self, value="0"))
            self.ver_lines.append(CurrentStrike(master=self, textvariable=self.ver_str_vals[-1]))
            self.ver_lines[-1].place(x=i * self.SIZE + self.tab(i) + d_move, y=0,
                                     width=self.SIZE, height=self.SIZE * 2)

        self.but = []
        for ind, val in enumerate(button_text):
            self.but.append(Button(self, text=val, command=button_command[ind]))
            self.but[-1].place(x=size * self.SIZE + self.tab(size) + d_move, y=0 + d_move + (2 * self.SIZE) * ind,
                               width=self.SIZE, height=self.SIZE * 2)

    @staticmethod
    def __count_strike(lst: list[int], str_var: StringVar, wid: int) -> None:
        is_first = True
        result = []
        for i in lst:
            if i == 2:
                if is_first:
                    result.append(1)
                    is_first = False
                else:
                    result[-1] += 1
            else:
                is_first = True
        if not result:
            result = [0]
        ans = ""
        cnt = -1
        for i in result:
            if cnt + 1 + len(str(i)) > wid:
                ans += "\n"
                cnt = 0
            else:
                ans += " "
                cnt += 1
            ans += str(i)
            cnt += len(str(i))
        str_var.set(ans[1:])

    def modify_row(self, x_id: int):
        lst = [self.a[x_id][y_id].position for y_id in range(self.size)]
        self.__count_strike(lst, self.hor_str_vals[x_id], 9)

    def modify_col(self, y_id: int):
        lst = [self.a[x_id][y_id].position for x_id in range(self.size)]
        self.__count_strike(lst, self.ver_str_vals[y_id], 5)
        
    def destroy(self) -> None:
        super(BasicField, self).destroy()
