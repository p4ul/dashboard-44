#
# 
# requires https://github.com/evernote/evernote-sdk-python to be installed
# Before running this you must fill in your Evernote developer token.
#
#

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteTypes
import csv
from datetime import datetime
from evernote.api.client import EvernoteClient

# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action

auth_token = "your developer token"
csvfile = 'stats.csv'


if auth_token == "your developer token":
    print "Please fill in your developer token"
    print "To get a developer token, visit " \
        "https://sandbox.evernote.com/api/DeveloperToken.action"
    exit(1)

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action

client = EvernoteClient(token=auth_token, sandbox=False)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print "Is my Evernote API version up to date? ", str(version_ok)
print ""
if not version_ok:
    exit(1)

note_store = client.get_note_store()
cur_date = datetime.now()

with open(csvfile, 'ab') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
  

    f = NoteTypes.NoteFilter()
    noteBookCounts = note_store.findNoteCounts(f, True)
    # print noteBookCounts
    for tag_guid in noteBookCounts.tagCounts:
        tag = note_store.getTag(tag_guid)
        #print "tag", cur_date, tag_guid, tag.name, noteBookCounts.tagCounts[tag_guid]
        spamwriter.writerow([cur_date,'tag', tag_guid, tag.name, noteBookCounts.tagCounts[tag_guid] ])

    for notebook_guid in noteBookCounts.notebookCounts:
        notebook = note_store.getNotebook(notebook_guid)
        # print "  notebook ", cur_date,notebook_guid, notebook.name, noteBookCounts.notebookCounts[notebook_guid]
        spamwriter.writerow([cur_date,'notebook', notebook_guid, notebook.name, noteBookCounts.notebookCounts[notebook_guid] ])
    
    # print " trashcount ", cur_date,noteBookCounts.trashCount
    spamwriter.writerow([cur_date,'trash', '', 'trash', noteBookCounts.trashCount])

