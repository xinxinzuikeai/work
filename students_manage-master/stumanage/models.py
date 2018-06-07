# coding:utf-8
from __future__ import unicode_literals  # 2.x -> 3.x的编码模块
from django.db import models
from django.contrib.auth.models import User  # 系统用户
from tinymce.models import HTMLField  # 富文本

# 自定义管理器.并重写get_queryset()方法
class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager, self).get_queryset().filter(isDelete=False)

class Class(models.Model):
    name = models.CharField(max_length=32, verbose_name="班级名字")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否已删除")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name
        ordering = ["id"]

class Student(models.Model):
    # obj = StudentsManager()  # 此类一但实例化后,原生的objects就不好使了
    name = models.CharField(max_length=32, verbose_name="学生姓名")
    age = models.IntegerField(verbose_name="学生年龄")
    gender = models.BooleanField(default=True, verbose_name="性别")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="学生成绩")  # 一共5位数,小数占两位
    email = models.EmailField(null=True, blank=True, verbose_name="学生邮箱")
    tel = models.BigIntegerField(verbose_name="学生电话")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    className = models.ForeignKey(Class)
    avatar = models.ImageField(upload_to='avatar/', verbose_name='头像', default='avatar/default.jpg')
    isDelete = models.BooleanField(default=False, verbose_name="是否已删除")

    def __unicode__(self):
        return self.name

    # 定义一个类方法,用来创建 学生对象
    @classmethod
    def createStudent(cls, name, age, gender, score, email, tel, className_id, isDelete=False):
        stu = cls(name=name,
                  age=age,
                  gender=gender,
                  score=score,
                  email=email,
                  tel=tel,
                  className_id=className_id,
                  isDelete=isDelete
                  )
        return stu


    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name
        # 后台中以哪个字段来排序
        ordering = ["id"]
        # 可以自定义数据表的名称(建议小写),默认为:项目名小写_类名小写
        db_table = "student"

class UserProfile(models.Model):
    phone = models.CharField(max_length=20, verbose_name="手机号")
    nick = models.CharField(max_length=32, verbose_name="昵称")
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name = "系统用户拓展表"
        verbose_name_plural = verbose_name
        ordering = ["id"]

# 富文本类
class Text(models.Model):
    text = HTMLField()

