## Introduction
This is a simple web app written in python Flask to upload a .csv file containing a square matrix of integers and 
performing different functions on it.

## Instructions to Run the project
1. Clone the project locally
2. Once inside the project folder, 
   1. Create a python env: `python3 -m venv .venv`
   2. Activate the env: `. .venv/bin/activate`
   3. Install Flask: `pip install Flask`
3. Run the project: `flask run`. This starts the web server at port 5000 by default.
   1. Optionally if you want to run the server on some other port, you can do so running
      `flask run --port <desired_port>`
4. API endpoints you can hit:
   1. Echo: `curl -F "file=@/path/to/csv_file" -X POST http://127.0.0.1:5000/echo -i`
   2. Invert: `curl -F "file=@/path/to/csv_file" -X POST http://127.0.0.1:5000/invert -i`
   3. Flatten: `curl -F "file=@/path/to/csv_file" -X POST http://127.0.0.1:5000/flatten -i`
   4. Sum: `curl -F "file=@/path/to/csv_file" -X POST http://127.0.0.1:5000/sum -i`
   5. Multiply: `curl -F "file=@/path/to/csv_file" -X POST http://127.0.0.1:5000/multiply -i`

## Running tests
1. Different kinds of bad inputs + good inputs are provided in the sample_inputs folder.
2. test.py uses these files to check against expected output
3. To run test.py, first install pytest in your virtual env using `pip install pytest`
4. Then from the root directory of the folder run `pytest test.py -v`
   
