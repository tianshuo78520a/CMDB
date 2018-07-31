from django.shortcuts import render, HttpResponse, redirect
from app01.service.perssions import initial_session
from django.forms import ModelForm
from django.forms import widgets as wid
from app01 import models
from app01.page.page import Pagination
import logging
import re


class ServerForm(ModelForm):

    class Meta:
        model = models.Server
        fields = '__all__'
        labels = {
            'hostname': '主机名',
            'server_status_id': '使用状态',
            'server_type_id': '服务器类型',
            'gpu_number': 'GPU数量',
            'server_lease_last_day': '到期日',
            'docker_type_id': '是否有docker',
            'model_type': '机型',
            'msg': '备注',
            'user_group': '部门',
            'user_info': '负责人',
            'service': '服务',
        }
        widgets = {
            'hostname': wid.TextInput(attrs={'class': 'form-control'}),
            'server_status_id': wid.Select(attrs={'class': 'form-control'}),
            'server_type_id': wid.Select(attrs={'class': 'form-control'}),
            'gpu_number': wid.TextInput(attrs={'class': 'form-control'}),
            'gpu_number': wid.TextInput(attrs={'class': 'form-control'}),
            'model_type': wid.Select(attrs={'class': 'form-control'}),
            'docker_type_id': wid.Select(attrs={'class': 'form-control'}),
            'user_group': wid.Select(attrs={'class': 'form-control'}),
            'service': wid.SelectMultiple(attrs={'class': 'form-control'}),
            'user_info': wid.SelectMultiple(attrs={'class': 'form-control'}),
            'server_lease_last_day': wid.TextInput(attrs={'type': 'date', 'class': 'form-control'})
        }


