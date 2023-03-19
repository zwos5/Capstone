import os, time
from urllib import parse
from cgi import parse_header
from PyQt5 import QtCore

home_directory = os.path.expanduser("~")
download_directory = home_directory + "/Downloads/"
doc_directory = home_directory + "/Documents/"
dirconfig = QtCore.QStandardPaths.writableLocation(13) + "/Zeta-Browser/"
dir_icons = dirconfig + 'iconDB/'
pic_dir = dirconfig + 'thumbnails/'
program_dir = os.path.dirname(os.path.abspath(__file__)) + '/'


file_exts = {
'application/pdf':  '.pdf',
'audio/mpeg':       '.mp3',
'video/mpeg':       '.mp4',
'video/mp4':        '.mp4',
'image/jpeg':       '.jpg',
'image/png':        '.png',
'text/html':        '.html',
}

def file_validate(text, mimetype=None):
    if text == '':
        text = time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        chars = [ '/', '\\', '|', '*', '"', '`', '<', '>', '^', '?', '$', '=']
        for char in  chars:
            text = text.replace(char, ' ')
        while '  ' in text:
            text = text.replace('  ', ' ')
    text = text[:255] 
    text = os.path.splitext(text)[0][:100] + os.path.splitext(text)[1] 
    if mimetype and (mimetype in file_exts):
        text = os.path.splitext(text)[0] + file_exts[mimetype]
    return text

def wait(millisec):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(millisec, loop.quit)
    loop.exec_()

def file_rename(filename):
    name, ext = os.path.splitext(filename)
    i = 0
    while 1:
        if not os.path.exists(filename) : return filename
        i+=1
        filename = name + str(i) + ext

def file_name_header(header):
    value, params = parse_header(header)
    if 'filename*' in params:
        filename = params['filename*']
        if filename.startswith("UTF-8''"):
            filename = parse.unquote(filename[7:])
    elif 'filename' in params:
        filename = params['filename']
    else:
        filename = ''
    return filename

# get filename from url string
def file_name_url(addr):
    Url = QtCore.QUrl.fromUserInput(addr)
    Url.setFragment(None)
    url = Url.toString(QtCore.QUrl.RemoveQuery)
    return QtCore.QFileInfo(parse.unquote_plus(url)).fileName()

# Converting a QByteArray to python str object
def str_(byte_array):
    return bytes(byte_array).decode('utf-8')

# Argument parsing
def hasArg(argname, arglist):
    for arg in arglist:
        if arg==argname:
            return True
    return False