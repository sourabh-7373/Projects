from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Album, Song
from .forms import AlbumForm, UserForm, SongForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# *
# Index Function is used render index page that the user views.
# Is_authenticated: Is used to to authenticate the user and if he is not, then render to Login Page again.
# albums: Returns a new QuerySet containing objects that match the given lookup parameters. (With the help of filter)
# songs: Retreiving all the objects in the database.
# query: Search at index page has access to the q value in request.GET. Hence show results accordingly
#


class IndexView(LoginRequiredMixin, ListView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    template_name = 'music/album_list.html'
    context_object_name = 'albums'

    ''' get_queryset: Get the list of items for this view '''
    def get_queryset(self):
        return Album.objects.filter(user = self.request.user)




# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'music/login.html')
#     else:
#         albums = Album.objects.filter(user=request.user)
#         song_results = Song.objects.all()
#         query = request.GET.get("q")
#         if query:
#             albums = albums.filter(Q(album_title__icontains=query) | Q(artist__icontains=query)).distinct()
#             song_results = song_results.filter(Q(song_title__icontains=query)).distinct()
#             return render(request, 'music/index.html', {
#                 'albums': albums,
#                 'songs': song_results,
#             })
#         else:
#             return render(request, 'music/index.html', {'albums': albums})

# *
# Is_authenticated: Is used to to authenticate the user and if he is not, then render to Login Page again.
# album: Going to query album model in class Album and retreive all objects in the db with id as a parameter passed or else give 404 error
# After authenticated user is logged in, shows the details page to user containing albums created of that user.
#

class AlbumDetail(LoginRequiredMixin, DetailView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    template_name = 'music/detail.html'

# def detail(request, album_id):
#     if not request.user.is_authenticated:
#         return render(request, 'music/login.html')
#     else:
#         user = request.user
#         album = get_object_or_404(Album, pk=album_id)
#         return render(request, 'music/detail.html', {'album': album, 'user': user})

# *
# Is_authenticated: Is used to to authenticate the user and if he is not, then render to Login Page again.
# Form: Has a POST request or else None will go.
# is_Valid: Check the validation of the form and if not going to render to the same page with form to fill.
# form.save(): Is going to save in the db if validated and has content in it.
# album_logo: Request a logo from the form.
# file_type: Type of file like PNG etc. Split it with '.' & .lower(): Change in lowercase
# If Not in IMAGE_FILE_TYPES global list: Going to throw an error in context dictionary & will render you to same page only.
# Otherwise, album.save() is going to save in the db and render to details page with albums listed if you have uploaded any.


class AlbumCreate(LoginRequiredMixin, CreateView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    fields = ['album_title','artist','genre','album_logo']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    fields = ['album_title','artist','genre','album_logo']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(AlbumUpdate, self).form_valid(form)


# def create_album(request):
#     if not request.user.is_authenticated:
#         return render(request, 'music/login.html')
#     else:
#         form = AlbumForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             album = form.save(commit=False)
#             album.user = request.user
#             album.album_logo = request.FILES['album_logo']
#             file_type = album.album_logo.url.split('.')[-1]
#             file_type = file_type.lower()
#             if file_type not in IMAGE_FILE_TYPES:
#                 context = {
#                     'album': album,
#                     'form': form,
#                     'error_message': 'Image file must be PNG, JPG, or JPEG',
#                 }
#                 return render(request, 'music/create_album.html', context)
#             album.save()
#             return render(request, 'music/detail.html', {'album': album})
#         context = {
#             "form": form,
#         }
#         return render(request, 'music/create_album.html', context)

# *
# [delete_album] : Going to delte the album uploaded specific to the user. Takes album id (Primary Key) and parameter to make sure only album with passed album_id will be deleted.
# album : Get all the objects from the db with pk of that record.
# .delete(): Will delete the record from the db.
# albums : Returns a new QuerySet containing objects that match the given lookup parameters. (With the help of filter)
# After exceution is done, render to Index page with albums listed.
#

class AlbumDelete(LoginRequiredMixin, DeleteView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    success_url = reverse_lazy('music:album_list')

# def delete_album(request, album_id):
#     album = Album.objects.get(pk=album_id)
#     album.delete()
#     albums = Album.objects.filter(user=request.user)
#     return render(request, 'music/index.html', {'albums': albums})

# *
# [create_song]: Takes parameter as album_id specific to the album uploaded.
# form : Show the form created and has a request.POST since content will be asked to create.
# album : Going to query album model in class Album and retreive all objects in the db with id as a parameter passed or else give 404 error
# form.is_Valid(): Check the validation of the form and if not going to render to the same page with form to fill.
# form.save(): Is going to save in the db if validated and has content in it.
# album_songs = Goin to do 2 queries instead of one. First it will fetch objects of Album and then as a foreign key has access to Song for that album linked to it.
# (cleaned_data) : Used to return cleaned data dictionary of the form after validating it. When we use form.cleaned_data.get() means data if not passed in song_title will return None as default.
# s.song_title = object accesses song_title in the db and checks whether the record entered in the field matches with s or not. If yes, then error will show from context dictionary and will render you to same create_song html page.
# form.save() : Save the changes in the form in the db.
# song.album = gives you the album objects from the db & stores songs in its album only.
# song.audio_file = stores audio_file requested type like .mp3 etc
# AUDIO_FILE_TYPES global list will check whether type matches with the types passed. If yes, will save the song and render to the details page to show all the albums.
# If form is not valid, will render to create_song page.
#


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)

# *
# [delete_song function] : Deletes the song inside its album. Uses the parameters as song_id for songs id and album_id for id of that album mapped with song.
# album : Going to query album model in class Album and retreive all objects in the db with id as a parameter passed or else give 404 error
# song : Get all objects of the Song in db.
# .delete(): Deletes the song from the album and db.
# Render to details page to open album again and refreshes data.
#


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})

# *
# [favourite] : Uses the paramter song_id for marking the particular song as favourite
# song: Get all the objects of the Song from the db or else give 404 error if no record is found.
# try and except is used in case it throws error for handling it.
# is_favourite: Checks the boolean value of it. Its value by default is False.
# song.save(): Will save the is_favourite value in the db with updated record.
# Will give a JSON output as success message.
#


# *
# [favourite_album]: Uses album_id as paramter to make album as favourite.
# album: Going to query album model in class Album and retreive all objects in the db with id as a parameter passed or else give 404 error
# try and except is used in case it throws error for handling it.
# is_favourite: Checks the boolean value of it. Its value by default is False.
# album.save(): Will save the is_favourite value in the db with updated record.
# Will give a JSON output as specific message.


# *
# [login_user]: For loging in for user. Has a form with username and password as enteries.
# request.method == POST: if the requested method is POST check.
# authenticate(): Used to authenticate the enteries used as POST.
# Is user is not in the records of User class in the db then render it to same login page with error.
# Is yes, then check is_active(), if true, Login and albums will be show respective to him. Rendered to index page else login page with error message if not active.
# Reuested method is not POST, returns error and renders to same login page.
#


class LoginView(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/album_list.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})


    def get(self, request):
        return render(request, 'music/login.html')

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 albums = Album.objects.filter(user=request.user)
#                 return render(request, 'music/index.html', {'albums': albums})
#             else:
#                 return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'music/login.html', {'error_message': 'Invalid login'})
#     return render(request, 'music/login.html')

