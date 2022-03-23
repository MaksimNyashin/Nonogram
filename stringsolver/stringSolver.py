from result_array import EMPTY, CROSS, BLACK, STATES, STATES_CHARS, ResultArray, ResultArraySlide


class StrikeList:
    def __init__(self, *args: int):
        self.line = args

    def __eq__(self, other):
        return self.line == other.line

    def is_sub(self, other, is_continuing):
        if not other:
            return True
        n = len(other)
        if len(self) < n:
            return False
        if is_continuing:
            return self[n - 1] >= other[n - 1] and self[:n - 1] == other[:n - 1]
        else:
            return self[:n] == other.line

    def __len__(self):
        return len(self.line)

    def __getitem__(self, item):
        return self.line[item]


class MyString:
    def __init__(self, parent, n: int, x_id, is_hor: bool, s):
        self.parent = parent
        self.x_id = x_id
        self.is_hor = is_hor
        self.a = [EMPTY] * n
        self.__changes = []
        if s is None:
            while True:
                s = input(f"{'Hor' if is_hor else 'Ver'} {(x_id + 1) // 10}{(x_id + 1) % 10}: ").split()
                if all([s_val.isdigit() for s_val in s]):
                    break
        else:
            s = s.split()
        a = [int(i) for i in s]
        self.__strike = StrikeList(*a)

    def __getitem__(self, item):
        # while self.__changes:
        #     self.__undo_change()
        if self.__changes:
            raise ValueError("Changes mast be empty while getting item")
        return self.a[item]

    def __setitem__(self, key, value):
        if value in STATES:
            if self.__changes:
                raise ValueError("Changes mast be empty while setting item")
            self.a[key] = value
        else:
            raise ValueError(f"Value in MyString mast be either {EMPTY}, {CROSS} or {BLACK}"
                             f"but {value} for key={key} is given")

    def get_strike(self, n: int = None) -> StrikeList:
        is_first = True
        result = []
        if n is None:
            n = len(self.a)
        for i in self.a[:n]:
            if i == BLACK:
                if is_first:
                    result.append(1)
                    is_first = False
                else:
                    result[-1] += 1
            else:
                is_first = True
        return StrikeList(*result)

    def __change(self, key, value) -> None:
        self.__changes.append((key, self.a[key], value))
        self.a[key] = value

    def __undo_change(self) -> None:
        key, old_value, cur_value = self.__changes[-1]
        if self.a[key] != cur_value:
            raise ValueError(f"While undoing change expected {cur_value}, found {self.a[key]}")
        self.a[key] = old_value
        self.__changes.pop()

    def fill_string(self):
        n = len(self.a)
        for_or, for_and = [0] * n, [1] * n
        # dep = [0] * 16

        def rec(pos: int):
            # dep[pos] += 1
            if pos == n:
                # print("here")
                # print(self.__strike.line, self.get_strike().line, self.a)
                if self.__strike == self.get_strike():
                    for ind in range(n):
                        if self.a[ind] == EMPTY:
                            raise ValueError(f"At the end of recursion value mustn't be {EMPTY}")
                        val = 1 if self.a[ind] == BLACK else 0
                        for_or[ind] |= val
                        for_and[ind] &= val
                return
            is_emp = (self.a[pos] == EMPTY)
            used = False
            for new_var in (CROSS, BLACK):
                if is_emp:
                    self.__change(pos, new_var)
                if not used or is_emp:
                    used = True
                    if self.__strike.is_sub(self.get_strike(pos + 1), self.a[pos] == BLACK and pos + 1 < n):
                        rec(pos + 1)
                if is_emp:
                    self.__undo_change()

        rec(0)
        # print(self.x_id, self.is_hor)
        # print(for_or, for_and)
        for i in range(n):
            if for_or[i] == 0 and for_and[i] == 1:
                print(self.__strike.line, self.get_strike().line, self.a, self.__changes)
                raise ValueError("Current crosses and colored are impossible with given strike")
            if for_or[i] == 0:
                self.parent.modify(self, i, CROSS)
            if for_and[i] == 1:
                self.parent.modify(self, i, BLACK)

    def get_const_strike(self) -> list[int]:
        return list(self.__strike.line)


