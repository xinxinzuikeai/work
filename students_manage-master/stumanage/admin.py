# coding:utf8
from django.contrib import admin
from models import *

class StuTempAdmin(admin.TabularInline):
    model = Student
    # extra = 3

class ClassAdmin(admin.ModelAdmin):
    inlines = [StuTempAdmin]
    list_display = ['id', 'name', 'pub_time', 'isDelete']
    list_filter = ['pub_time']
    search_fields = ['name']

# @admin.register(Student)  # 也可以通过装饰器来注册
class StudentAdmin(admin.ModelAdmin):
    # 显示男女函数
    def generFun(self):
        if self.gender:
            return "男"
        else:
            return "女"
    list_display = ['id', 'name', generFun, 'pub_time', 'isDelete']
    list_filter = ['className']
    search_fields = ['name']
    # 这是每页显示几条信息
    list_per_page = 5
    fieldsets = [
        ('基本', {'fields': ['name', 'age', 'gender', 'score', 'email',  'className']}),
        ('可选', {'fields': ['tel', 'avatar', 'isDelete']}),
    ]

admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(UserProfile)
admin.site.register(Text)  # 注册富文本