# *
# [logout_user]: Used to log out the user from the active session.
# logout(): Will take the request and log out and render to login page to start session again.
# form : Has the UserForm from forms file with enteries entered via POST request or else None by default if not entered.
#


class LogoutView(View):
	def get(self, request):
		logout(request)
		form = UserForm(request.POST or None)
		context = {
			"form": form,
		}
		return render(request, 'music/login.html', context)

# def logout_user(request):
#     logout(request)
#     form = UserForm(request.POST or None)
#     context = {
#         "form": form,
#     }
#     return render(request, 'music/login.html', context)

# *
# [register]: Used to register user if not signed up. It takes request and returns response.
# form : Has the UserForm from forms file with enteries entered via POST request or else None by default if not entered.
# form.save(): Saves the data in the form.
# form.cleaned_data(): Gives you the cleaned data.
# set_password() = Hash the password.
# user.save() : Saves the form data in the User table.
# authenticate(): Checks the UserForm entered record for the user.
# If user has record, is_active() check is performed and login him through login function and render to index page with albums uploaded by him.
# If form invalid: Register page is rendered.
#


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/album_list.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)

# *
# [songs]: Takes filter_by generic parameter to retreive all the records so far for songs of the authenticated user.
# songs_ids: Empty list to store song's id from albums mapped to it.
# album: Get all objects of Album from the db.
# song: Performs 2 queries; One for Albums mapped to it as foreign key and has
# access to its variables. Second get all objects of it from db.
# filter_by check with favourites, Show the records maked True for is_favourite from db.
# render to songs html to show user_songs and filtered content passed as parameter.
#


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'q':
                users_songs = users_songs.filter(filter_by)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
