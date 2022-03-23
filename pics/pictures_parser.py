from PIL import Image
from os import path
FOLDERS = [10, 15, 20]


class PicturesParser:
    DIF = 25
    __DRAW = False
    lst = ((255, 255, 255), (235, 239, 248), (52, 72, 97), (0, 0, 0), (194, 197, 206), (23, 41, 63))

    @staticmethod
    def dif(arr_a, arr_b):
        res = 0
        for ind, val in enumerate(arr_a):
            res += abs(val - arr_b[ind])
        return res

    @staticmethod
    def zzz(r, g, b, delta):
        def ab(val):
            return min(max(0, val + delta), 255)

        return ab(r), ab(g), ab(b)

    def __init__(self, name, n):
        self.name = name
        self.n = n
        pic = Image.open(path.join(path.dirname(__file__), str(n), name))
        self.pic = pic
        width, height = pic.size
        self.width, self.height = width, height

        # self.test_parsed()

        new_pic = Image.new("RGB", (self.width, self.height))
        self.new_pic = new_pic
        self.mxi, self.mni, self.mxj, self.mnj = 0, self.width, 0, self.height
        self.draw_frame()
        # self.new_pic.save("tmp/new_pic_frame.png")
        self.draw_cross_black()

    def draw_frame(self):
        # 1.6208333333333333
        FRAME_COEF = 4/3
        arr = [[(0, 0)] * self.height for _ in range(self.width)]
        arr2 = [[(0, 0)] * self.height for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if self.dif(self.lst[3], self.pic.getpixel((i, j))) < self.DIF:
                    # noinspection PyTypeChecker
                    arr[i][j] = [1, 1]
                    if i > 0:
                        arr[i][j][0] += arr[i - 1][j][0]
                    if j > 0:
                        arr[i][j][1] += arr[i][j - 1][1]

        for i in range(self.width - 1, -1, -1):
            for j in range(self.height - 1, -1, -1):
                if self.dif(self.lst[3], self.pic.getpixel((i, j))) < self.DIF:
                    # noinspection PyTypeChecker
                    arr2[i][j] = [1, 1]
                    if i < self.width - 1:
                        arr2[i][j][0] += arr2[i + 1][j][0]
                    if j < self.height - 1:
                        arr2[i][j][1] += arr2[i][j + 1][1]

        for i in range(self.width):
            for j in range(self.height):
                if arr[i][j][0] + arr[i][j][1] + arr2[i][j][0] + arr2[i][j][1] > \
                        min(self.width, self.height) * FRAME_COEF:
                    self.mni = min(self.mni, i)
                    self.mxi = max(self.mxi, i)
                    self.mnj = min(self.mnj, j)
                    self.mxj = max(self.mxj, j)
                    if self.__DRAW:
                        self.new_pic.putpixel((i, j), (255, 255, 255))

        if self.__DRAW:
            val = self.n // 5
            ver = [self.mni + (self.mxi - self.mni) * i // val for i in range(val + 1)]
            hor = [self.mnj + (self.mxj - self.mnj) * j // val for j in range(val + 1)]
            for i in range(self.mni, self.mxi + 1):
                for j in range(self.mnj, self.mxj + 1):
                    if i in ver:
                        self.new_pic.putpixel((i, j), (255, 0, 0))
                    if j in hor:
                        self.new_pic.putpixel((i, j), (0, 255, 255))

    def draw_cross_black(self):
        ans = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            lef_i = self.mni + (self.mxi - self.mni) * i // self.n
            rig_i = self.mni + (self.mxi - self.mni) * (i + 1) // self.n
            mid_i = (rig_i + lef_i) // 2
            del_i = (mid_i - lef_i) // 2
            for j in range(self.n):
                lef_j = self.mnj + (self.mxj - self.mnj) * j // self.n
                rig_j = self.mnj + (self.mxj - self.mnj) * (j + 1) // self.n
                mid_j = (rig_j + lef_j) // 2
                del_j = (mid_j - lef_j) // 2
                cnt_good, cnt_total = 0, 0
                for i1 in range(mid_i - del_i, mid_i + del_i):
                    for j1 in range(mid_j - del_j, mid_j + del_j):
                        cnt_total += 1
                        if self.dif(self.lst[0], self.pic.getpixel((i1, j1))):
                            cnt_good += 1
                eps = cnt_total * 0.05
                if eps < cnt_total - cnt_good < cnt_total - eps:
                    ans[j][i] = 1
                    if self.__DRAW:
                        for i1 in range(mid_i - del_i, mid_i + del_i):
                            for j1 in range(mid_j - del_j, mid_j + del_j):
                                self.new_pic.putpixel((i1, j1), (255, 0, 0))
                else:
                    ans[j][i] = 2
                    if self.__DRAW:
                        for i1 in range(mid_i - del_i, mid_i + del_i):
                            for j1 in range(mid_j - del_j, mid_j + del_j):
                                self.new_pic.putpixel((i1, j1), (0, 255, 0))

        from show_field import ShowField, ResultArray
        from tkinter import messagebox
        from builder import Saver

        res = ResultArray.build_list(ans)
        from os import system

        def pic_parsed_callback():
            if self.__DRAW:
                self.new_pic.save("tmp/new_pic_frame.png")
            msg_box = messagebox.askokcancel(title="Save", message="Do you want to save?")
            if msg_box:
                Saver.save(res)
                self.pic.close()
                from os import rename
                rename(path.join(path.dirname(__file__), str(self.n), self.name),
                       path.join(path.dirname(__file__), str(self.n), "Used", self.name))

        system(f"start {path.join(path.dirname(__file__), str(self.n), self.name)}")
        ShowField(self.n, res, pic_parsed_callback)

    def test(self):
        new_pic = Image.new("RGB", (self.width, self.height))
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pic.getpixel((i, j))
                pt = False
                for k, val in enumerate(self.lst):
                    if self.dif(val, (r, g, b)) < self.DIF:
                        pt = True
                        break
                if pt:
                    new_pic.putpixel((i, j), (255, 255, 255))
                # if pt:
                #     new_pic.putpixel((i, j), (r, g, b))
                # else:
                #     new_pic.putpixel((i, j), (175, 175, 0))
        new_pic.save("tmp/new_pic.png")

    def test_parsed(self):
        new_pics = [Image.new("RGB", (self.width, self.height)) for _ in self.lst]
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pic.getpixel((i, j))
                for k, val in enumerate(self.lst):
                    if self.dif(val, (r, g, b)) < self.DIF:
                        new_pics[k].putpixel((i, j), (255, 255, 255))
                        break
                # if pt:
                #     new_pic.putpixel((i, j), zzz(r, g, b, 40))
                # else:
                #     new_pic.putpixel((i, j), zzz(r, g, b, -40))
                # if pt:
                #     new_pic.putpixel((i, j), (r, g, b))
                # else:
                #     new_pic.putpixel((i, j), (175, 175, 0))
        for ind, val in enumerate(new_pics):
            val.save(f"tmp/new_pic{ind}.png")

    def count_pixels(self):
        cnt = {}
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pic.getpixel((i, j))
                cnt[(r, g, b)] = cnt.get((r, g, b), 0) + 1
        a = sorted([(key, cnt[key]) for key in cnt if cnt[key] > 1000], key=lambda x: x[1], reverse=True)
        for i in a:
            print(*i)
        z1 = self.pic.getpixel((191, 556))
        print("\t", z1, cnt[z1])
        z1 = self.pic.getpixel((286, 517))
        print("\t", z1, cnt[z1])
        z1 = self.pic.getpixel((676, 410))
        print("\t", z1)


if __name__ == '__main__':
    from os import listdir
    ind = FOLDERS[1]
    for link in listdir(path.join(path.dirname(__file__), str(ind))):
        if path.isfile(path.join(path.dirname(__file__), str(ind), link)):
            print("file:", link)
            PicturesParser(link, ind)
            break
    # PicturesParser("Screenshot_2022-02-04-13-46-46-10_4346f199aefb0b8fa54954fbf08fc720.jpg", 15)
    # PicturesParser("Screenshot_2022-02-04-18-00-36-14_4346f199aefb0b8fa54954fbf08fc720.jpg", 20)
