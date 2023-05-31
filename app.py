from flask import Flask, request

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['TESTING'] = False

def request_validations(request):
    """
    Helper function to validate the incoming request
    Checks performed:
    1. request is a post request
    2. Request has a file uploaded with param "file"
    3. Uploaded file ends is in csv file format
    :param request: Incoming Http request
    :return: None if all validations pass, error message with 400 response code if validation fails
    """
    if request.method != "POST":
        return "Only http POST verb supported", 400

    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if not file.filename.endswith('.csv'):
        return 'Invalid file format, only CSV files are allowed', 400

    return None

def is_integer(n):
    """
    Helper to check if a string can be parsed as an integer
    Ex. of allowed values: 1 and 1.0
    Ex. of bad values: 1.23 and any non-numeric input
    :param n:
    :return: Boolean if value is an integer
    """
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def matrix_validations(matrix):
    """
    Helper to valid matrix. Performs 3 validations:
    1. all elements are integers
    2. all rows have same number of columns
       Ex. of invalid input:
            1, 2, 3
            4, 5, 6, 7, 8
    3. Matrix is a square matrix i.e. number of rows == number of columns

    :param matrix:
    :return: None if all validations pass, error message with 400 response code if validation fails
    """
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if not is_integer(matrix[row][col]):
                return f'Invalid matrix element at row:{row}, col:{col} => "{matrix[row][col]}", only integers allowed', 400

    num_cols = len(matrix[0])
    for row in matrix:
        col_len = len(row)
        if col_len != num_cols:
            return 'Invalid matrix: unequal number of columns across rows', 400

    num_rows = len(matrix)
    if num_rows != num_cols:
        return f'Invalid matrix dimension: {num_rows} x {num_cols}, only square matrices allowed', 400

    return None
def parse_file_to_matrix(request):
    """
    Helper to parse request to matrix of string integers
    :param request: Http request containing the .csv file
    :return: matrix of integers stored as strings
    """
    file = request.files['file']
    contents = file.read().decode('utf-8')
    lines = contents.split('\n')
    matrix = []
    for line in lines:
        matrix.append(line.split(","))
    return matrix

def print_matrix(matrix):
    """
    Helper function to print a matrix
    :param matrix: 2-dimensional square matrix of integers stored as strings
    :return: a string of numbers seperated by ",". Each row is seperated by "\n" (new line)
    """
    mat_str = ""
    for row in matrix:
        row_str = ",".join(row)
        mat_str += row_str
        mat_str += "\n"
    return mat_str

def run_validations(request):
    """
    run_validations is a helper function that calls 2 validations:
    1. Request validations
    2. Matrix validations
    If none of the above validations fail, it returns the parsed matrix
    along with an HTTP 200
    """
    request_error = request_validations(request)
    if request_error:
        return request_error
    matrix = parse_file_to_matrix(request)
    is_bad_matrix = matrix_validations(matrix)
    if is_bad_matrix:
        return is_bad_matrix
    return matrix, 200


@app.route("/echo", methods=["POST"])
def echo():
    """
    echo() takes a .csv file containing a valid square matrix as input and prints it
    :return: Http 200 with parsed matrix from csv
    """
    output, httpCode = run_validations(request)
    if httpCode != 200:
        return output, httpCode
    matrix = output
    return print_matrix(matrix), 200

def invert_matrix(matrix):
    dimension = len(matrix)
    inverted_matrix = [[0 for _ in range(dimension)] for _ in range(dimension)]
    for row in range(dimension):
        for col in range(dimension):
            inverted_matrix[row][col] = matrix[col][row]
    return inverted_matrix

@app.route("/invert", methods=["POST"])
def invert():
    """
    invert() takes a .csv file containing a valid square matrix as input and transposes it
    :return: Http 200 with transposed matrix
    """
    output, httpCode = run_validations(request)
    if httpCode != 200:
        return output, httpCode
    matrix = invert_matrix(output)
    return print_matrix(matrix), 200

def flatten_matrix(matrix):
    acc = []
    for row in matrix:
        acc.extend(row)
    return [acc]

@app.route("/flatten", methods=["POST"])
def flatten():
    """
    flatten() takes a .csv file containing a valid square matrix as input and outputs the
    flattened matrix as a single row
    :return: Http 200 with flattend matrix
    """
    output, httpCode = run_validations(request)
    if httpCode != 200:
        return output, httpCode
    matrix = flatten_matrix(output)
    return print_matrix(matrix), 200

def sum_matrix(matrix):
    total = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            total += int(matrix[row][col])
    return total

@app.route("/sum", methods=["POST"])
def sum():
    """
    sum() takes a .csv file containing a valid square matrix as input and outputs the sum of all integers in the matrix
    :return: Http 200 with sum of matrix elements (ints)
    """
    output, httpCode = run_validations(request)
    if httpCode != 200:
        return output, httpCode
    total = sum_matrix(output)
    return str(total), 200

def multiply_matrix(matrix):
    product = 1
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            product *= int(matrix[row][col])
    return product

@app.route("/multiply", methods=["POST"])
def multiply():
    """
    multiply() takes a .csv file containing a valid square matrix as input and outputs the product of all integers in the matrix
    :return: Http 200 with product of matrix elements (ints)
    """
    output, httpCode = run_validations(request)
    if httpCode != 200:
        return output, httpCode
    product = multiply_matrix(output)
    return str(product), 200