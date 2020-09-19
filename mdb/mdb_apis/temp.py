from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User, File, Folder

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def addUser(request):
    print(request.body)
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            root_folder_name = body['email']
            folder = Folder(folder_name=root_folder_name, created_by=body['email'])
            user = User(email=body['email'], root_folder_name=root_folder_name)
            user.save()
            folder.save()
            user.owns.connect(folder)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding user'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "User was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def addFile(request):
    print(request.body)
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            #assuming unique folder/file names as of now
            relative_path = body['relative_path']
            file_name = relative_path.split('/')[-1]
            parent_folder_name = relative_path.split('/')[-2]
            parent_folder = Folder.nodes.get(folder_name=parent_folder_name)
            file = File(file_name=file_name, created_by=parent_folder.created_by)
            file.save()
            parent_folder.contains_file.connect(file)

        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding file'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "File was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def addFolder(request):
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            #assuming unique folder/file names as of now
            relative_path = body['relative_path']
            folder_name = relative_path.split('/')[-1]
            parent_folder_name = relative_path.split('/')[-2]
            parent_folder = Folder.nodes.get(folder_name=parent_folder_name)
            folder = Folder(folder_name=folder_name, created_by=parent_folder.created_by)
            folder.save()
            parent_folder.contains_folder.connect(folder)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding folder'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "Folder was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def shareFolderWithUser(request):
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            user = User.nodes.get(user_id=body['user_id'])
            folder = Folder.nodes.get(folder_id=body['folder_id'])
            user.owns.connect(folder)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while assigning the mentor'}), content_type='application/json')
        return HttpResponse(json.dumps({"Message": "Mentor assigned successfully"}), content_type='application/json')



@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def moveFile(request):
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')

    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            relative_path = body['relative_path']
            new_relative_path = body['new_relative_path']

            file_name = 
