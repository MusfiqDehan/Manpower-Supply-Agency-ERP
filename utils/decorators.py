from functools import wraps
from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def render_403_template(request, permission_codename):
    if "view" in permission_codename:
        return render(request, "errors/403.html", status=403)
    elif "update" in permission_codename or "delete" in permission_codename:
        return render(request, "errors/403-contents.html", status=403)
    else:
        raise PermissionDenied


def custom_permission_required(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)

                user_groups = request.user.Group_Users.all()
                if not user_groups:
                    return render_403_template(request, permission_codename)

                for user_group in user_groups:
                    group_permissions = user_group.permissions.all()
                    for perm in group_permissions:
                        if perm.codename == permission_codename:
                            return view_func(request, *args, **kwargs)

                return render_403_template(request, permission_codename)
            except Exception as e:
                print(f"Error in custom_permission_required: {e}")
                return render_403_template(request, permission_codename)

        return _wrapped_view

    return decorator
