from typing import Optional

EMPTY, CROSS, BLACK = 0, 1, 2
STATES_CHARS = {EMPTY: "_", CROSS: ".", BLACK: "0"}
STATES = STATES_CHARS.keys()
STATES_UN_CHARS = dict((STATES_CHARS[key], key) for key in STATES_CHARS)


class ResultArray:
    def __init__(self, array=None):
        n = len(array)
        self.__n = n
        for ind, val in enumerate(array):
            if n != len(val):
                raise ValueError(f"ResultArray must be square. But it has {n} rows and its row number {ind} has length "
                                 f"{len(val)}")
            for jnd, cell in enumerate(val):
                if cell not in STATES and cell not in STATES_UN_CHARS.keys():
                    raise ValueError(f"ResultArray may received char {cell} at position {ind}, {jnd}, "
                                     f"which is forbidden")
        self.__a = array

    @classmethod
    def build_list(cls, lst):
        return cls(lst)

    @classmethod
    def build_str(cls, lst: str):
        return cls(list(lst.split("\n")))

    def get_num(self, i_id, j_id):
        val = self.__a[i_id][j_id]
        if isinstance(val, int):
            return val
        else:
            return STATES_UN_CHARS[val]

    def get_char(self, i_id, j_id):
        val = self.__a[i_id][j_id]
        if isinstance(val, str):
            return val
        else:
            return STATES_CHARS[val]

    def __len__(self):
        return self.__n

    def __str__(self):
        return "\n".join("".join(self.get_char(i, j) for j in range(self.__n)) for i in range(self.__n))


class ResultArraySlide:
    def __init__(self):
        self.__a = []
        self.__pos = 0

    def add_slide(self, new_result: ResultArray) -> None:
        self.__a.append(new_result)

    def get_cur_result(self) -> Optional[ResultArray]:
        if self.__pos < len(self.__a):
            return self.__a[self.__pos]
        else:
            return None

    def inc_pos(self) -> None:
        if self.__pos < len(self.__a):
            self.__pos += 1

    def dec_pos(self) -> None:
        if self.__pos > 0:
            self.__pos -= 1

    def __len__(self) -> int:
        return len(self.__a)

    def get_pos(self) -> int:
        return self.__pos