class Field:
    def __init__(self, n: int, s: str, slide: ResultArraySlide):
        def is_parsed_as_digits(s_: str) -> bool:
            for i in s_:
                if (not i.isdigit()) and i != " ":
                    return False
            return True

        self.slide = slide
        self.filled = 0
        self.filled_colored = 0
        s_split = []
        if s is not None:
            s_split = s.split("\n")
        if s is None or len(s_split) != 2 * n or not all(is_parsed_as_digits(s_) for s_ in s_split):
            s_split = [None] * (n * 2)
        self.h = [MyString(self, n, x_id, True, s_split[x_id]) for x_id in range(n)]
        self.v = [MyString(self, n, x_id, False, s_split[x_id + n]) for x_id in range(n)]
        self.slide.add_slide(self.__get_solved_list())

    def modify(self, child: MyString, y_id: int, new_val: int):
        x_id = child.x_id
        if not child.is_hor:
            x_id, y_id = y_id, x_id
        if self.h[x_id][y_id] != new_val:
            self.h[x_id][y_id] = new_val
            self.v[y_id][x_id] = new_val
            self.filled += 1
            if new_val == BLACK:
                self.filled_colored += 1

    def get_pic(self) -> str:
        res = []
        d = STATES_CHARS
        for i in self.h:
            res.append("".join(d[j] for j in i))
        return "\n".join(res)

    def draw(self) -> None:
        print()
        print(self.get_pic())

    def solve(self, n: int = None) -> bool:
        import time
        t = 0
        nn = len(self.h) ** 2
        tm = 0
        while self.filled < nn:
            begin = time.time()
            if t == n:
                break
            t += 1
            old_filled = self.filled
            for i in self.h:
                # c_beg = time.time()
                i.fill_string()
                # print("Hor", i.x_id + 1, (time.time() - c_beg) * 1000)
            # print(f"\t-------{t}----------")
            # print(self.filled)
            # print(self.filled_colored)
            # print(self.get_pic())
            self.slide.add_slide(self.__get_solved_list())

            if t == n or self.filled == len(self.h) ** 2:
                break
            t += 1
            for i in self.v:
                # c_beg = time.time()
                i.fill_string()
                # print("Hor", i.x_id + 1, (time.time() - c_beg) * 1000)
            # print(f"\t-------{t}----------")
            # print(self.filled)
            # print(self.filled_colored)
            # print(self.get_pic())
            self.slide.add_slide(self.__get_solved_list())

            if self.filled == old_filled:
                break
            ad_tm = (time.time() - begin) * 1000
            # print(f"{t//2})\t{self.filled}\t\t{ad_tm} ms")
            tm += ad_tm
        if self.filled == nn:
            from tkinter import messagebox
            messagebox.showinfo("Successful!", f"Solved at round {t}\n{tm} ms spent")
            return True
        else:
            return False

    def get_list(self) -> tuple[list[list[int]], list[list[int]]]:
        return [i.get_const_strike() for i in self.h], [i.get_const_strike() for i in self.v]

    def save(self):
        with open("out.txt", "a") as fi:
            lst = self.get_list()
            fi.write(f"{len(lst[0])}\n{lst[0]}\n{lst[1]}\n{self.get_pic()}\n\n")

    def __get_solved_list(self) -> ResultArray:
        return ResultArray([list(i) for i in self.h])

    @classmethod
    def solve_string_by_string(cls, n: int, rows: list[list[int]], cols: list[list[int]],
                               slide: ResultArraySlide) -> ResultArray:
        def list_to_str(lst: list[list[int]]) -> str:
            return "\n".join(" ".join(map(str, i)) for i in lst)

        f = Field(n, f"{list_to_str(rows)}\n{list_to_str(cols)}", slide)
        f.solve()
        return f.__get_solved_list()


def main():
    #
    s = """3
13
14
2 6 3
3 6 3
3 7 1
1 3 6
1 4 2 2
6 6
4 4
13
15
15
5 5
5 5
6 4
9 5
3 2 7
2 8
2 10
12
8 3
5 3
8 3
12
6 7
2 1 7
4 9
7 5
2 4"""
    res = Field.solve_string_by_string(5, [[2, 2], [2, 2], [1], [4], [3, 1]], [[2, 2], [2, 2], [3], [2, 1], [2, 1]],
                                       ResultArraySlide())
    print(res)
    return
    # s1 = StrikeList(2)
    # s2 = StrikeList(1)
    # print(s1.is_sub(s2, False))
    f = Field(len(s.split("\n")) // 2, s, ResultArraySlide())
    # f = Field(15)

    if f.solve(1):
        print("VICTORY!!")
        if input("ENTER to save: ") == "" or False:
            f.save()
    else:
        print(f.filled_colored)
        print(f.filled)
    f.draw()

    # ms = f.h[2]
    # r = [1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2]
    # import time
    # for i in range(15):
    #     now = time.time()
    #     ms.fill_string()
    #     print(i, (time.time() - now) * 1000)
    #     ms.a[i] = r[i]
    # print(ms.a)

    # ms = f.h[0]
    # ms.a = [2, 2, 1, 1, 2]
    # print(ms._MyString__strike.line)
    # for i in range(5):
    #     print(ms.get_strike(i + 1).line)
    #     print(ms._MyString__strike.is_sub(ms.get_strike(i + 1), ms.a[i] == 2 and i != 4))


if __name__ == '__main__':
    main()
