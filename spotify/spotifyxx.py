import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]
# scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username) # add scope

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>> Welcome to Spotipy " + displayName + '!')
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("1 - Search for an Artist")
    print("2 - Your favorite tracks")
    print("x - exit")
    print()
    choice = input("Your choice: ")

    if choice == '1':
        print()
        searchQuery = input("Ok, what's their name? ")
        print()

        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        # print(json.dumps(searchResults, sort_keys=True, indent=4))

        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + ' followers')
        print(artist['genres'][0])
        print()
        print("ALBUMS (recent -> old)")
        print()

        # webbrowser.open(artist['images'][0]['url'])

        # album and track details
        trackURIs = []
        trackArt = []
        albums = {}
        z = 1

        # extract album data
        artistID = artist['id']
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']
        # print(json.dumps(albumResults, sort_keys=True, indent=4))

        for item in albumResults:
            albumID = item['id']
            albumArt = item['images'][0]['url']
            albumName = item['name']
            if albumName in albums.keys(): # no duplicates
                continue
            print(str(z) + ": " + item['name'])
            z+=1
            trackArt.append(albumArt)
            albums[albumName] = []
            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']
            # print(json.dumps(trackResults, sort_keys=True, indent=4))
            for item in trackResults:
                # print("    " + item['name'])
                trackURIs.append(item['uri'])
                print("      " + item['name'])
                albums[albumName].append(item['name'])

            # print("printing albums\n")
            # print(albums)

        while True:
            songSelection = input("Enter a album number to see the art (x to exit): ")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection) - 1])
    if choice == '2':
        top_tracks = spotifyObject.current_user_top_artists()
        print(json.dumps(top_tracks, sort_keys=True, indent=4))

    if choice == 'x': # end program
        break

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
