import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from song_model import Song
from song_dao import dao_get_all_songs, dao_save_songs
from db import create_tables

from typing import List

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_songs(query: str) -> list [Song]:
    results = sp.search(query, limit =10)


    songs = []
    for track in results["tracks"]["items"]:
        song = Song(
            title=track["name"],
            artist=track["artists"][0]["name"],
            album=track["album"]["name"],
            spotify_id=track["id"]
        )

        songs.append(song)
    
    return songs 

if __name__ == '__main__':
    create_tables()

    while True:
        selection = input('''
                          Enter:
                            s - to search
                            g - to print all songs in the db
                            q - to quit
                            ''')
        selection = selection.lower()

        if selection == 'q':
            break 

        elif selection == 'g':
            print("All songs in the database: ")
            all_songs = dao_get_all_songs()
            for song in all_songs:
                print(f"Title: {song.title} Artist: {song.artist} Album: {song.album}")

        elif selection == "s":
            search_query = input("Enter your search: ")
            songs = search_songs(search_query)

            if len(songs) > 0:
                print(f"Songs returned: len(songs)")
                for i, song in enumerate(songs, start=1):
                    print(f"{i}: Title: {song.title} Artist: {song.artist}")

                save_choice = input("Do you want to save these songs (y/n): ")
                if save_choice.lower() == 'y':
                    dao_save_songs(songs)
                else: 
                    print("Songs not saved")
            else:
                print("No songs were found for your search")
