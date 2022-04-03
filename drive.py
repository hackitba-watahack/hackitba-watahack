from xml.etree.ElementTree import tostring
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

folder_name = "watahack_folder1"
local_file_name = "test_local_file.txt"

debug = False

def init_module():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def open_folder(drive,folder_name):
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false",
    'corpora':'allDrives',
    'includeItemsFromAllDrives':True,
    'supportsAllDrives':True}).GetList()
    for file in fileList:
        if(file['title'] == folder_name):
            return file
    return 0

def open_sub_folder(drive,folder,subfolder_name):
    fileList = drive.ListFile({'q': "'%s' in parents and trashed=false"%(folder['id']),
    'corpora':'allDrives',
    'includeItemsFromAllDrives':True,
    'supportsAllDrives':True}).GetList()
    for file in fileList:
        if(file['title'] == subfolder_name):
            return file
    return 0

def create_file_from_local(drive, folder, local_file_name):
    file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder['id']}]})
    file.SetContentFile(local_file_name)
    file.Upload()


def get_list_from_folder(drive, folder):
    return drive.ListFile({
  'q': "'%s' in parents and trashed=false" % folder['id'],
  'supportsAllDrives' : True,
  'includeItemsFromAllDrives': True
}).GetList()

def get_file_from_folder(drive, folder, file_name):
    list = get_list_from_folder(drive,folder)
    for file in list:
        if(file['title'] == file_name):
            return file
    return 0

def download_file(drive, file, local_name):
    local_file = drive.CreateFile({'id':file['id']})
    local_file.GetContentFile(local_name)

def change_content_from_string(file, string):
    file.SetContentString(string)
    file.Upload()

def change_content_from_file(file, local_name):
    file.SetContentFile(local_name)
    file.Upload()

if debug:

    drive = init_module()
    folder = open_folder(drive, folder_name)
    if not folder is 0:

        #create_file_from_local(drive, folder, local_file_name)

        #list = get_list_from_folder(drive, folder)
        #var = 0
        #for file in list:
        #    download_file(drive,file,'local_file_%s.txt'%(var))
        #    var+=1

        list = get_list_from_folder(drive, folder)
        var = 0
        for file in list:
            change_content_from_string(file,'Esta es la numero %s'%(var))
            var+=1
