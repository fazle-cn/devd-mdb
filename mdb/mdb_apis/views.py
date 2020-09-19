from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User, File, Folder, FolderJournalNode, FileJournalNode

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
            leaf_journal_node = FolderJournalNode(file_name=file_name, operation='CREATE')
            if str(parent_folder.leaf_journal_node_id) == "_":
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                parent_folder.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            else:
                previous_leaf_journal_node = FolderJournalNode.nodes.get(jid=parent_folder.leaf_journal_node_id)
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                previous_leaf_journal_node.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.disconnect(previous_leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            file = File(file_name=file_name, created_by=parent_folder.created_by)
            file.save()
            parent_folder.contains_file.connect(file)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding file'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "File was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def removeFile(request):
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
            leaf_journal_node = FolderJournalNode(file_name=file_name, operation='REMOVE')
            if str(parent_folder.leaf_journal_node_id) == "_":
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                parent_folder.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            else:
                previous_leaf_journal_node = FolderJournalNode.nodes.get(jid=parent_folder.leaf_journal_node_id)
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                previous_leaf_journal_node.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.disconnect(previous_leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            file = File.nodes.get(file_name=file_name)
            parent_folder.contains_file.disconnect(file)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding file'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "File was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def renameFile(request):
    print(request.body)
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            #assuming unique folder/file names as of now
            relative_path = body['relative_path']
            new_name = body['new_name']
            file_name = relative_path.split('/')[-1]
            parent_folder_name = relative_path.split('/')[-2]
            parent_folder = Folder.nodes.get(folder_name=parent_folder_name)
            leaf_journal_node = FolderJournalNode(file_name=file_name, operation='RENAME', new_name=new_name)
            if str(parent_folder.leaf_journal_node_id) == "_":
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                parent_folder.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            else:
                previous_leaf_journal_node = FolderJournalNode.nodes.get(jid=parent_folder.leaf_journal_node_id)
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                previous_leaf_journal_node.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.disconnect(previous_leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            file = File.nodes.get(file_name=file_name)
            file.file_name = new_name
            file.save()
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding file'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "File was added successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def moveFile(request):
    print(request.body)
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            #assuming unique folder/file names as of now
            relative_path = body['relative_path']
            new_relative_path = body['new_relative_path']
            file_name = relative_path.split('/')[-1]
            parent_folder_name = relative_path.split('/')[-2]
            new_parent_folder_name = new_relative_path.split('/')[-2]
            parent_folder = Folder.nodes.get(folder_name=parent_folder_name)
            new_parent_folder = Folder.nodes.get(folder_name=new_parent_folder_name)
            leaf_journal_node = FolderJournalNode(file_name=file_name, operation='REMOVE')
            if str(parent_folder.leaf_journal_node_id) == "_":
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                parent_folder.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)
            else:
                previous_leaf_journal_node = FolderJournalNode.nodes.get(jid=parent_folder.leaf_journal_node_id)
                parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                parent_folder.save()
                previous_leaf_journal_node.journal_node.connect(leaf_journal_node)
                parent_folder.leaf_journal_node.disconnect(previous_leaf_journal_node)
                parent_folder.leaf_journal_node.connect(leaf_journal_node)

            file = File.nodes.get(file_name=file_name)
            parent_folder.contains_file.disconnect(file)

            leaf_journal_node = FolderJournalNode(file_name=file_name, operation='CREATE')
            if str(new_parent_folder.leaf_journal_node_id) == "_":
                new_parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                new_parent_folder.save()
                new_parent_folder.journal_node.connect(leaf_journal_node)
                new_parent_folder.leaf_journal_node.connect(leaf_journal_node)
            else:
                previous_leaf_journal_node = FolderJournalNode.nodes.get(jid=new_parent_folder.leaf_journal_node_id)
                new_parent_folder.leaf_journal_node_id = leaf_journal_node.jid
                leaf_journal_node.save()
                new_parent_folder.save()
                previous_leaf_journal_node.journal_node.connect(leaf_journal_node)
                new_parent_folder.leaf_journal_node.disconnect(previous_leaf_journal_node)
                new_parent_folder.leaf_journal_node.connect(leaf_journal_node)

            new_parent_folder.contains_file.connect(file)
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
def removeFolder(request):
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
            folder = Folder.nodes.get(folder_name=folder_name)
            print(folder)
            parent_folder.contains_folder.disconnect(folder)
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding folder'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "Folder was removed successfully"}), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def renameFolder(request):
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            #assuming unique folder/file names as of now
            relative_path = body['relative_path']
            new_name = body['new_name']
            folder_name = relative_path.split('/')[-1]
            folder = Folder.nodes.get(folder_name=folder_name)
            folder.folder_name = new_name
            folder.save()
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while adding folder'}),  content_type='application/json')
        return HttpResponse(json.dumps({"Message": "Folder was added successfully"}), content_type='application/json')



@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def pollFolder(request):
    if request.method == "OPTIONS":
        return HttpResponse(json.dumps({"Default": "Options"}), content_type='application/json')
    else:
        body = json.loads(request.body.decode('utf-8'))
        try:
            try:
                current_journal_node = FolderJournalNode.nodes.get(jid=body['current_node_id'])
            except:
                current_journal_node = Folder.nodes.get(folder_id=body['current_node_id'])
            next_nodes_list = []
            while len(current_journal_node.journal_node) > 0:
                next_node = current_journal_node.journal_node[0]
                next_nodes_list.append(next_node.__properties__)
                current_journal_node = next_node
        except:
            return HttpResponseBadRequest(json.dumps({'Message': 'Error Occured while assigning the mentor'}), content_type='application/json')
        return HttpResponse(json.dumps(next_nodes_list), content_type='application/json')
