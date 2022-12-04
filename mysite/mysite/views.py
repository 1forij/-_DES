from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

from django.utils import timezone
from read_count.views import readNum_recent_senven,hotest_blog

# 导入数据库缓存
from django.core.cache import cache


def index(request):
    today = timezone.now().date()
    contenttype = ContentType.objects.get_for_model(Blog)
    hot_blogs = {}

    # 获取近7天热门博客
    # (先尝试从缓存获取，为None则通过函数获取数据并将其存入缓存)
    hot_datas = cache.get("hot_datas")      # 尝试从缓存获取

    if hot_datas is None:                   # 若没有相应的缓存
        hot_datas = hotest_blog(today, contenttype)     # 函数计算获取
        cache.set("hot_datas",hot_datas,86400)          # 存入缓存，备用
        
    for i in range(len(hot_datas)):
        title = Blog.objects.get(id = hot_datas[i].get("object_id")).title
        hot_blogs [title] = hot_datas[i]

    dates, week_datas = readNum_recent_senven(today, contenttype)

    context = {
        # 近7天热门博客
        'hot_blogs':hot_blogs,
        # 图表
        'week_datas':week_datas,
        'dates':dates,
    }

    return render(request,'index.html',context)
