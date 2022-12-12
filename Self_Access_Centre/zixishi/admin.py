from django.contrib import admin

from zixishi.models import Course, Building

# 用于展示类(表)的属性和方法
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('building_name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name','teacher','classes','building')