import os, platform
from django.shortcuts import render
from django.views import View
from django.conf import settings
from .des_test_modify import ECB, CBC, CFB, OFB, CTR
from django.http import Http404, FileResponse

# 获取数据
class Prepare(View):

    def get(self, request):
        return render(request, 'des_ui.html')

    def post(self, request):

        '''
        如果是输入字符串的加解密，
                                全部数据获取到  args
        如果是上传文件的加解密，
                                模式和操作   args，文件数据保存到本地并格式化获取数据到     字典txt
        '''
        args = request.POST                         # 获取用户的表单参数
        txt_file = request.FILES.get("up_file")     # 获取上传的文件（可以没有，也就代表使用字符串输入）

        filename = os.path.join(settings.MEDIA_ROOT, "default.txt")         # 兼容运行而设置的一些default值
        txt = {}                                                            # 兼容运行而设置的一些default值

        if txt_file:                                # 如果是文件，则读取并保存文件内容
            data = []
            filename = os.path.join(settings.MEDIA_ROOT, txt_file.name)

            for line in txt_file.file:
                data.append(line.decode("utf-8").strip())

            with open(filename, "w") as f:
                for i in data:
                    f.write(i)

            txt = {i: j for i, j in zip(["text","key","iv"], data)}     # 读取上传的文件的数据，达到同化文件问题为字符串问题的效果
# 补充：多轮的实现
        text = args.get("text") or txt['text']
        divided_text = []
        for i in range(0,len(text),16):
            divided_text.append(text[i:i+16])

        result = ""
        result += func(request, args, divided_text, txt)

        content = {
            'result': result,
            'download': filename.split('\\')[-1],
        }

        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        return render(request, 'des_ui.html', content)

