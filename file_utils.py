from os import path, listdir, mkdir, rename
# from pprint import pprint


class FileManager:
    def __init__(self):
        self.output_file_name = 'name.txt'
        self.dir_path = '~/Documents'
        self.OLDS_DIR_NAME = 'old'

    def current_drawing(self, output_file_name, dir_path):
        cur_drawing = []

        if output_file_name == '':
            return cur_drawing

        for file_name in listdir(dir_path):
            if file_name == output_file_name:
                cur_drawing = True
                break

        return cur_drawing

    def move_file(self, file_name, old_dir, new_dir):
        # determine appropriate file name
        new_file_name = file_name
        count = 1
        name, extension = path.splitext(file_name)

        while path.isfile(path.join(new_dir, new_file_name)):
            count += 1
            new_file_name = name + ' (' + str(count) + ')' + extension

        # move the file
        old_file_path = path.join(old_dir, file_name)
        new_file_path = path.join(new_dir, new_file_name)
        rename(old_file_path, new_file_path)

    def prepare_dir(self, output_file_name, dir_path, olds_dir_name):
        # store any existing file names with same drawing number
        cur_drawing = self.current_drawing(output_file_name, dir_path)

        if cur_drawing:
            # if olds directory doesn't exist, create it
            olds_dir_path = dir_path + '\\' + olds_dir_name
            if not path.isdir(olds_dir_path):
                mkdir(olds_dir_path)

            old_drawings_path = (olds_dir_path + '\\' +
                                 output_file_name.split('.', 1)[0])
            if not path.isdir(old_drawings_path):
                mkdir(old_drawings_path)

            # move existing drawing to olds dir without overwriting
            self.move_file(output_file_name, dir_path, old_drawings_path)

            files_were_moved = True
        else:
            files_were_moved = False

        return files_were_moved
