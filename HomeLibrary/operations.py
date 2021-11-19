import tkinter.messagebox as tk_message_box
from data import *
import shutil as shutil

class Operations:
    def __init__(self, window):
        self.window = window
        self.displayed_file_address = ''

    def save_file(self):
        new_text = self.window.reader_box.get_value()
        if self.displayed_file_address and new_text:
            if new_text[0] != '\n':
                file = open(self.displayed_file_address, 'w', encoding='utf-8')
                file.write(new_text)
                file.close()
                self.window.reader_box.insert_text(new_text.strip())
            else:
                tk_message_box.showerror("Ошибка", "Нельзя сохранять пустой файл")

    def add_new_file(self, new_file_name):
        length = len(new_file_name)
        if new_file_name[length - 4:] != '.txt':
            full_file_address = new_file_name + '.txt'
        else:
            full_file_address = new_file_name
        file = open(full_file_address, 'w')
        file.close()

        index = full_file_address.rfind('\\')
        file_address = full_file_address[0: index]

        index = full_file_address.find('\\')
        main_folder = full_file_address[0: index]

        self.window.tree.get_folder_dict(main_folder)
        self.window.tree.current_folder = file_address
        self.window.modal_window.close_modal_window()
        self.window.folder_row.insert_search_row()
        self.window.view.set_file_row()

    def add_new_folder(self, new_folder_address):
        pass

    def edit_object(self, object_type, object_address, new_name, frame):
        if object_type == 'file':
            self.edit_file(object_address, new_name, frame)
        elif object_type == 'folder':
            self.edit_folder(object_address, new_name, frame)

    def edit_file(self, file_address, new_name, frame):
        index = file_address.rfind('\\')
        folder_address = file_address[0: index]
        new_address = folder_address + '\\' + new_name + '.txt'

        os.rename(file_address, new_address)
        self.window.tree.folder_dict[folder_address][2].remove(file_address)
        self.window.tree.folder_dict[folder_address][2].append(new_address)
        self.window.tree.file_list.remove(file_address)
        self.window.tree.file_list.append(new_address)
        self.window.modal_window.close_modal_window()

        if frame == 'right' and self.window.mode.search_flag:
            index = 0
            child = self.window.file_row.found_files_row.selection()[0]
            children = self.window.file_row.found_files_row.get_children()
            for i in range(len(children)):
                if children[i] == child:
                    index = i
            value_name = new_name + '.txt'
            self.window.file_row.found_files_row.insert('', index, value=value_name)
            new_children = self.window.file_row.found_files_row.get_children()
            new_child = new_children[index]
            self.window.file_row.found_files_row.delete(child)
            self.window.file_row.found_files_row.focus_set()
            self.window.file_row.found_files_row.focus(new_child)
            self.window.file_row.found_files_row.selection_set(new_child)
        elif frame == 'right' and not(self.window.mode.search_flag):
            index = 0
            child = self.window.file_row.file_row.selection()[0]
            children = self.window.file_row.file_row.get_children()
            for i in range(len(children)):
                if children[i] == child:
                    index = i
            value_name = new_name + '.txt'
            self.window.file_row.file_row.insert('', index, value=value_name)
            new_children = self.window.file_row.file_row.get_children()
            new_child = new_children[index]
            self.window.file_row.file_row.delete(child)
            self.window.file_row.file_row.focus_set()
            self.window.file_row.file_row.focus(new_child)
            self.window.file_row.file_row.selection_set(new_child)
        elif frame == 'left' and not(self.window.mode.search_flag):
            index = 0
            child = self.window.folder_row.folder_row.selection()[0]
            children = self.window.folder_row.folder_row.get_children()
            for i in range(len(children)):
                if children[i] == child:
                    index = i
            value_name = new_name + '.txt'
            self.window.folder_row.folder_row.insert('', index, value=value_name)
            new_children = self.window.folder_row.folder_row.get_children()
            new_child = new_children[index]
            self.window.folder_row.folder_row.delete(child)
            self.window.folder_row.folder_row.focus_set()
            self.window.folder_row.folder_row.focus(new_child)
            self.window.folder_row.folder_row.selection_set(new_child)

    def edit_folder(self, folder_address, new_name, frame):
        index = folder_address.rfind('\\')
        prev_level_address = folder_address[0: index]
        new_address = prev_level_address + '\\' + new_name

        os.rename(folder_address, new_address)
        index = folder_address.find('\\')
        main_folder = folder_address[0: index]
        self.window.tree.get_folder_dict(main_folder)
        self.window.modal_window.close_modal_window()

        if frame == 'right' and not(self.window.mode.search_flag):
            index = 0
            child = self.window.file_row.file_row.selection()[0]
            children = self.window.file_row.file_row.get_children()
            for i in range(len(children)):
                if children[i] == child:
                    index = i

            self.window.file_row.file_row.insert('', index, value=new_name)
            new_children = self.window.file_row.file_row.get_children()
            new_child = new_children[index]
            self.window.file_row.file_row.delete(child)
            self.window.file_row.file_row.focus_set()
            self.window.file_row.file_row.focus(new_child)
            self.window.file_row.file_row.selection_set(new_child)
        elif frame == 'left' and not(self.window.mode.search_flag):
            index = 0
            child = self.window.folder_row.folder_row.selection()[0]
            children = self.window.folder_row.folder_row.get_children()
            for i in range(len(children)):
                if children[i] == child:
                    index = i
            self.window.folder_row.folder_row.insert('', index, value=new_name)
            new_children = self.window.folder_row.folder_row.get_children()
            new_child = new_children[index]
            self.window.folder_row.folder_row.delete(child)
            self.window.folder_row.folder_row.focus_set()
            self.window.folder_row.folder_row.focus(new_child)
            self.window.folder_row.folder_row.selection_set(new_child)

    def add_new_word(self, new_word):
        self.window.swl.search_words_list.append(new_word)

        file = open('KeyList.txt', 'w', encoding='utf-8')
        for word in self.window.swl.search_words_list:
            file.write(word + '\n')
        file.close()

        self.window.modal_window.close_modal_window()
        self.window.mode.create_search_settings_main_window()

        children_array = self.window.folder_row.search_words_row.get_children()
        if children_array:
            for child_id in children_array:
                if self.window.folder_row.search_words_row.item(child_id)['values'][0].strip() == new_word:
                    self.window.folder_row.search_words_row.focus_set()
                    self.window.folder_row.search_words_row.focus(child_id)
                    self.window.folder_row.search_words_row.selection_set(child_id)
                    self.window.view.view_selected_objects_left_search()

    def delete_key_word(self):
        if self.window.folder_row.search_words_row.selection():
            child_id = self.window.folder_row.search_words_row.selection()[0]
            word = self.window.folder_row.search_words_row.item(child_id)['values'][0].strip()

            self.window.swl.search_words_list.remove(word)
            file = open('KeyList.txt', 'w', encoding='utf-8')
            for word in self.window.swl.search_words_list:
                file.write(word + '\n')
            file.close()

            self.window.mode.create_search_settings_main_window()

        else:
            tk_message_box.showerror("Ошибка", "Слово не выбрано")

    def delete_file_or_folder_left(self):
        if self.window.folder_row.folder_row.selection():
            child_id = self.window.folder_row.folder_row.selection()[0]
            object_name = self.window.folder_row.folder_row.item(child_id)['values'][0].strip()
            object_address = self.window.tree.current_folder + '\\' + object_name

            if os.path.isfile(object_address):
                self.window.tree.folder_dict[self.window.tree.current_folder][2].remove(object_address)
                self.window.tree.file_list.remove(object_address)
                os.remove(object_address)
                self.window.folder_row.folder_row.delete(child_id)
            elif os.path.isdir(object_address):
                shutil.rmtree(object_address)
                self.window.tree.get_folder_dict(self.window.tree.main_folder)
                self.window.folder_row.insert_values_in_folder_frame()
                self.window.file_row.clear_file_row()

        else:
            tk_message_box.showerror("Ошибка", "Объект не выбран")

    def delete_file_or_folder_right(self):
        if self.window.file_row.file_row.selection():
            child_id = self.window.file_row.file_row.selection()[0]
            object_name = self.window.file_row.file_row.item(child_id)['values'][0].strip()
            middle_child_id = self.window.folder_row.folder_row.selection()[0]
            middle_folder =  self.window.folder_row.folder_row.item(middle_child_id)['values'][0].strip()
            object_address = self.window.tree.current_folder + '\\' + middle_folder + '\\' + object_name

            if os.path.isfile(object_address):
                self.window.tree.folder_dict[self.window.tree.current_folder + '\\' +
                                             middle_folder][2].remove(object_address)
                self.window.tree.file_list.remove(object_address)
                os.remove(object_address)
                self.window.file_row.file_row.delete(child_id)
            elif os.path.isdir(object_address):
                shutil.rmtree(object_address)
                self.window.tree.get_folder_dict(self.window.tree.main_folder)
                self.window.file_row.file_row.delete(child_id)

        else:
            tk_message_box.showerror("Ошибка", "Объект не выбран")