def func(request,args,divided_text,txt):
    mode = args.get("mode")
    res = ""
    tmp = []            # 用来传递上轮的密钥给下轮的IV
    for i in range(len(divided_text)):
        if mode == "ECB":
            des_ecb = ECB(args, divided_text[i], txt)                        # 实例化ECB对象
            des_ecb.text = des_ecb.to_str_bin(des_ecb.text)  # 将text转化为2进制矩阵
            des_ecb.key = des_ecb.to_str_bin(des_ecb.key)  # 将key转化为2进制矩阵
            des_ecb.key = des_ecb.get_key_16(des_ecb.key)  # 得到16轮密钥(兼容了加密的key1~16,解密的key16~1)

            des_ecb.l, des_ecb.r, des_ecb.r_tmp = des_ecb.ip_trans(des_ecb.text)    # 得到l0 和 r0
            des_ecb.round_16_f()
            des_ecb.text = des_ecb.ip_invert()
            des_ecb.text = hex(int(f'0b{"".join(des_ecb.text)}',2))[2:].upper().zfill(16)

            res += des_ecb.text

        elif mode == "CBC":
            des_cbc = CBC(args, divided_text[i], txt)                        # 实例化ECB对象
            des_cbc.text = des_cbc.to_str_bin(des_cbc.text) # 将text转化为2进制矩阵

            des_cbc.iv = des_cbc.to_str_bin(des_cbc.iv)     # 第一轮iv
            if i>0:                                         # 其他轮的iv
                des_cbc.iv = tmp

            des_cbc.key = des_cbc.to_str_bin(des_cbc.key)   # 将key转化为2进制矩阵
            des_cbc.key = des_cbc.get_key_16(des_cbc.key)   # 得到16轮密钥(兼容了加密的key1~16,解密的key16~1)

            if args.get("operate") == "encrypt":            # CBC加密前异或
                des_cbc.text = des_cbc.add_xor()                # text和iv异或，返回异或后的2进制矩阵

            des_cbc.l, des_cbc.r, des_cbc.r_tmp = des_cbc.ip_trans(des_cbc.text)  # 得到l0 和 r0
            des_cbc.round_16_f()
            des_cbc.text = des_cbc.ip_invert()

            if args.get("operate") == "decrypt":            # CBC解密后异或
                des_cbc.text = des_cbc.add_xor()                # text和iv异或，返回异或后的2进制矩阵

            tmp = des_cbc.text if args.get("operate") == "encrypt" else des_cbc.to_str_bin(divided_text[i])     # 为下轮做准备(8x8的二进制矩阵)
            des_cbc.text = hex(int(f'0b{"".join(des_cbc.text)}', 2))[2:].upper().zfill(16)

            res += des_cbc.text

        elif mode == "CTR":
            des_ctr = CTR(args, divided_text[i], txt)
            des_ctr.text = des_ctr.to_str_bin(des_ctr.text)  # 将text转化为2进制矩阵
            des_ctr.iv = des_ctr.iv[:len(des_ctr.iv)-1] + hex( int(des_ctr.iv[-1],16) + (i+1) )[-1]   # 实现IV+1的操作(基于十六进制的+1)
            des_ctr.iv = des_ctr.to_str_bin(des_ctr.iv)     # 将iv转化为2进制矩阵
            des_ctr.key = des_ctr.to_str_bin(des_ctr.key)  # 将key转化为2进制矩阵
            des_ctr.key = des_ctr.get_key_16(des_ctr.key, mode)  # 得到16轮密钥(兼容了加密的key1~16,解密的key16~1)

            des_ctr.l, des_ctr.r, des_ctr.r_tmp = des_ctr.ip_trans(des_ctr.iv)  # 得到l0 和 r0
            des_ctr.round_16_f()
            des_ctr.iv_des = des_ctr.ip_invert()

            des_ctr.text = des_ctr.add_xor()

            des_ctr.text = hex(int(f'0b{"".join(des_ctr.text)}', 2))[2:].upper().zfill(16)

            res += des_ctr.text

    if mode == "OFB":
        des_ofb = OFB(args, "".join(divided_text), txt)
        des_ofb.text = des_ofb.to_str_bin(des_ofb.text)  # 将text转化为2进制矩阵
        des_ofb.iv = des_ofb.to_str_bin(des_ofb.iv)  # 将iv转化为2进制矩阵
        des_ofb.key = des_ofb.to_str_bin(des_ofb.key)  # 将key转化为2进制矩阵
        des_ofb.key = des_ofb.get_key_16(des_ofb.key, mode)  # 得到16轮密钥(兼容了加密的key1~16,解密的key16~1)

        for i in range(len(des_ofb.text)):
            des_ofb.l, des_ofb.r, des_ofb.r_tmp = des_ofb.ip_trans(des_ofb.iv)  # 得到l0 和 r0
            des_ofb.round_16_f()
            des_ofb.iv_des = des_ofb.ip_invert()

            tmp_str = des_ofb.add_xor()     # 处理了8位的结果，临时存放

            des_ofb.iv.append(des_ofb.iv_des[0])

            des_ofb.text.pop(0)
            des_ofb.iv.pop(0)

            tmp.append(hex(int(f'0b{tmp_str}', 2))[2:].upper().zfill(2))

        res = "".join(tmp)

    if mode == "CFB":
        des_cfb = CFB(args, "".join(divided_text), txt)
        des_cfb.text = des_cfb.to_str_bin(des_cfb.text) # 将text转化为2进制矩阵
        des_cfb.iv = des_cfb.to_str_bin(des_cfb.iv)     # 将iv转化为2进制矩阵
        des_cfb.key = des_cfb.to_str_bin(des_cfb.key)   # 将key转化为2进制矩阵
        des_cfb.key = des_cfb.get_key_16(des_cfb.key, mode)   # 得到16轮密钥(兼容了加密的key1~16,解密的key16~1)

        for i in range(len(des_cfb.text)):
            des_cfb.l, des_cfb.r, des_cfb.r_tmp = des_cfb.ip_trans(des_cfb.iv)
            des_cfb.round_16_f()
            des_cfb.iv_des = des_cfb.ip_invert()

            tmp_str = des_cfb.add_xor()

            # prepare for next turns    兼容加密和解密

            if des_cfb.operate == "encrypt":
                des_cfb.iv.append(tmp_str)
            else:
                des_cfb.iv.append(des_cfb.text[0])

            des_cfb.text.pop(0)
            des_cfb.iv.pop(0)

            tmp.append(hex(int(f'0b{tmp_str}', 2))[2:].upper().zfill(2))

        res = "".join(tmp)

    return res

def down(request):
    filename = request.GET.get("res")
    path = os.getcwd() + ("\\upload" if platform.system() == "Windows" else "/upload")

    if filename.split('/')[-1] in os.listdir(path):
        file_full_name = os.path.join(settings.MEDIA_ROOT, filename)

        response = FileResponse(open(file_full_name, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + filename

        return response

    return Http404
