from datetime import date
import os
import mysql.connector
from rest_framework.decorators import api_view
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import mysql.connector
import os
from django.http import JsonResponse
from datetime import date

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

            # Ejecutar la consulta SQL desde la variable de entorno para insertar datos adicionales
            consulta = os.getenv('INSERT_QUERY')
            if consulta:
                cursor.execute(consulta)
                conexion.commit()

            # Obtener todos los datos de la tabla raw_data
            cursor.execute("SELECT id, nombre, apellido, edad FROM raw_data")
            raw_data = cursor.fetchall()

            # Transformar los datos
            for data in raw_data:
                id, nombre, apellido, fecha_nacimiento = data
                nombre_completo_transformado = f"{nombre} {apellido}"
                edad_nominal_transformada = (date.today() - fecha_nacimiento).days // 365

                # Actualizar los datos en la tabla raw_data
                update_query = """
                UPDATE raw_data
                SET nombre_completo = %s, edad_nominal = %s
                WHERE id = %s
                """
                cursor.execute(update_query, (nombre_completo_transformado, edad_nominal_transformada, id))

            # Confirmar los cambios
            conexion.commit()
            cursor.close()
            conexion.close()

            return JsonResponse({'status': 'success', 'message': 'Datos transformados e insertados correctamente'})
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
            cursor.execute("SELECT * FROM raw_data")
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

