# -_DES
某校网络安全设计的代码实现~

环境：

python 3.7

requirements.txt

问题：

  linux下，文件下载有点小问题
  
修复：

在/zixishi/views.py的down函数的

  path = os.getcwd() + "\\upload"   改为
  
  path = os.getcwd() + "/upload"
  
即可
