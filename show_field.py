from basic_field import BasicCell, BasicField
from result_array import ResultArray


class ShowField(BasicField):
    def __init__(self, size, field: ResultArray, callback):
        super().__init__(size=size, cell_type=BasicCell, cell_params=(lambda _i, _j: {}), button_text=("Back", ),
                         button_command=(lambda event=None: self.destroy(), ))

        for i in range(self.size):
            for j in range(self.size):
                self.a[i][j].set_position(field.get_num(i, j))

        for i in range(self.size):
            self.modify_row(i)
            self.modify_col(i)

        self.focus_force()
        self.but[0].focus_force()
        self.callback = callback
        self.mainloop()
        
    def destroy(self):
        if self.callback is not None:
            self.callback()
        super(ShowField, self).destroy()


if __name__ == '__main__':
    ShowField(5, ResultArray.build_list([[2, 2, 1, 2, 2],
                                         [2, 1, 2, 1, 2],
                                         [1, 2, 1, 2, 1],
                                         [2, 2, 2, 1, 1],
                                         [2, 1, 1, 2, 1]]), lambda *args: None)
    # ShowField(3, ResultArray.build_list(["_.0", "_00", "0_."]))
    # ShowField(3, ResultArray.build_str("0.0\n.00\n0.."))
