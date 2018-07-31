# by luffycity.com
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect


class ValidPermission(MiddlewareMixin):

    def process_request(self,request):

        # 当前访问路径
        current_path = request.path_info

        # 检查是否属于白名单
        valid_url_list = ["/login/", "/admin/.*", '/logout/']

        for valid_url in valid_url_list:
            ret = re.match(valid_url, current_path)
            if ret:
                return None

        # 校验是否登录

        user_id = request.session.get("user_id")

        if not user_id:
            return redirect("/login/")

        # 校验权限
        permission_list = request.session.get("permission_list", [])  # ['/users/', '/users/add', '/users/delete/(\\d+)', 'users/edit/(\\d+)']

        flag = False
        for permission in permission_list:

            permission = "^%s$" % permission

            ret = re.match(permission, current_path)
            if ret:
                flag = True
                break
        if not flag:
            return HttpResponse("没有访问权限！")

        return None
