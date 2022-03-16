import shutil
import os

def saveTempFile(file):
    """ save the file to the temp images folder """

    with open(file.filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
        shutil.move(file.filename, 'temp/images/'+file.filename)

    # return the filename for identification purposes
    return file.filename

def deleteTempFile(file):
    """ delete the file from the temp images folder """
    os.remove('temp/images/'+file)
