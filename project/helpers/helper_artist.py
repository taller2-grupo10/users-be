from project.helpers.helper_media import MediaRequester


def edit_artist(request, albums, songs, artist):
    for album in albums:
        album_id = album["_id"]
        album_request = {"artist.name": request.json["name"]}
        _put_album(album_id, album_request)

    for song in songs:
        song_id = song["_id"]
        artist_name = artist["name"]
        # Modify song artist name if it's the main artist
        if artist_name == song["artists"]["name"]:
            song_request = {"artists.name": request.json["name"]}
            _put_song(song_id, song_request)
        # Modify song collaborator name if it's a featured artist
        elif artist_name in song["artists"]["collaboratorsNames"]:
            song_collaborators_names = song["artists"]["collaboratorsNames"]
            song_collaborators_names = list(
                filter(lambda x: x != artist_name, song_collaborators_names)
            )
            song_collaborators_names.append(request.json["name"])
            song_request = {"artists.collaboratorsNames": song_collaborators_names}
            _put_song(song_id, song_request)


def delete_artist(albums, songs):
    for album in albums:
        album_id = album["_id"]
        _delete_album(album_id)

    for song in songs:
        song_id = song["_id"]
        _delete_song(song_id)


def _delete_album(album_id):
    return MediaRequester.delete(f"albums/{album_id}")


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_album(album_id, request):
    return MediaRequester.put(f"albums/{album_id}", data=request)


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
