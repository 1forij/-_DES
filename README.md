<a name="p3HpI"></a>
# 基于WEB程序设计的DES实现
某校网络安全设计——DES的编程实现~

---

<a name="xr5WX"></a>
## 项目要求

1. 实现简单的加解密界面
2. 加解密对象输入输出可选：字符串或文件
3. 工作模式可选：ECB，CBC，CTR，OFB，CFB

---

<a name="RsOwj"></a>
## 实现情况
<a name="Pe3h0"></a>
### 简单的加解密界面
效果图如下
> 高情商：简约而不简单，低情商："简单"

前端不怎么会，基于前端框架Bootstrap快速实现，能用就行。(菜狗)<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670850513971-2b7ce5b8-01ff-49ca-8fa7-f8cc519e1077.png#averageHue=%23fcfcfc&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=737&id=u683a240b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1105&originWidth=2239&originalType=binary&ratio=1&rotation=0&showTitle=false&size=87824&status=done&style=none&taskId=u7dba5077-906c-4611-9f45-5252dc1220f&title=&width=1492.6666666666667)

---

<a name="avTtq"></a>
### 加解密对象输入输出可选字符串或文件
对于字符串：<br />通过form表单传递即可<br />对于文件：<br />对于WEB程序而言，输入文件，实质就是要实现文件上传(对应输入)和下载(对应输出)。

为了减少代码量，不对两者单独处理，而是将文件内容读取出来，把问题同化为字符串处理

逻辑图如下：<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851072770-350a773e-9328-4b61-8ecb-888ffa668ca8.png#averageHue=%23ccc2a9&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=525&id=u17d25aa8&margin=%5Bobject%20Object%5D&name=image.png&originHeight=787&originWidth=1402&originalType=binary&ratio=1&rotation=0&showTitle=false&size=71699&status=done&style=none&taskId=ud864ad4e-c163-4631-a9b9-5479d0c9168&title=&width=934.6666666666666)

---

<a name="USv0v"></a>
### 工作模式可选：ECB，CBC，CTR，OFB，CFB
这就是DES算法五种工作模式的实现。
> 起初的实现，只是写了一轮（即单次运算只能处理64位），导致DES的工作模式意义不大，基本没有什么隐蔽性可言。出现这个现象的原因，可能是受密码学书上的单组运算案例所影响吧，实现的时候也只顾着单组实现，证明能写出来，懂这么个意思，就行了。觉得答辩应该也就问问实现的细节，比如说：E拓展，S盒变化等的代码实现。好家伙，答辩的时候就很尴尬...被要求同时处理多组字符串...然后...很尴尬就对了。
> 当天下午，花了近3小时，把多轮数连续的加密给实现了，也意识到多轮同时加密，确实很有必要，不然规律容易被观察出来，很大程度上失去了加解密的意义。

