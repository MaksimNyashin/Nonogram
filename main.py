def default_solution(n, rows, cols):
    def cmp(list1, list2):
        if list1 == [0]:
            return True
        l1 = len(list1) - 1
        if list1[l1] == 0:
            l1 -= 1
        if l1 + 1 > len(list2):
            return False
        return list1[l1] <= list2[l1] and list1[:l1] == list2[:l1]

    def equal(l1, l2):
        if l1 == [0]:
            if l2 == [0]:
                return True
            return False
        ll2 = len(l2)
        ll1 = len(l1)
        if not (ll2 == ll1 or (ll2 + 1 == ll1 and l1[-1] == 0)):
            return False
        for ind in range(ll2):
            if l1[ind] != l2[ind]:
                return False
        return True

    def rec(pos, a, my_cols, row):
        # global mxx
        # mxx = max(mxx, pos)
        # print(a, my_cols, row)
        if pos == n * n:
            for ind_d in range(n):
                if not equal(my_cols[ind_d], cols[ind_d]):
                    return None
            return a.copy()
        x, y = pos // n, pos % n
        a[x][y] = 1
        my_cols[y][-1] += 1
        res = None
        if cmp(my_cols[y], cols[y]):
            row[-1] += 1
            if y == n - 1:
                if equal(row, rows[x]):
                    res = rec(pos + 1, a, my_cols, [0])
            else:
                if cmp(row, rows[x]):
                    res = rec(pos + 1, a, my_cols, row)
            row[-1] -= 1
        my_cols[y][-1] -= 1
        if res is not None:
            return res
        a[x][y] = 2
        is_add = False
        if my_cols[y][-1] != 0:
            is_add = True
            my_cols[y].append(0)
        if cmp(my_cols[y], cols[y]):
            is_a = False
            if row[-1] != 0:
                is_a = True
                row.append(0)
            if y == n - 1:
                if equal(row, rows[x]):
                    res = rec(pos + 1, a, my_cols, [0])
            else:
                if cmp(row, rows[x]):
                    res = rec(pos + 1, a, my_cols, row)
            if is_a:
                row.pop()

        if is_add:
            my_cols[y].pop()
        a[x][y] = 0
        return res

    ar = []
    my_cols_ = []
    for i in range(n):
        ar.append([0] * n)
        my_cols_.append([0])
    ret = rec(0, ar, my_cols_, [0])
    return ret if ret is not None else [[None]]


def main():
    inp = input("Размер: ")
    if inp == "builder" or inp == "build":
        import builder
        builder.SetSize()
        return
    if inp == "end" or inp == "exit":
        exit(0)
    if not inp.isdigit():
        return
    n = int(inp)
    from solver import InputSolver
    InputSolver(n)


if __name__ == "__main__":
    while True:
        main()
