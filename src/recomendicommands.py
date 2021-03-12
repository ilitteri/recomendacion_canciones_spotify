from constants import SONG_COLOR, USER_COLOR
from error_messages import *
from graph import Graph
from error_handling import error_handler, end_points_error_handler, song_error_handler
from graphtools import bfs_shortest_path, bfs_in_range, cycle_n, clustering, pagerank, personilized_pagerank, random_walk

def print_shortest_path(users_graph: Graph, path: list) -> None:
    '''
    Imprime el camino minimo recibido con el formato exigido.
    '''
    out = ""
    i = 2
    v0 = v1 = v2 = None
    while i < len(path):
        v0 = path[i-2]
        v1 = path[i-1]
        v2 = path[i]
        e01 = users_graph.edge_weight(v0, v1)
        e12 = users_graph.edge_weight(v1, v2)
        out += f'{v0} --> aparece en playlist --> {e01} --> de --> {v1} --> tiene una playlist --> {e12} --> donde aparece --> '
        i += 2
    out += v2
    print(out)

def walk(users_graph: Graph, songs: dict, origin: str, destination: str) -> None:
    '''
    Ejecuta el comando camino minimo:
    Imprime una lista con la cual se conecta (en la menor cantidad de pasos posibles)
    una canción con otra, considerando los usuarios intermedios y las listas de 
    reproducción en las que aparecen.
    '''
    if not end_points_error_handler(songs, origin, destination): 
        return
    path = bfs_shortest_path(users_graph, origin, destination)
    if not error_handler(path, ERROR_PATH_NOT_FOUND):
        return
    print_shortest_path(users_graph, path)

def print_cycle(cycle: list) -> None:
    '''
    Imprime el ciclo recibido con el formato exigido.
    '''
    out = ""
    for v in cycle:
        out += f'{v} --> '
    out += cycle[0]
    print(out)

def get_cycle_n(songs_graph: Graph, song: str, n: int) -> None:
    '''
    Ejecuta el comando ciclo de n canciones:
    Obtiene un ciclo de largo n (dentro de la red de canciones) 
    que comience en la cancion indicada.
    '''
    visited = set()
    cycle = cycle_n(songs_graph, song, song, n, [], visited)
    if not error_handler(cycle, ERROR_CYCLE): 
        return
    print_cycle(cycle)

def in_range(songs_graph: Graph, n: int, song: str) -> None: # O(C+L)
    '''
    Ejecuta el comando todas en rango:
    Obtiene la cantidad de canciones que se encuenten a exactamente n saltos 
    desde la cancion pasada por parametro.
    '''
    if not song_error_handler(songs_graph, song): 
        return
    songs_in_range = bfs_in_range(songs_graph, song, n)
    print(songs_in_range)

def print_clustering_coefficient(songs_graph: Graph, song: str = None) -> None:
    '''
    Calcula e imprime el coeficiente de clustering de la cancion recibida, 
    en caso que no se reciba cancion calcula e imprime el coeficiente de clustering
    promedio de toda la red.
    '''
    if song == None:
        c_coef = sum([clustering(songs_graph, v) for v in songs_graph]) / songs_graph.order()
        print("%.3f" % c_coef)
    else: 
        c_coef = clustering(songs_graph, song)
        print("%.3f" % c_coef)

def print_song_list(song_list: list, n: int) -> None:
    '''
    Imprime la lista de canciones mas importantes con el formato exigido.
    '''
    out = ""
    i = 0
    for _, song in song_list:
        if i == n:
            break
        out += f'{song}{"; " if song != song_list[n-1][1] else ""}'
        i += 1
    print(out)

def initialize_pagerank(graph: Graph, d: float = 0.85) -> dict:
    '''
    Inicializa el valor de pagerank de todos los vertices,
    devuelve un diccionario donde la clave son los vertices 
    y el valor su pagerank.
    '''
    order = graph.order()
    return dict.fromkeys(graph, (1 - d) / order)

def sort_most_importants(songs: dict, most_importants: dict):
    '''
    Filtra en una lista las canciones del diccionario recibido
    y luego la ordena en forma descendiente segun su valor de pagerank
    y la devuelve.
    '''
    return sorted([(most_importants[v], v) for v in most_importants if v in songs], reverse=True)

def load_most_importants(users_graph: Graph, songs: dict) -> list:
    '''
    Devuelve las n canciones mas centrales/importantes del mundo segun el 
    algoritmo de pagerank, ordenadas de mayor importancia a menor importancia.
    '''
    initial_ranks = initialize_pagerank(users_graph)
    pagerank(users_graph, users_graph.random_vertex(), initial_ranks)
    return sort_most_importants(songs, initial_ranks)

def initialize_personalized_pagerank(path: list, recommended: dict) -> None:
    '''
    Inicializa el valor de pagerank personalizado de todos los vertices
    '''
    for v in path:
        if v not in recommended:
            recommended[v] = 1

def sort_recommendations(liked_songs: list, songs: dict, users: dict, rec_type: str, recommendations: dict) -> list:
    '''
    Devuelve una lista de canciones o usuarios dependiendo del tipo de recomendacion solicitado,
    esta estara ordenada de mayor a menor importancia
    '''
    if rec_type == USER_COLOR:
        return sorted([(recommendations[v], v) for v in recommendations if v in users and v not in liked_songs], reverse=True)
    elif rec_type == SONG_COLOR:
        return sorted([(recommendations[v], v) for v in recommendations if v in songs and v not in liked_songs], reverse=True)

def recommend(users_graph: Graph, users: dict, songs: dict, rec_type: str, liked_songs: list):
    '''
    Ejecuta el camando recomendacion:
    Da una lista de n usuarios o canciones para recomendar, dado el listado de 
    canciones que ya sabemos que le gustan a la persona a la cual recomedar.
    '''
    recommendations = {}
    for song in liked_songs:
        path = random_walk(users_graph, song)
        initialize_personalized_pagerank(path, recommendations)
        personilized_pagerank(users_graph, recommendations, path)
    return sort_recommendations(liked_songs, songs, users, rec_type, recommendations)