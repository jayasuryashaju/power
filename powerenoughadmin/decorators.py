from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """
    Decorator for views that checks whether the user is authenticated and is a superuser.
    If not, redirects to the login page.
    """
    decorated_view = user_passes_test(
        lambda user: user.is_authenticated and user.is_superuser,
        login_url='powerenoughadmin:login'
    )(view_func)
    return decorated_view