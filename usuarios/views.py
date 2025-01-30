from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from .models import UserToken
from .decorators import token_required

@csrf_exempt    # Decorador para desactivar la proteccion csrf de django
@require_http_methods(["POST"]) # Decorador para permitir solo peticiones POST
def auth(request):
    try:
        # Cargo los datos del request
        data = json.loads(request.body)
        
        # Reviso que la petición tenga los campos requeridos
        if not all(k in data for k in ['user', 'password']):
            response_data = {
                'error_message': 'Petición inválida'
            }
            
            return JsonResponse(response_data, status=401)
        
        # Organizo los datos en variables para facilitar su uso
        username = data['user']
        password = data['password']
        
        # Intento autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        # Verifico que el usuario exista y que las credenciales sean correctas para generar token y la respuesta JSON
        if user is not None:
            token = UserToken.generate_token(user)
            response_data = {
                'token': token,
                'user': user.username
            }
            
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'error_message': 'Credenciales inválidas o usuario inexistente'
            }
            
            return JsonResponse(response_data, status=401)
    
    # Manejo errores de decodificacion de cadenas JSON
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'JSON inválido'}, 
            status=400
        )
    # Manejo de otros errores que puedan ocurrir con el JSON
    except Exception as e:
        return JsonResponse(
            {'error': str(e)}, 
            status=500
        )

@token_required # Decorador para validar el token
def user(request):
    if request.method != 'GET':
        return JsonResponse({'error: Metodo no permitido'}, status=405)
    
    # Obtengo todos los usuarios
    users = User.objects.all()
    # Creo una lista con los datos de los usuarios
    users_list = [
        {
            'user_name': user.first_name,
            'user_lastname': user.last_name,
        }
        for user in users
    ]
    # Envio la lista de usuarios en formato JSON
    return JsonResponse({'users': users_list}, status=200)
                