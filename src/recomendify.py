#!/usr/bin/python3
from os import listxattr
import sys
import json
from typing import List
from graph import Graph, Edge, Vertex
from user import User
from playlist import Playlist
from song import Song

USER_COLOR = "user"
SONG_COLOR = "song"

def load_playlists_song_structure(playlists: dict, songs: dict) -> Graph:
    graph = Graph()

    for song in songs:
        graph.addVertex(Vertex(song, songs[song], SONG_COLOR))

    for playlist in playlists:
        added = {}
        for song1 in playlists[playlist]:
            added[song1] = True
            for song2 in playlists[playlist]:
                if not (song1 in added and song2 in added):
                    graph.addEdge(Edge(graph.getVertex(song1), graph.getVertex(song2)))
    
    return graph

def load_user_song_structure_(lines: list) -> Graph:
    graph = Graph()
    for line in lines:
        _, user_id, track_name, artist, *_ = line
        user = Vertex(user_id, color=USER_COLOR)
        song = Vertex(track_name+"-"+artist, color=SONG_COLOR)
        graph.addVertex(user)
        graph.addVertex(song)
        graph.addEdge(Edge(user, song))

    return graph

def read_input(path) -> list:
    parsed_lines = []
    with open(path, "r") as input_file:
        line = input_file.readline().rstrip('\n')
        line = input_file.readline().rstrip('\n')
        while line:
            parsed_lines.append(line.split('\t'))
            line = input_file.readline().rstrip('\n')
    return parsed_lines

def process_stdin():
    while True:
        command = input("")

def load_data(lines: list) -> tuple:
    songs = {}
    users = {}
    playlists = {}
    for line in lines:
        _, user_id, track_name, artist, playlist_id, playlist_name, genres = line

        if playlist_id not in playlists:
            playlists[playlist_id] = Playlist(playlist_id, playlist_name)
        if user_id not in users:
            users[user_id] = User(user_id)
        if playlist_id not in users[user_id]:
            users[user_id].addPlaylist(playlists[playlist_id])
        if track_name+"-"+artist not in songs:
            song = Song(track_name+"-"+artist, artist, genres.split(','))
            songs[track_name+"-"+artist] = song
            playlists[playlist_id].addSong(song)
            user_playlist = users[user_id].getPlaylists()[playlist_id]
            user_playlist.addSong(song)
    return users, songs, playlists

def main():
    parsed_lines = read_input(sys.argv[1])
    users, songs, playlists = load_data(parsed_lines)
    user_song_relation = load_user_song_structure_(parsed_lines)
    songs_song_relation = load_playlists_song_structure(playlists, songs)
    del(parsed_lines)
    # process_stdin()
    # print(len(songs))
    # print(len(user_song_relation.getVertices()) - len(users))
    # print(len(songs_song_relation.getVertices()))

main()