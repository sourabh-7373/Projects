from django.contrib.auth.models import Permission, User
from django.db import models
from django.urls import reverse


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    album_logo = models.CharField(max_length=1000)

    # Returns album title along with artist for particular album.
    def __str__(self):
        return self.album_title + ' - ' + self.artist

    def get_absolute_url(self):
        return reverse('music:album_list')


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')

    # Returns song title from Song model.
    def __str__(self):
        return self.song_title


    def get_absolute_url(self):
        return reverse('music:detail', args=[str(self.id)])
