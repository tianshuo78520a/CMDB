from django.db import models


class User(models.Model):
    """
    用户名、密码
    """
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    roles = models.ManyToManyField(to="Role")

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    用户信息
    """
    users = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    服务信息
    """
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    机器信息
    """
    hostname = models.CharField(max_length=32)
    server_status_choices = (
        (1, '使用中'),
        (2, '空闲'),
        (3, '租借'),
    )
    server_status_id = models.IntegerField(choices=server_status_choices, default=2)

    server_lease_last_day = models.DateField('到期日', null=True, blank=True)

    server_type_choices = (
        (1, 'GPU'),
        (2, 'CPU'),
    )
    server_type_id = models.IntegerField(choices=server_type_choices)

    model__type_choices = (
        (1, 'K40'),
        (2, 'P40'),
        (3, 'V100')
    )
    model_type = models.IntegerField('机型',choices=model__type_choices, null=True, blank=True)

    gpu_number = models.IntegerField(null=True, blank=True)
    msg = models.CharField('备注', max_length=128, null=True, blank=True)
    docker_type_choices = (
        (1, '有'),
        (2, '没有'),
    )
    docker_type_id = models.IntegerField(choices=docker_type_choices)

    user_info = models.ManyToManyField(UserInfo)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return self.hostname






######################权限相关表########################


class Role(models.Model):
    """
    级别
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to="Permission")

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)

    def __str__(self):
        return self.title