class UserForm(ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'
        labels = {
            'name': '用户名',
            'pwd': '密码',
            'roles': '用户权限'
        }
        widgets = {
            'name': wid.TextInput(attrs={'class': 'form-control'}),
            'pwd': wid.PasswordInput(attrs={'class': 'form-control'}),
            'roles': wid.SelectMultiple(attrs={'class': 'form-control'})
        }


class UserInfoForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ('name', 'phone', 'email')
        labels = {
            'users': '账号',
            'name': '姓名',
            'phone': '电话',
            'email': '邮箱',
            'user_group': '部门'
        }
        widgets = {
            'users': wid.Select(attrs={'class': 'form-control'}),
            'name': wid.TextInput(attrs={'class': 'form-control'}),
            'phone': wid.TextInput(attrs={'class': 'form-control'}),
            'email': wid.EmailInput(attrs={'class': 'form-control'}),
        }


class ServiceForm(ModelForm):
    class Meta:
        model = models.Service
        fields = ('name',)
        labels = {
            'name': '服务名'
        }
        widgets = {
            'name': wid.TextInput(attrs={'class': 'form-control'})
        }


logger = logging.getLogger('sourceDns.webdns.views')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        ret = models.User.objects.filter(name=user, pwd=pwd).first()
        if ret:
            request.session["user_id"] = ret.pk
            request.session['user_name'] = ret.userinfo.name
            initial_session(ret, request)
            logger.info(user)
            return redirect('/index/')
        else:
            logger.error(user)
            return HttpResponse('登陆失败')


def logout(request):
    request.session['user_id'] = None
    return redirect('/login/')


def passwd(request):
    error = ''
    if request.method == 'POST':
        old_pwd = request.POST.get('old_pwd')
        pwd = request.POST.get('pwd')
        new_pwd = request.POST.get('new_pwd')
        user_id = request.session.get('user_id')
        obj = models.User.objects.filter(id=user_id).first()
        if old_pwd == obj.pwd and pwd == new_pwd and pwd != '':
            obj.pwd = new_pwd
            obj.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('输入有误')
    per_list = request.session.get('permission_list')
    return render(request, 'passwd.html', {'error': error, 'per_list': per_list})


# 首页
def index(request):
    re_list = models.Server.objects.all()
    per_list = request.session.get('permission_list')

    if request.method == 'POST':
        host = request.POST.get('host')
        if host == '空闲':
            re_list = models.Server.objects.filter(server_status_id=2).all()
            per_list = request.session.get('permission_list')
            return render(request, 'index.html', {'pc_list': re_list, 'per_list': per_list})

        if host:
            re_list = []
            server_list = models.Server.objects.all()

            for obj in server_list:
                if obj.hostname:
                    if host in obj.hostname:
                        re_list.append(obj)

            for obj in server_list:
                user = obj.user_info.all()
                for i in user:
                    if host in i.name:
                        re_list.append(obj)

            for obj in server_list:
                if obj.model_type:
                    if host in obj.model_type:
                        re_list.append(obj)
            re_list = set(re_list)

    # 分页
    data_count = len(re_list)
    current_page = int(request.GET.get("page", 1))

    pager = Pagination(data_count, current_page, '/index/')
    user_list = re_list[pager.start:pager.end]
    page_html = pager.page_html()
    return render(request, 'index.html', {'pc_list': user_list, 'page_html': page_html , 'per_list': per_list})


########################## 机器相关 #######################
# 添加机器
def server_add(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/index/')
    form = ServerForm()
    per_list = request.session.get('permission_list')
    return render(request, 'server_add.html', {'form': form, 'per_list': per_list})


# 修改机器
def server_edit(request, pk):
    server_obj = models.Server.objects.filter(id=pk).first()
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server_obj)
        if form.is_valid():
            form.save()
            msg = '%s 修改 %s 机器' % (request.session.get('user_name'), server_obj.hostname)
            logger.info(msg)
            return redirect('/index/')
    form = ServerForm(instance=server_obj)
    per_list = request.session.get('permission_list')
    return render(request, 'edit.html', {'form': form, 'per_list': per_list, 'title': '修改机器'})


# 删除机器
def server_delete(request, pk):
    try:
        obj = models.Server.objects.filter(id=pk)
        msg = '%s 删除 %s 机器' %(request.session.get('user_name'), obj[0].hostname)
        obj.delete()
        logger.info(msg)
    except Exception as e:
        logger.error(e)
    return redirect('/index/')

########################## 用户相关 #######################
# 查看用户
def user(request):
    user_list = models.User.objects.all()
    per_list = request.session.get('permission_list')
    return render(request, 'users.html', {'user_list': user_list, 'per_list': per_list})


# 查看用户详情
def user_info(request):
    user_list = models.UserInfo.objects.all()
    per_list = request.session.get('permission_list')
    return render(request, 'user_info.html', {'user_list': user_list, 'per_list': per_list})


# 添加用户
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('添加成功')
        else:
            return HttpResponse('添加失败')
    form = UserForm()
    per_list = request.session.get('permission_list')
    return render(request, 'edit.html', {'form': form, 'per_list': per_list})


# 添加用户详情
def user_info_add(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('添加成功')
        else:
            return HttpResponse('添加失败')
    form = UserInfoForm()
    per_list = request.session.get('permission_list')
    return render(request, 'edit.html', {'form': form, 'per_list': per_list, 'title': '添加用户详情'})


# 编辑用户详情
def user_info_edit(request, pk):
    user_info_obj = models.UserInfo.objects.filter(id=pk).first()
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=user_info_obj)
        if form.is_valid():
            form.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')
    form = UserInfoForm(instance=user_info_obj)
    per_list = request.session.get('permission_list')
    return render(request, 'edit.html', {'form': form, 'per_list': per_list, 'title': '编辑用户详情'})


# 删除用户
def user_delete(request, pk):
    try:
        models.User.objects.filter(id=pk).delete()
    except Exception as e:
        logger.error(e)
    return HttpResponse('删除成功')


########################## 服务相关 #######################
# 服务
def service(request):
    service_list = models.Service.objects.all()
    per_list = request.session.get('permission_list')
    return render(request, 'service.html', {'service_list': service_list, 'per_list': per_list})


# 添加服务
def service_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        models.Service.objects.create(name=name)
    return render(request, 'service_add.html')


# 修改服务
def service_edit(request, pk):
    obj = models.Service.objects.filter(id=pk).first()
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/service/')
        else:
            return HttpResponse('修改失败')
    form = ServiceForm(instance=obj)
    per_list = request.session.get('permission_list')
    return render(request, 'edit.html', {'form': form, 'per_list': per_list, 'title': '修改服务'})


# 删除服务
def service_delete(request, pk):
    try:
        models.Service.objects.filter(id=pk).delete()
    except Exception as e:
        logger.error(e)
    return HttpResponse('删除成功')


# 服务详情
def service_info(request, pk):
    service_obj = models.Service.objects.filter(id=pk).first()
    per_list = request.session.get('permission_list')
    return render(request, 'service_info.html', {'service_obj': service_obj, 'per_list': per_list})