下面给出各个模式的流程图：<br />ECB（[via: Tom rush的博客-CSDN博客_des算法流程图](https://blog.csdn.net/weixin_44995613/article/details/105970353)）<br />![des加密流程.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851919192-530cf41e-7692-477b-b474-9b02605187ef.png#averageHue=%23f3f2e3&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=996&id=u54cd173b&margin=%5Bobject%20Object%5D&name=des%E5%8A%A0%E5%AF%86%E6%B5%81%E7%A8%8B.png&originHeight=3792&originWidth=1000&originalType=binary&ratio=1&rotation=0&showTitle=false&size=452234&status=done&style=none&taskId=u6a5e78df-bad8-42e6-9848-044989b8ba1&title=&width=262.66668701171875)![des解密流程.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851919284-1f052118-e55e-4d22-92ea-872533840003.png#averageHue=%23f4f3e4&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=994&id=u83ec1221&margin=%5Bobject%20Object%5D&name=des%E8%A7%A3%E5%AF%86%E6%B5%81%E7%A8%8B.png&originHeight=3948&originWidth=1000&originalType=binary&ratio=1&rotation=0&showTitle=false&size=509359&status=done&style=none&taskId=uc5fca5f6-c12a-465c-a639-e0bdf478842&title=&width=251.6666717529297)![des密钥产生.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851919094-5cc86fe1-96dd-45eb-888b-3214e75d1273.png#averageHue=%23f5f3e5&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=478&id=u7b9b574f&margin=%5Bobject%20Object%5D&name=des%E5%AF%86%E9%92%A5%E4%BA%A7%E7%94%9F.png&originHeight=2360&originWidth=1000&originalType=binary&ratio=1&rotation=0&showTitle=false&size=326781&status=done&style=none&taskId=ubfcc90da-d849-4147-a26d-b26dcc6375f&title=&width=202.66668701171875)

CBC<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851876857-c5836148-b8bd-48c0-b0d9-f1a2b5acf7d5.png#averageHue=%23f8f5f5&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=176&id=uc116e0f1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=264&originWidth=489&originalType=binary&ratio=1&rotation=0&showTitle=false&size=67799&status=done&style=none&taskId=u57c2ee88-b00a-4f56-a11e-77a618150f0&title=&width=326)            ![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670851867595-c997a0d9-fb49-4301-8f2c-8e77346d0752.png#averageHue=%23f9f6f6&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=174&id=uc27a81b9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=261&originWidth=535&originalType=binary&ratio=1&rotation=0&showTitle=false&size=59805&status=done&style=none&taskId=u1c27a3f9-42ad-47d2-b082-b4c68f73e1a&title=&width=356.6666666666667)

CTR<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852024792-60d61adf-51f9-4608-8f28-6c0275edb88e.png#averageHue=%23f8f5f5&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=187&id=u4273c0e9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=280&originWidth=460&originalType=binary&ratio=1&rotation=0&showTitle=false&size=64656&status=done&style=none&taskId=ud91ce179-eb24-43ff-a2a8-1f70dcb1ee5&title=&width=306.6666666666667)                      ![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852032251-b7118e4e-fae1-448f-b726-b5e6d1eeb82a.png#averageHue=%23f9f7f7&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=173&id=u52e756a9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=260&originWidth=470&originalType=binary&ratio=1&rotation=0&showTitle=false&size=61323&status=done&style=none&taskId=ud85e39f6-3b4b-4a2d-bbff-360de93b5d8&title=&width=313.3333333333333)

OFB<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852057977-08d408ef-e288-4ee6-bc06-44d114d0843c.png#averageHue=%23f3f2f2&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=166&id=ub3b5a3e3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=346&originWidth=758&originalType=binary&ratio=1&rotation=0&showTitle=false&size=46666&status=done&style=none&taskId=ue0f3d18f-4093-4261-ba1d-fdf0fe5470e&title=&width=363.3333435058594)![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852061886-d246f52a-19a4-4dca-b6a3-560e99a69bfb.png#averageHue=%23f2f2f2&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=156&id=u3dfc7de3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=325&originWidth=758&originalType=binary&ratio=1&rotation=0&showTitle=false&size=43714&status=done&style=none&taskId=u0944945d-ce2e-432c-bc62-44228e4c5e3&title=&width=363.3333435058594)

CFB<br />![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852115571-2a58d29d-28c8-40da-b9f7-f208e634d0e2.png#averageHue=%23f3f3f3&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=170&id=u5b74ce7e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=362&originWidth=726&originalType=binary&ratio=1&rotation=0&showTitle=false&size=49238&status=done&style=none&taskId=u4830a118-710c-4906-b1cf-55ec203f76c&title=&width=341)![image.png](https://cdn.nlark.com/yuque/0/2022/png/25755897/1670852122660-19a59c63-9f2a-4c60-b08f-764298fc32e2.png#averageHue=%23f2f2f2&clientId=u0bf2c792-5e8c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=168&id=ub5d9ec82&margin=%5Bobject%20Object%5D&name=image.png&originHeight=330&originWidth=726&originalType=binary&ratio=1&rotation=0&showTitle=false&size=46636&status=done&style=none&taskId=u87427e5d-6e66-44b4-a916-da85e8e03d4&title=&width=370)

---

<a name="fJfFt"></a>
## 使用的相关技术
后端：Python Django<br />前端：Bootstrap

---

<a name="d6IqF"></a>
## 简单部署测试
项目目录内写了dockerfile，可通过dockerfile部署测试
```shell
# 把Self_Access_Centre.zip上传到linux当前用户的家目录

# 解压
unzip Self_Access_Centre.zip

# 进入项目
cd Self_Access_Centre

# docker build  创建镜像
docker build -t des:v3 .

# 基于des:v3镜像在后台实例化交互式的一个名为des_ok的容器，且将容器的8000端口映射到宿主机的80端口
docker run -it -d --name des_ok -p 80:8000 des:v3

# 从新的TTY进入des_ok容器
docker exec -it des_ok /bin/bash

# django数据库同步的三步骤（我又没用到数据库...）
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

# 挂起docker
Ctrl + P + Q
```

---

<a name="g6LlF"></a>
## 已知小BUG
就算用户还没上传文件，也把结果文件的超链接显示出来了，总会有人闲的...先去点着玩玩，然后出现报错界面....<br />这个其实可以通过JS或者直接用jQuery来控制a标签的hidden属性即可。
