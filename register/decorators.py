from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group= list()
                groups = request.user.groups.all()
                for i in range(len(groups)):
                    group += [groups[i].name]
            
            if any(elem in allowed_roles  for elem in group):
                
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

