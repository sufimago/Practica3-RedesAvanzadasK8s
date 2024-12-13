import pytest
from app import app  # Asegúrate de importar tu aplicación Flask aquí
from flask import Flask, jsonify

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():  # Asegúrate de usar el contexto de la app
            yield client

# Test de health check
def test_health_check(client):
    """Probar el endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'{"status":"ok"}' in response.data

# Test del endpoint principal '/'
def test_index(client):
    """Probar la página principal"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Conexion con exito' in response.data or b'Error con la base de datos' in response.data

