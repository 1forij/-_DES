from django.db import models

# Create your models here.

class Building(models.Model):
    building_name = models.CharField(max_length=50)

    # 在被引用时显示自身字段的名称
    def __str__(self):
        return self.building_name

class Course(models.Model):
    # 课程名
    course_name = models.CharField(max_length=100)
    # 授课老师
    teacher = models.CharField(max_length=100)
    # 班级
    classes = models.CharField(max_length=100)
    # 上课地点
    building = models.ForeignKey(Building ,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "<Course:%s>"%self.course_name