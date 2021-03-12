import os
from errors import *
from constants import *

def walk_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    if len(parameters) != param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def most_importants_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    if len(parameters) != param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return parameters[0].isdigit() #imprimir error

def recomendation_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    pass

def cycle_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    if len(parameters) != param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def range_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    if len(parameters) != param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def clustering_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    if not len(parameters) <= param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def parameters_error_handler(command: str, param_count: int, parameters: list) -> bool:
    '''
    Verifica que la cantidad de parametros sea valida para cada comando.
    Pre: se verifico el ingreso por consola.
    '''
    if command == WALK:
        return walk_parameter_error_handler(param_count, parameters)
    elif command == MOST_IMPORTANTS:
        return most_importants_parameter_error_handler(param_count, parameters)
    # elif command == RECOMENDATION:
    #     return recomendation_parameter_error_handler(param_count, parameters)
    elif command == CYCLE:
        return cycle_parameter_error_handler(param_count, parameters)
    elif command == RANGE:
        return range_parameter_error_handler(param_count, parameters)
    elif command == CLUSTERING:
        return clustering_parameter_error_handler(param_count, parameters)

def command_handle_error(command: str) -> bool:
    '''
    Verifica que el comando ingresado sea valido.
    Pre: se verifico el ingreso por consola.
    '''
    if command not in COMMANDS:
        print(ERROR_CMD)
        return False
    return True
    
def input_handle_error(splitted_line: list) -> bool:
    '''
    Verifica que la entrada por consola sea valida.
    Pre: se ingreso por consola.
    '''
    if len(splitted_line) < 1:
        print(ERROR_INPUT)
        return False
    elif len(splitted_line) == 1:
        if CLUSTERING in splitted_line:
            return True
        else:
            print(ERROR_PARAM_COUNT)
            return False
    return True

def path_handle_error(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError("Buscate un archivo de verdad.")