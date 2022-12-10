class ECB(object):
# 转化为二进制8x8矩阵
    def __init__(self, args , txt):
        self.operate = args.get("operate")
        self.text = args.get("text",txt.get("text"))
        self.key = args.get("key",txt.get("key"))
        self.iv = args.get("iv",txt.get("iv"))

    def to_str_bin(self, hex_str):
        tmp = ''
        res = []
        # 转二
        for i in hex_str:                       # 两个取巧：1.将其他进制数转化为10进制 ：int('文本类型数据',该数的进制)     2.zfill:字符串的0填充，避免16进制的1转化为二进制变成0b1 ，要求是0001
            tmp += bin(int(i,16))[2:].zfill(4)

        # 得矩阵
        for i in range(0,len(tmp),8):
            res.append(tmp[i:i+8])

        return res


    def ip_trans(self, m_b):
        l = []; r = []
        tmp = ''

        for j in range(0, 8):  # 对列
            for i in range(7, -1, -1):  # 对行
                tmp += m_b[i][j]
            if j % 2 == 0:  # 给r
                r.append(tmp)
            else:  # 给l
                l.append(tmp)
            tmp = ''

        return l, r, r

    def E_extend(self, r):
        r_bat = []
        r_bat.extend(r)

        for j in range(len(r_bat)):
            r_bat[j]=list(r_bat[j])
            # 处理中间v
            r_bat[j].insert(4,r_bat[j][4])
            r_bat[j].insert(5,r_bat[j][3])

        for i in range(len(r_bat)):
            # 处理左端
            if r_bat[i][-1]=="0":
                r_bat[(i+1)%4].insert(0,'0')
            else:
                r_bat[(i+1)%4].insert(0,'1')

        for i in range(len(r_bat)):
            # 处理右端
            if r_bat[i][1]=="0":
                r_bat[(i-1)%4].insert(999,'0')  # 999是超额的位置，默认到最后一个
            else:
                r_bat[(i-1)%4].insert(999,'1')

        # 恢复成["1101","1010"..]形式
        for i in range(len(r_bat)):
            r_bat[i]="".join(r_bat[i])


        return r_bat

    def get_key_16(self, key_b, mode = ""):
        # 置换选择1 得c0和d0（直接按表变化还快一点~）
        table_c = [
            57,49,41,33,25,17,9,
            1,58,50,42,34,26,18,
            10,2,59,51,43,35,27,
            19,11,3,60,52,44,36,
        ]
        table_d = [
            63,55,47,39,31,23,15,
            7,62,54,46,38,30,22,
            14,6,61,53,45,37,29,
            21,13,5,28,20,12,4,
        ]

        # 置换选择2用到的表
        table_2 = [
            14,17,11,24,1,5,
            3,28,15,6,21,10,
            23,19,12,4,26,8,
            16,7,27,20,13,2,
            41,52,31,37,47,55,
            30,40,51,45,33,48,
            44,49,39,56,34,53,
            46,42,50,36,29,32,
        ]

        # 得c0和d0
        c = "";d = ""
        key_str = ''.join(key_b)

        for i in range(len(table_c)):
            c+=key_str[table_c[i]-1]
            d+=key_str[table_d[i]-1]

    # 获取16轮key

        # 16次循环左移表
        move_left_table = [
            1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1
        ]

        key_16=[]   # 定义一个用来存储16次key的list

        # 获取16轮的key
        for i in range(len(move_left_table)):

            # 循环左移
            start = move_left_table[i]

            c = c[start::]+c[0:start]
            d = d[start::]+d[0:start]

            # c0和d0组合
            tmp = c+d

            # 置换选择2


            tmp2 = ''

            for i in range(len(table_2)):
                tmp2 += tmp[table_2[i]-1]

            key_16.append(tmp2)

        if self.operate == "encrypt" or mode == "CFB" or mode == "OFB" or mode == "CTR":
            return key_16
        else:
            return list(reversed(key_16))

    def to_xor(self, obj1,obj2):  # obj1是列表   obj2是str

        res = []
        obj1 = ''.join(obj1)
        tmp = ''

        for i in range(len(obj1)):
            tmp += str(eval(obj1[i])^eval(obj2[i]))
            if i%6==5:
                res.append(tmp)
                tmp = ""

        return res

    def tans_sbox(self, r_xor):
        # 8个s盒
        s=[
                [
                [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
                [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
                [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
                [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
            ],
                [
                [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,],
                [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,],
                [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,],
                [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9,]
            ],
                [
                [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,],
                [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,],
                [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,],
                [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12,]
            ],
                [
                [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,],
                [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,],
                [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,],
                [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14,]
            ],
                [
                [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,],
                [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,],
                [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,],
                [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3,],
            ],
                [
                [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,],
                [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,],
                [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,],
                [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13,],
            ],
                [
                [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,],
                [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,],
                [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,],
                [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12,],
            ],
                [
                [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,],
                [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,],
                [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,],
                [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11,],
            ],
        ]

        row = "" ; col = ""
        res = []

        for i in range(len(r_xor)):
            # 行(row)   列(col)
            row = r_xor[i][0]+r_xor[i][-1]
            col = r_xor[i][1:5]

            row = int(f"0b{row}",2)
            col = int(f"0b{col}",2)

            res.append(bin(s[i][row][col])[2:].zfill(4))

        return res

    def p_subs(self, r_s):
        p_table = [
            16,7,20,21,
            29,12,28,17,
            1,15,23,26,
            5,18,31,10,
            2,8,24,14,
            32,27,3,9,
            19,13,30,6,
            22,11,4,25
        ]
        r_tmp = ''.join(r_s)
        tmp = ''
        res = []

        for i in range(len(p_table)):
            tmp += r_tmp[p_table[i]-1]
            if len(tmp) % 8 == 0:
                res.append(tmp)
                tmp = ""

        return res

    def new_xor(self, l, r, r_p):

        tmp = ""
        l_str = "".join(l)
        r_p = "".join(r_p)

        r_new = [] ; l_new = []

        l_new.extend(r)

        for i in range(len(l_str)):
            tmp += str(eval(l_str[i])^eval(r_p[i]))
            if i%8==7:
                r_new.append(tmp)
                tmp = ""

        return l_new,r_new

    def output_res(self,l,r,key,times):
        l_str = "".join(l)
        r_str = "".join(r)

        l_res = hex(int(f"0b{l_str}",2))[2:].upper()
        r_res = hex(int(f"0b{r_str}",2))[2:].upper()
        key_res =  hex(int(f"0b{key}",2))[2:].upper()

        print(f"L{times}={l_res}    R{times}={r_res}    key{times}={key_res}")

# append function
    def ip_invert(self):
        ip_reverse_table = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25,
        ]
        res = []; tmp = ""

        merging_str = "".join(self.l) + "".join(self.r)

        for i in range(len(ip_reverse_table)):
            tmp += merging_str[ip_reverse_table[i] - 1]
            if len(tmp) == 8:
                res.append(tmp)
                tmp = ""

        return res






    def round_16_f(self):
        for i in range(16):
            # 对r进行E拓展(32-->48)
            self.r_tmp = self.E_extend(self.r_tmp)  # 返回的是["",""]
            # 异或
            self.r_tmp = self.to_xor(self.r_tmp, self.key[i])
            # s盒
            self.r_tmp = self.tans_sbox(self.r_tmp)
            # p盒
            self.r_tmp = self.p_subs(self.r_tmp)
            # 得到l_next盒r_next
            self.l,self.r = self.new_xor(self.l,self.r,self.r_tmp)     # 存在错误：self.r_previous没有更替
            # 使得r_tmp等于r，方便下一轮的r_tmp继续打工
            self.r_tmp = self.r

            self.output_res(self.l, self.r, self.key[i], i+1)

        # F函数的16轮需要特殊处理
        tmp = self.r
        self.r = self.l
        self.l = tmp

        self.output_res(self.l, self.r, self.key[15], 16)

class CBC(ECB):
    def add_xor(self):
        text = "".join(self.text)
        iv = "".join(self.iv)
        tmp = "" ; res = []

        for i in range(len(text)):
            tmp += str(eval(text[i])^eval(iv[i]))
            if len(tmp) == 8:
                res.append(tmp)
                tmp = ""
        return res

class CFB(ECB):
    def add_xor(self):
        part_text = ""

        for i in range(len(self.text[0])):
            part_text += str(eval(self.text[0][i])^eval(self.iv_des[0][i]))

        return part_text

class OFB(CFB):
    pass

class CTR(OFB):
    pass
