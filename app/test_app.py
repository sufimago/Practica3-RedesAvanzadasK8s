import pytest
from app import app  # Asegúrate de importar tu aplicación Flask aquí
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():  # Asegúrate de usar el contexto de la app
            yield client

# Test del endpoint principal '/'
def test_index(client):
    """Probar la página principal"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Conexion con exito' in response.data or b'Error con la base de datos' in response.data


# Test de health check
# Usar mock para simular la conexión de MySQL y Redis
@patch('mysql.connector.connect')
@patch('redis.StrictRedis.ping')
def test_health_check(mock_redis_ping, mock_mysql_connect, client):
    """Probar el endpoint de health check"""

    # Crear un objeto mock para la conexión MySQL
    mock_mysql_connection = MagicMock()
    mock_mysql_connect.return_value = mock_mysql_connection  # Devuelve el objeto mock de conexión MySQL

    # Simula una conexión exitosa de Redis
    mock_redis_ping.return_value = True

    response = client.get('/health')

    # Imprimir los detalles de la respuesta para depurar el error
    print(response.data)

    # Verifica que la respuesta tenga el código 200
    assert response.status_code == 200