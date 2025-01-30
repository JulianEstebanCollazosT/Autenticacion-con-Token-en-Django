from django.http import JsonResponse
from functools import wraps
from .models import UserToken

def token_required(view_func):
    @wraps(view_func)   # Permite que el decorador no modifique el nombre de la función
    def wrapped_view(request, *args, **kwargs):
        # Validar que la peticion tenga el formato esperado
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header:
            return JsonResponse({'error': 'Problema al leer la petición'}, status=401)
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Solicitud no tiene formato válido'}, status=401)
        
        # Extraer el token de la solicitud
        token = auth_header.split(' ')[1]
        
        #Validar que el token sea correcto
        try:
            user_token = UserToken.objects.select_related('user').get(token=token)
            request.user = user_token.user
            return view_func(request, *args, **kwargs)
        except UserToken.DoesNotExist:
            return JsonResponse({'error': 'Token inválido'}, status=401)
    
    return wrapped_view