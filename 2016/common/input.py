import os


def read(python_file_name):
    with open(__get_input_data_file_path(python_file_name)) as f:
        return f.read()
    return ['']

def readline(python_file_name):
    return readlines(python_file_name)[0]

def readlines(python_file_name):
    return read(python_file_name).splitlines()

def __get_input_data_file_path(python_file_name):
        return f'data/{os.path.splitext(python_file_name)[0]}.txt'
