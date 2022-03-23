from result_array import ResultArraySlide
from basic_field import BasicField, BasicCell


class SlideShowField(BasicField):
    def __init__(self, size: int, array: ResultArraySlide, callback):
        super(SlideShowField, self).__init__(size=size, cell_type=BasicCell, cell_params=(lambda _i, _j: {}),
                                             button_text=("Next", "Prev"),
                                             button_command=(self.__next_slide, self.__prev_slide))
        self.__array = array
        self.__callback = callback

        from tkinter import Label, StringVar
        self.counter_str = StringVar(master=self, value=f"0/{len(self.__array) - 1}")
        self.counter = Label(self, bg="SystemButtonFace", textvariable=self.counter_str)
        self.counter.place(x=0, y=0, width=self.SIZE * 2, height=self.SIZE * 2)
        self.bind("p", func=lambda event=None: self.__prev_slide())
        self.bind("n", func=lambda event=None: self.__next_slide())

        self.but[0].focus_force()
        self.mainloop()

    def __next_slide(self):
        self.__array.inc_pos()
        if not self.__update_field():
            self.destroy()

    def __prev_slide(self):
        self.__array.dec_pos()
        self.__update_field()

    def __update_field(self) -> bool:
        cur_result_array = self.__array.get_cur_result()
        if cur_result_array is None:
            return False
        for i in range(self.size):
            for j in range(self.size):
                self.a[i][j].set_position(new_position=cur_result_array.get_num(i, j))

        for i in range(self.size):
            self.modify_row(i)
            self.modify_col(i)
        self.counter_str.set(f"{self.__array.get_pos()}/{len(self.__array) - 1}")
        return True

    def destroy(self) -> None:
        self.__callback()
        super(SlideShowField, self).destroy()
