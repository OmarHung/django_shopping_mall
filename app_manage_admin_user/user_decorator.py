from django.http import HttpResponseRedirect

def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('admin_username'):
            return func(request,*args,**kwargs)
        else:
            res = HttpResponseRedirect('/manage_login/login/')
            res.set_cookie('url', request.get_full_path())
            return res

    return login_fun