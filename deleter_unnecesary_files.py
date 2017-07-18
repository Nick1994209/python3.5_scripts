import os


class DeleteUnnecessaryFiles:
    def __init__(self, directory, need_delete_files_with_extensions=(),
                 need_leave_files_with_path_ends=()):
        self.directory = directory
        self.need_delete_files_with_extensions = need_delete_files_with_extensions
        self.need_leave_files_with_path_ends = need_leave_files_with_path_ends

    def delete(self, from_directory_path=None):
        from_directory_path = from_directory_path or self.directory

        for name in os.listdir(from_directory_path):
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                self.delete(path)

            if not self.is_file_with_delete_extension(path):
                continue
            if self.is_need_leave_file(path):
                continue
            print(path)
            # os.remove(path)

    def is_file_with_delete_extension(self, file_path):
        for extension in self.need_delete_files_with_extensions:
            if file_path.endswith(extension):
                return True
        return False

    def is_need_leave_file(self, file_path):
        for end_file_path in self.need_leave_files_with_path_ends:
            if file_path.endswith(end_file_path):
                return True
        return False

    @staticmethod
    def get_need_leave_files_with_ends(contains_symbols, extensions, splitter='.'):
        return [lang + splitter + ext for lang in contains_symbols for ext in extensions]


if __name__ == '__main__':
    extensions = ['vtt', 'srt']
    languages = ['ru', 'en']
    need_leave_files_with_ends = DeleteUnnecessaryFiles.get_need_leave_files_with_ends(
        languages, extensions)
    DeleteUnnecessaryFiles('youtube', extensions, need_leave_files_with_ends).delete()
