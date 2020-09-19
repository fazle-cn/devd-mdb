from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty

# Create your models here.

class FileJournalNode(StructuredNode):
    jid = UniqueIdProperty()
    modified_on = DateTimeProperty(default=datetime.utcnow)
    modified_by = StringProperty()

class FolderJournalNode(StructuredNode):
    jid = UniqueIdProperty()
    file_name = StringProperty()
    operation = StringProperty()
    new_name = StringProperty(default='')
    journal_node = RelationshipTo('FolderJournalNode', 'next_journal_entry')

class File(StructuredNode):
    file_id = UniqueIdProperty()
    file_name = StringProperty(unique_index=True)
    created_on = DateTimeProperty(default=datetime.utcnow)
    created_by = StringProperty()

class Folder(StructuredNode):
    folder_id = UniqueIdProperty()
    folder_name = StringProperty(unique_index=True)
    created_on = DateTimeProperty(default=datetime.utcnow)
    created_by = StringProperty()
    leaf_journal_node_id = StringProperty(default='_')
    contains_file = RelationshipTo('File', 'contains')
    contains_folder = RelationshipTo('Folder', 'contains')
    journal_node = RelationshipTo('FolderJournalNode', 'next_journal_entry')
    leaf_journal_node = RelationshipTo('FolderJournalNode', 'leaf_journal_entry')


class User(StructuredNode):
    email = StringProperty(unique_index=True, required=True)
    user_id = UniqueIdProperty()
    boarded_on = DateTimeProperty(default=datetime.utcnow)
    root_folder_name = StringProperty(unique_index=True)
    owns = RelationshipTo('Folder', 'owner_of')

