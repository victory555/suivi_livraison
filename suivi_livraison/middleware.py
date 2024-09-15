from django.shortcuts import redirect

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass the middleware for login and static files
        if request.path in ['/login/', '/static/'] or request.user.is_authenticated:
            return self.get_response(request)
        
        # Vérifiez si les informations de session existent
        if not request.session.get('username') or not request.session.get('email'):
            return redirect('login')  # redirige vers la page de connexion

        return self.get_response(request)
