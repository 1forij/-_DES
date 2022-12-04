import datetime
from django.contrib.contenttypes.models import ContentType
from read_count.models import ReadNum, ReadDetail

from django.utils import timezone
from django.db.models import Sum

# 假如是blog_detail的请求
# tab_obj:blog_current  tab:BLog
# 未曾读，返回cookie_key，阅读量+1
# 曾读且CD 不做任何操作
def toBe_or_NotToBe(request, tab_obj):# 未读过则计数（不一定是blog，也可以是其他的）
    tab = ContentType.objects.get_for_model(tab_obj)
    cookie_key = '%s_%s_read'%(tab.model, tab_obj.id)
    if not request.COOKIES.get(cookie_key):
        # 总浏览量计数+1
        # 这里不用判断博客的对应阅读量条目是否存在，因为在get_read_num已经建立相应的阅读数量条目
        read_obj = ReadNum.objects.filter(content_type=tab, object_id=tab_obj.id)
        read_num_all = read_obj[0].read_num
        read_obj.update(read_num = read_num_all + 1)

        # 今日浏览量计数+1
        today = timezone.now().date()# 获得当前日期
        ReadDetail.objects.get_or_create(date=today, content_type=tab, object_id=tab_obj.id)

        today_read_obj = ReadDetail.objects.filter(date=today, content_type=tab, object_id=tab_obj.id)
        read_num_today = today_read_obj[0].read_num
        today_read_obj.update(read_num = read_num_today + 1)

        return cookie_key
    return ""

def readNum_recent_senven(today, contenttype):

    dates = []      # 记录日期
    week_datas = []  # 记录对应日期的浏览量

    for i in range(7,0,-1):     # 前七天
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m-%d'))         # 获取日期字符串，存入dates

        oneday_data = ReadDetail.objects.filter(content_type=contenttype, date=date)
        dict = oneday_data.aggregate(oneday_date_sum=Sum('read_num'))  # 聚合函数，返回值是一个字典
        week_datas.append(dict["oneday_date_sum"] or 0)      # 如果字典中key="oneday_date_sum"，找不到对应value，则返回0

    return dates,week_datas

# 近7天热门（博客/教程/等）前五
def hotest_blog(today, contenttype):
    start_time = today - datetime.timedelta(weeks=1)
    end_time = today

    hot_datas = ReadDetail.objects.filter(content_type=contenttype, date__range=(start_time, end_time)).values('content_type','object_id').annotate(read_num_sum=Sum('read_num')).order_by('-read_num_sum')
    print(hot_datas,len(hot_datas))

    if len(hot_datas) >= 5:
        return hot_datas[:5]
    return hot_datas

