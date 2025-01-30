Descripcion del proyecto: Creacion de dos endpoints para autenticacion de usuarios por token, y
validacion de Token para vista protegida de lista de usuarios.

Los curls que se utilizaron para probar el buen funcionamiento de la app, fueron los siguientes:

curl -X POST http://127.0.0.1:8000/auth/ \
     -H "Content-Type: application/json" \
     -d '{"user": "your_user", "password": "your_password"}'

curl -X GET http://127.0.0.1:8000/user \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json"

Por supuesto, "your_user", "your_password" y YOUR_TOKEN, deben ser reemplazados por la informacion
correspondiente segun sea el caso.
