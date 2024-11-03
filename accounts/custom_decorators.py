from django.shortcuts import redirect

def redirect_if_authenticate(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return func(request, *args, **kwargs)
    return wrapper