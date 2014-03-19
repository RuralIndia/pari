from django.conf import settings
import soundcloud


class SoundCloudHelper:
    def __init__(self):
        pass
    client = soundcloud.Client

    def authenticate(self):
        self.client = soundcloud.Client(client_id=settings.SOUND_CLOUD_CLIENT_ID,
                                        client_secret=settings.SOUND_CLOUD_CLIENT_SECRET,
                                        username=settings.SOUND_CLOUD_USERNAME, password=settings.SOUND_CLOUD_PASSWORD)

        print self.client.get('/me').username

    def create_playlist(self, playlist_title):
        self.authenticate()
        self.client.post('/playlists', playlist={'title': playlist_title, 'sharing': 'public'})

    def get_playlist(self, playlist_title):
        playlists = self.client.get('/me/playlists')
        for playlist in playlists:
            if playlist_title == playlist.title:
                return playlist.uri

    def add_track_to_playlist(self, track, client, playlist_title):

        playlist_uri = self.get_playlist(playlist_title)
        tracks = map(lambda id: dict(id=id), [track])
        print playlist_uri
        client.put(playlist_uri, playlist={
            'tracks': tracks
        })

    def upload(self, audio_file, playlist_title):
        self.authenticate()
        track = self.client.post('/tracks', track={'title': audio_file.name, 'asset_data': open(audio_file.path, 'rb'),
                                                   'sharing': 'public'})
        self.add_track_to_playlist(track.id, self.client, playlist_title)

        return track.id
