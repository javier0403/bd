from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TransformedData
from .serializers import TransformedDataSerializer
import os
import mysql.connector
from django.conf import settings
import os
from django.http import JsonResponse

@api_view(['POST'])
def transform_data(request):
    try:
        # Obtener credenciales de variables de entorno
        BDname = os.getenv('DB_NAME')
        Usuario = os.getenv('DB_USER')
        Contraseña = os.getenv('DB_PASSWORD')
        Host = os.getenv('DB_HOST')
        Puerto = os.getenv('DB_PORT')

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            user=Usuario, password=Contraseña,
            host=Host, port=Puerto,
            database=BDname
        )

        # Verificar la conexión
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Obtener la consulta SQL desde la variable de entorno
            insert_query = os.getenv('INSERT_QUERY')

            # Ejecutar la consulta
            cursor.execute(insert_query)
            conexion.commit()

            cursor.close()
            conexion.close()

            return JsonResponse({'status': 'success', 'message': 'Datos insertados correctamente'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo conectar a la base de datos'})
    except mysql.connector.Error as error:
        return JsonResponse({'status': 'error', 'message': f'Error: {error}'})

@api_view(['GET'])
def get_transformed_data(request):
    try:
        # Obtener credenciales de variables de entorno
        BDname = os.getenv('DB_NAME')
        Usuario = os.getenv('DB_USER')
        Contraseña = os.getenv('DB_PASSWORD')
        Host = os.getenv('DB_HOST')
        Puerto = os.getenv('DB_PORT')

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            user=Usuario, password=Contraseña,
            host=Host, port=Puerto,
            database=BDname
        )

        # Verificar la conexión
        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)

            # Ejecutar consulta para obtener los datos transformados
            cursor.execute("SELECT * FROM datos")
            rows = cursor.fetchall()

            # Imprimir los datos
            for row in rows:
                print(row)

            cursor.close()
            conexion.close()

            return JsonResponse({'status': 'success', 'data': rows})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo conectar a la base de datos'})
    except mysql.connector.Error as error:
        return JsonResponse({'status': 'error', 'message': f'Error: {error}'})

