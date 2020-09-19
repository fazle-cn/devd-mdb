from django.urls import path

from . import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'addUser', views.addUser, name='addUser'),
    url(r'addFile', views.addFile, name='addFile'),
    url(r'removeFile', views.removeFile, name='removeFile'),
    url(r'renameFile', views.renameFile, name='renameFile'),
    url(r'moveFile', views.moveFile, name='moveFile'),
    url(r'addFolder', views.addFolder, name='addFolder'),
    url(r'removeFolder', views.removeFolder, name='removeFolder'),
    url(r'renameFolder', views.renameFolder, name='renameFolder'),
    url(r'pollFolder', views.pollFolder, name='pollFolder'),
]