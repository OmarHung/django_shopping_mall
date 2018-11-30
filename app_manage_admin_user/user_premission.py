from django.http import HttpResponseRedirect


def premission(func, type):
    def premission_fun(request, *args, **kwargs):
        if 'all' in request.session.admin_premission or type in request.session.admin_premission:
            return func(request, *args, **kwargs)
        else:
            res = HttpResponseRedirect('/manage_login/login/')
            return res

    return premission_fun