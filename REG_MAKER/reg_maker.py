from xml.etree.ElementTree import tostring
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

debug = False

if debug:

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)

    #   ENTRO EN LA CARPETA Y VEO QUE HAY
    # View all folders and file in your Google Drive
    fileList = drive.ListFile({'corpora':'allDrives','q': "'%s' in parents and trashed=false"%("1s2OxNICWhZnaYGOjCqDiOQpH-wZ_SBAt"),'includeItemsFromAllDrives':True,'supportsAllDrives':True}).GetList()
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))

    input("Press Enter to continue...")

    #   CREO UN TXT
    file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "1s2OxNICWhZnaYGOjCqDiOQpH-wZ_SBAt"}]})
    file1.SetContentFile("test_local_file.txt")
    file1.Upload() # Upload the file.
    print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))   

    input("Press Enter to continue...")

    fileID = "1s2OxNICWhZnaYGOjCqDiOQpH-wZ_SBAt"
    #   ENTRO A LA CARPETA DE NUEVO, ENLISTO CONTENIDO
    #for archivos in file:
    #    print('Title: %s, ID: %s' % (archivos['title'], archivos['id']))
    #myFileList = drive.ListFile({'corpora': 'drive','supportsAllDrives': True,'includeItemsFromAllDrives': True,'driveId': fileID}).GetList()
    myFileList = drive.ListFile({
    'q': "'%s' in parents and trashed=false" % (fileID),
    'supportsAllDrives' : True,
    'includeItemsFromAllDrives': True
    }).GetList()

    input("Press Enter to continue...")

    var = 0

    #   DESCARGO LOS ARCHIVOS!!!
    for file in myFileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        my_file = drive.CreateFile({'id': file['id']})
        my_file.GetContentFile('file %s.txt' % (str(var)))
        var += 1

    input("Press Enter to continue...")

    #   EDITO LOS ARCHIVOS!!!

    myFileList = drive.ListFile({
    'q': "'%s' in parents and trashed=false" % (fileID),
    'supportsAllDrives' : True,
    'includeItemsFromAllDrives': True
    }).GetList()

    for file in myFileList:
        file.SetContentString("a la grande NO le puse cuca")
        file.Upload()

    print("done")