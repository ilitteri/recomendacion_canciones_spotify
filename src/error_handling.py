import os
from graph import Graph
from error_messages import *
from constants import *

def _parameters_error_handler(param_count: int, parameters: tuple) -> bool:
    '''
    Verifica que la cantidad de parametros sea valida dada una tupla de parametros.
    '''
    if len(parameters) != param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def clustering_parameter_error_handler(param_count: int, parameters: tuple) -> bool:
    '''
    Verifica que la cantidad parametros ingresados para el comando clustering 
    sea valida.
    '''
    if not len(parameters) <= param_count:
        print(ERROR_PARAM_COUNT)
        return False
    return True

def parameters_error_handler(command: str, param_count: int, parameters: list) -> bool:
    '''
    Verifica que la cantidad de parametros sea valida para cada comando.
        Pre: se verifico el ingreso por consola.
    '''
    if command != CLUSTERING:
        return _parameters_error_handler(param_count, parameters)
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
    '''
    Verifica que el archivo de la ruta especificada exista.
    '''
    if not os.path.exists(path):
        raise FileNotFoundError()

def song_error_handler(songs_graph: Graph, song: str) -> bool:
    '''
    Verifica si una cancion pertenece a la estructura grafo.
        Pre: el grafo no dirigido que relaciona canciones si aparecen en una
            misma playlist fue creado.
    '''
    if song not in songs_graph:
        print(ERROR_SONG)
        return False
    return True

def error_handler(element: list, msg: str) -> bool:
    '''
    Verifica la existencia de un elemento.
    '''
    if element == None:
        print(msg)
        return False
    return True

def end_points_error_handler(songs: dict, origin: str, destination: str) -> bool:
    '''
    Verifica que las canciones existan en el diccionario de canciones
        Pre: el diccionario de canciones fue cargado.
    '''
    if origin not in songs or destination not in songs:
        print(ERROR_INVALID_SONG)
        return False
    return True