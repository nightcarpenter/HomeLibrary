import os as os

class FolderTree:
    def __init__(self):
        self.main_folder = 'data'
        self.folder_dict = dict()
        self.file_list = list()
        self.current_folder = self.main_folder
        self.get_folder_dict(self.current_folder)

    def get_folder_dict(self, object_address, parent_folder_address = ""):
        self.folder_dict[object_address] = [parent_folder_address, list(), list()]
        for next_level_object in os.listdir(object_address):
            next_level_object_address = object_address + "\\" + next_level_object
            next_level_object_address = self.remove_space(next_level_object_address)

            if os.path.isdir(next_level_object_address):
                self.folder_dict[object_address][1].append(next_level_object_address)
                self.get_folder_dict(next_level_object_address, object_address)
            elif next_level_object_address[-4:] == ".txt":
                self.folder_dict[object_address][2].append(next_level_object_address)
                self.file_list.append(next_level_object_address)

    def clear_file_list(self):
        self.file_list = list()

    def add_folder_in_file_list(self, folder_address):
        for next_level_object_address in self.folder_dict[folder_address][2]:
            self.file_list.append(next_level_object_address)
        for next_level_object_address in self.folder_dict[folder_address][1]:
            self.add_folder_in_file_list(next_level_object_address)

    def create_file_list(self, object_address, parent_folder_address = ""):
        for next_level_object in os.listdir(object_address):
            next_level_object_address = object_address + "\\" + next_level_object

            if os.path.isdir(next_level_object_address):
                self.create_file_list(next_level_object_address, object_address)
            elif next_level_object_address[-4:] == ".txt":
                self.file_list.append(next_level_object_address)

    def remove_space(self, object_address):
        if ' ' in object_address:
            os.rename(object_address, object_address.replace(' ', '_'))
            object_address = object_address.replace(' ', '_')
        return object_address


class SearchWordsList():
    def __init__(self):
        file = open('KeyList.txt', encoding='utf-8')
        self.search_words_list = file.readlines()
        file.close()

        for i in range(len(self.search_words_list)):
            self.search_words_list[i] = self.search_words_list[i].strip()


if __name__ == "__main__":
    d = FolderTree()
    print(d.file_list)