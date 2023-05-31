import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_echo_success(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 200
        assert response.data == b'1,2,3\n4,5,6\n7,8,9\n'


def test_flatten_success(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/flatten', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 200
        assert response.data == b'1,2,3,4,5,6,7,8,9\n'


def test_invert_success(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/invert', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 200
        assert response.data == b'1,4,7\n2,5,8\n3,6,9\n'

def test_multipy_success(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/multiply', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 200
        assert response.data == b'362880'

def test_sum_success(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/sum', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 200
        assert response.data == b'45'

def test_bad_format_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'bad_format.txt')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'bad_format.txt')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data, content_type='multipart/form-data')

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid file format, only CSV files are allowed'

def test_empty_matrix_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'empty_matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'empty_matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix element at row:0, col:0 => "", only integers allowed'


def test_matrix_floats_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix_floats.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix_floats.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix element at row:0, col:0 => "1.2", only integers allowed'


def test_matrix_headers_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'matrix_headers.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'matrix_headers.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix element at row:0, col:0 => "col1", only integers allowed'

def test_non_int_matrix_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'non_int_matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'non_int_matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix element at row:0, col:0 => "bad", only integers allowed'


def test_non_square_matrix_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'non_square_matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'non_square_matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix dimension: 2 x 3, only square matrices allowed'


def test_unequal_cols_matrix_failure(client):
    # Prepare a sample CSV file for testing
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_inputs', 'unequal_cols_matrix.csv')
    with open(csv_file_path, 'rb') as file:
        data = {'file': (file, 'unequal_cols_matrix.csv')}

        # Send a POST request to the endpoint with the sample CSV file
        response = client.post('/echo', data=data)

        # Assert the response is successful
        assert response.status_code == 400
        assert response.data == b'Invalid matrix: unequal number of columns across rows'