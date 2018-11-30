from PIL import Image
from django.core.files.storage import FileSystemStorage
import mimetypes
import uuid
import os
import re
from django.conf import settings
import json


class Upload_helper:

    def __init__(self, request, folder_name):
        self.request = request
        self.folder_name = folder_name

    def upload_multi_image(self, config):
        file_post = json.loads(self.request.POST['fileuploader-list-'+config['input_name']])
        file_file = self.request.FILES.getlist(config['input_name']+'[]')
        print(file_post)
        print(file_file)

        data = []
        if self.request.method == 'POST' and file_post:
            #遍歷
            idx = 0
            for myfile in file_file:
                index = file_post[idx]['index']

                uid = uuid.uuid1().hex
                ori_name = myfile.name
                new_name = uid + os.path.splitext(str(myfile))[1]
                #thumbnail_name = 's_' + uid + os.path.splitext(str(myfile))[1]
                file_path = settings.MEDIA_ROOT + '/' + self.folder_name + '/' + new_name
                file_url = settings.MEDIA_URL + self.folder_name + '/' + new_name
                #thumbnail_path = settings.MEDIA_ROOT + '/' + self.folder_name + '/' + thumbnail_name
                #thumbnail_url = settings.MEDIA_URL + self.folder_name + '/' + thumbnail_name

                #儲存檔案
                image = Image.open(myfile)
                # 檢查圖片exif中的Orientation
                if hasattr(image, '_getexif'):
                    orientation = 0x0112
                    exif = image._getexif()
                    if exif is not None and orientation in exif.keys():
                        orientation = exif[orientation]
                        rotations = {
                            3: Image.ROTATE_180,
                            6: Image.ROTATE_270,
                            8: Image.ROTATE_90
                        }
                        if orientation in rotations.keys():
                            image = image.transpose(rotations[orientation])

                if 'editor' in file_post[idx]:
                    image = self.__image_editor(image, file_post[idx]['editor'])

                image.save(file_path)
                size = os.stat(file_path).st_size

                #產縮圖
                # image = Image.open(myfile)
                # image.thumbnail((128, 128), Image.ANTIALIAS)
                # image.save(thumbnail_path)

                data.append({
                    'file_url': file_url,
                    'ori_name': ori_name,
                    #'thumbnail_url': thumbnail_url,
                    'name': re.sub(r'^.*/', '', file_url),
                    'type': mimetypes.guess_type(file_url)[0] or 'image/png',
                    'size': size,
                    'index': index,
                })
                idx += 1
            return data

    def ajax_upload_imgs(self, config):
        isAfterEditing = False
        #fileuploader_replace = False

        # if after editing
        if self.request.POST.__contains__('_namee') and self.request.POST.__contains__('_editorr'):
            #fileuploader_replace = True
            isAfterEditing = True
            _file = settings.MEDIA_URL + self.request.POST['_namee']
            _editor = self.request.POST['_editorr']


        if self.request.method == 'POST' and self.request.FILES:
            if isAfterEditing:
                post_data = {
                    '_file': _file,
                    '_editor': _editor,
                    'fileuploader': 1
                }
                self.crop_image(post_data)
            else:
                myfile = self.request.FILES[config['input_name']+'[]']
                uid = uuid.uuid1().hex
                ori_name = myfile.name
                new_name = uid + os.path.splitext(str(myfile))[1]
                thumbnail_name = 's_' + uid + os.path.splitext(str(myfile))[1]
                file_path = settings.MEDIA_ROOT + '/' + self.folder_name + '/' + new_name
                file_url = settings.MEDIA_URL + self.folder_name + '/' + new_name
                #thumbnail_path = settings.MEDIA_ROOT + '/' + self.folder_name + '/' + thumbnail_name
                #thumbnail_url = settings.MEDIA_URL + self.folder_name + '/' + thumbnail_name
                extension = (ori_name.split('.')[-1]).lower()

                #儲存檔案
                image = Image.open(myfile)
                # fs = FileSystemStorage()
                # filename = fs.save(self.folder_name + '/' + new_name, myfile)
                # file_url = fs.url(filename)
                # size = fs.size(filename)
                # 檢查圖片exif中的Orientation
                if hasattr(image, '_getexif'):
                    orientation = 0x0112
                    exif = image._getexif()
                    if exif is not None and orientation in exif.keys():
                        orientation = exif[orientation]
                        rotations = {
                            3: Image.ROTATE_180,
                            6: Image.ROTATE_270,
                            8: Image.ROTATE_90
                        }
                        if orientation in rotations.keys():
                            image = image.transpose(rotations[orientation])
                image.save(file_path)
                size = os.stat(file_path).st_size

                #產縮圖
                # image = Image.open(file_path)
                # image.thumbnail((128, 128), Image.ANTIALIAS)
                # image.save(thumbnail_path)

            import datetime
            import time
            from email import utils
            nowdt = datetime.datetime.now()
            nowtuple = nowdt.timetuple()
            nowtimestamp = time.mktime(nowtuple)
            date = utils.formatdate(nowtimestamp)

            data = {
                #'thumbnail_url': thumbnail_url,
                'hasWarnings': False,
                'isSuccess': True,
                'warnings': [],
                'files':[{
                    'date': date,
                    'editor': True,
                    'extension': extension,
                    'file': file_url,
                    'name': re.sub(r'^.*/', '', file_url),
                    'old_name': ori_name,
                    'old_title': os.path.splitext(str(ori_name))[0],
                    'replaced': False,
                    'size': size,
                    'size2': self.__formatSize(size),
                    'title': os.path.splitext(str(new_name))[0],
                    'type': mimetypes.guess_type(file_url)[0] or 'image/png',
                    'uploaded': True
                 }],
            }

            return data

    def crop_image(self, post_data = None):
        check = False

        if post_data is None:
            post_data = self.request.POST
            if post_data.__contains__('fileuploader') and post_data.__contains__('_file') and post_data.__contains__(
                '_editor'):
                check = True

        elif all (k in post_data for k in ("fileuploader", "_file", "_editor")):
            check = True

        if check == True:
            file = post_data['_file']
            file_name = re.sub(r'^.*/', '', file)
            file_path = settings.MEDIA_ROOT + '/' + self.folder_name + '/' + file_name

            editor = json.loads(post_data['_editor'])
            #print(editor)

            image = Image.open(file_path)
            image = self.__image_editor(image, editor)

            image.save(file_path)

    def __formatSize(self, bytes):
        if bytes >= 1073741824:
            bytes = '{:,.2f}'.format(bytes / 1073741824) + ' GB'
        elif bytes >= 1048576:
            bytes = '{:,.2f}'.format(bytes / 1048576) + ' MB'
        elif bytes > 0:
            bytes = '{:,.2f}'.format(bytes / 1024) + ' KB'
        else:
            bytes = '0 bytes'

        return bytes

    def __image_editor(self, image, editor):
        rotation = editor['rotation'] if 'rotation' in editor else None
        crop = editor['crop'] if 'crop' in editor else None

        hasRotation = rotation
        hasCrop = isinstance(crop, dict) or crop == True

        if not hasRotation and not hasCrop:
            return

        if hasRotation:
            if hasRotation == 90:
                rotation = Image.ROTATE_270
            elif hasRotation == 180:
                rotation = Image.ROTATE_180
            elif hasRotation == 270:
                rotation = Image.ROTATE_90

            image = image.transpose(rotation)

        if hasCrop:
            # 坐標：圖片左上為(0.0), 右下為(max_x, max_y)
            # box(左上x, 左上y, 右下x ,右下y)
            box = (crop['left'], crop['top'], crop['left'] + crop['width'], crop['top'] + crop['height'])
            image = image.crop(box)

        return image