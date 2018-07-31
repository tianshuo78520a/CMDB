# by luffycity.com


def initial_session(user, request):
    """
    获取所有可以访问页面的url
    :param user:
    :param request:
    :return:
    """
    permissions = user.roles.all().values("permissions__url").distinct()

    permission_list = []

    for item in permissions:
        permission_list.append(item["permissions__url"])

    request.session["permission_list"] = permission_list
