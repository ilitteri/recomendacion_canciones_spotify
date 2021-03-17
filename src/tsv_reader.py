from error_handling import path_handle_error

def read_input(path: str) -> list:
    '''Lee el archivo de entrada y lo parsea.'''
    path_handle_error(path)
    parsed_lines = []
    with open(path, "r", encoding='utf-8') as input_file:
        line = input_file.readline().rstrip('\n') # Header
        line = input_file.readline().rstrip('\n')
        while line:
            parsed_lines.append(line.split('\t'))
            line = input_file.readline().rstrip('\n')

    return parsed_lines
