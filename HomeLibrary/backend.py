from operations import *


class MenuSearchFlag:
    def __init__(self, window):
        self.window = window
        self.search_flag = False

    def change_search_flag(self):
        if self.search_flag:
            self.search_flag = False

            self.window.tree.clear_file_list()
            self.window.tree.create_file_list(self.window.tree.main_folder)

            self.window.menu.menu_buttons()
            self.window.folder_row.hide_search_words_row()
            self.window.folder_row.view_folder_row()
            self.window.file_row.hide_found_files_row()
            self.window.file_row.view_file_row()
            self.window.view.set_file_row()
            self.window.reader_box.clear_text_box()
            self.window.folder_row.folder_row.focus_set()
            self.window.folder_buttons.destroy_word_buttons()
            self.window.folder_buttons.folder_buttons()
        else:
            self.search_flag = True

            # Если было выделено больше одной папки, создаём массив файлов
            # только по выделенным папкам
            if self.window.tree.current_folder == self.window.tree.main_folder and \
                    len(self.window.folder_row.folder_row.selection()) > 1:
                folder_index_array = self.window.folder_row.folder_row.selection()
                folder_array = list()
                for folder_index in folder_index_array:
                    folder_array.append('data\\' +
                                        self.window.folder_row.folder_row.item(
                                            folder_index)['values'][0])
                self.window.tree.clear_file_list()
                for folder in folder_array:
                    self.window.tree.add_folder_in_file_list(folder)
            # Если было выделено не больше одной папки, создаём массив файлов
            # по всем папкам
            else:
                self.window.tree.clear_file_list()
                self.window.tree.create_file_list(self.window.tree.main_folder)

            self.create_search_settings_main_window()
            if self.window.folder_row.search_words_row.get_children():
                child_id = self.window.folder_row.search_words_row.get_children()[0]
                self.window.folder_row.search_words_row.focus_set()
                self.window.folder_row.search_words_row.focus(child_id)
                self.window.folder_row.search_words_row.selection_set(child_id)
                self.window.view.view_selected_objects_left_search()
            self.window.folder_buttons.destroy_folder_buttons()
            self.window.folder_buttons.word_buttons()

    def create_search_settings_main_window(self):
        self.window.menu.menu_buttons()
        self.window.folder_row.hide_folder_row()
        self.window.folder_row.view_search_words_row()
        self.window.folder_row.insert_search_row()
        self.window.file_row.clear_file_row()
        self.window.file_row.hide_file_row()
        self.window.file_row.view_found_files_row()
        self.window.reader_box.clear_text_box()

class ViewOperations:
    def __init__(self, window):
        self.window = window

    def show_selected_objects(self, event):
        self.view_selected_objects()

    def view_selected_objects(self):
        if len(str(self.window.root.focus_get())) == 35 and int(str(self.window.root.focus_get())[24]) == 3:
            self.view_selected_objects_left_catalog()

        elif len(str(self.window.root.focus_get())) == 35 and int(str(self.window.root.focus_get())[24]) == 4:
            self.view_selected_objects_right_catalog()

        elif len(str(self.window.root.focus_get())) == 36 and int(str(self.window.root.focus_get())[24]) == 3:
            self.view_selected_objects_left_search()

        elif len(str(self.window.root.focus_get())) == 36 and int(str(self.window.root.focus_get())[24]) == 4:
            self.view_selected_objects_right_search()

    def view_selected_objects_left_catalog(self):
        if len(self.window.folder_row.folder_row.selection()) == 1:
            object_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
            if object_dict:
                object_address = self.window.tree.current_folder + "\\" + object_dict['folder']
                if os.path.isdir(object_address):
                    self.window.reader_box.clear_text_box()
                    self.set_file_row()
                elif os.path.isfile(object_address):
                    self.window.file_row.clear_file_row()
                    self.show_file()
                else:
                    self.window.file_row.clear_file_row()
                    self.window.reader_box.clear_text_box()
        else:
            self.window.file_row.clear_file_row()
            self.window.reader_box.clear_text_box()

    def view_selected_objects_right_catalog(self):
        if len(self.window.file_row.file_row.selection()) == 1 and \
                len(self.window.folder_row.folder_row.selection()) == 1:
            object_dict = self.window.file_row.file_row.set(self.window.file_row.file_row.selection())
            if object_dict:
                middle_folder = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
                object_address = self.window.tree.current_folder + "\\" \
                                 + middle_folder['folder'] + "\\" + object_dict['file']
                if os.path.isfile(object_address):
                    self.show_file()
                else:
                    self.window.reader_box.clear_text_box()
        else:
            self.window.reader_box.clear_text_box()

    def view_selected_objects_left_search(self):
        if self.window.folder_row.search_words_row.selection():
            key_word = self.window.folder_row.search_words_row.set(
                self.window.folder_row.search_words_row.selection())['word']
            self.window.reader_box.clear_text_box()
            self.window.search.search_files(key_word)

    def set_file_row(self):
        if len(self.window.folder_row.folder_row.selection()) == 1:
            folder_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
            address = self.window.tree.current_folder + "\\" + folder_dict['folder']
            if os.path.isdir(address):
                files_array = self.window.tree.folder_dict[address][2]
                self.window.file_row.insert_values_in_file_frame(files_array)

    def show_file(self):
        # Если файл в левой колонке
        if self.window.file_row.file_row.set(self.window.file_row.file_row.selection()):
            file_dict = self.window.file_row.file_row.set(self.window.file_row.file_row.selection())
            folder_name = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())['folder']
            parent_folder_address = self.window.tree.current_folder
            file_address = parent_folder_address + "\\" + folder_name + "\\" + file_dict['file']
            file = open(file_address, encoding='utf-8')
            self.window.reader_box.insert_text(file.read())
            file.close()
            self.window.operations.displayed_file_address = file_address
        # Если файл в правой колонке
        else:
            file_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
            parent_folder_address = self.window.tree.current_folder
            file_address = parent_folder_address + "\\" + file_dict['folder']
            file = open(file_address, encoding='utf-8')
            self.window.reader_box.insert_text(file.read())
            file.close()
            self.window.operations.displayed_file_address = file_address

    def view_selected_objects_right_search(self):
        # Определяем адрес выделенного элемента
        row_id = self.window.file_row.found_files_row.focus()
        if row_id in self.window.file_row.children_dict:
            file_address = self.window.file_row.children_dict[row_id]

            # Определяем выделенное ключевое слово
            key_word = self.window.folder_row.search_words_row.set(
                self.window.folder_row.search_words_row.selection())['word']
            if not(key_word[0].isalnum()):
                key_word = key_word[1:]

            # Открываем файл и извлекаем из него текст
            file = open(file_address, encoding='utf-8')
            file_text = file.read()
            file.close()

            # Определяем позицию ключевого слова в тексте и создаём нужные индексы
            key_word_index = file_text.find(key_word)
            key_word_end_index = key_word_index + len(key_word)
            if key_word_index == -1:
                key_word_index = 0
                key_word_end_index = 0

            # Вызываем метод, отображающий текст файла и передаём в него нужные индексы
            self.window.reader_box.insert_text_with_key_word(
                file_text, key_word_index, key_word_end_index)
            self.window.operations.displayed_file_address = file_address

    def clear_file_text_frame(self):
        self.window.reader_box.clear_text_box()

    def move_focus_right(self, event):
        if len(str(self.window.root.focus_get())) == 35:
            if int(str(self.window.root.focus_get())[24]) == 3:
                if self.window.file_row.file_row.get_children():
                    self.__child_id = self.window.file_row.file_row.get_children()[0]
                    self.window.file_row.file_row.focus_set()
                    self.window.file_row.file_row.focus(self.__child_id)
                    self.window.file_row.file_row.selection_set(self.__child_id)
                    self.view_selected_objects()
        if len(str(self.window.root.focus_get())) == 36:
            if int(str(self.window.root.focus_get())[24]) == 3:
                if self.window.file_row.found_files_row.get_children():
                    self.__child_id = self.window.file_row.found_files_row.get_children()[0]
                    self.window.file_row.found_files_row.focus_set()
                    self.window.file_row.found_files_row.focus(self.__child_id)
                    self.window.file_row.found_files_row.selection_set(self.__child_id)
                    self.view_selected_objects()

    def move_focus_left(self, event):
        # Убеждаемся в том, что фокус находится в правом поле (режим каталога)
        if len(str(self.window.root.focus_get())) == 35:
            if int(str(self.window.root.focus_get())[24]) == 4:

                # Если в левой части уже есть выделенный элемент ставим курсор на него
                if self.window.folder_row.folder_row.selection():
                    child_id = self.window.folder_row.folder_row.selection()
                # Если в левой части нет выделенных элементов,
                # ставим курсор на первый по списку
                else:
                    child_id = self.window.folder_row.folder_row.get_children()[0]
                self.window.folder_row.folder_row.focus_set()
                self.window.folder_row.folder_row.focus(child_id)
                self.window.folder_row.folder_row.selection_set(child_id)

                # Удаляем текст файла, который был выделен из поля для просмотра файла
                self.clear_file_text_frame()
                self.set_file_row()

        # Убеждаемся в том, что фокус находится в правом поле (режим поиска)
        if len(str(self.window.root.focus_get())) == 36:
            if int(str(self.window.root.focus_get())[24]) == 4:

                # Если в левой части уже есть выделенный элемент ставим курсор на него
                if self.window.folder_row.search_words_row.selection():
                    child_id = self.window.folder_row.search_words_row.selection()
                # Если в левой части нет выделенных элементов,
                # ставим курсор на первый по списку
                else:
                    child_id = self.window.folder_row.search_words_row.get_children()[0]
                self.window.folder_row.search_words_row.focus_set()
                self.window.folder_row.search_words_row.focus(child_id)
                self.window.folder_row.search_words_row.selection_set(child_id)
                self.clear_file_text_frame()

                # Удаляем текст файла, который был выделен из поля для просмотра файла
                self.window.file_row.clear_found_files_row()

                # Узнаём новое выделенное ключевое слово и создаём для него список файлов
                key_word = self.window.folder_row.search_words_row.set(child_id)['word']
                self.window.search.search_files(key_word)

    def go_to_next_folder(self, event):
        if len(str(self.window.root.focus_get())) == 35:
            # Если активно левое поле
            if int(str(self.window.root.focus_get())[24]) == 3:
                object_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
                if object_dict:
                    object_address = self.window.tree.current_folder + "\\" + object_dict['folder']
                    # Если выделена папка
                    if os.path.isdir(object_address):
                        if self.window.tree.folder_dict[object_address][1]:
                            self.window.tree.current_folder = object_address
                            self.window.address.set_address_label_text()
                            self.window.folder_row.insert_values_in_folder_frame()
                            self.set_file_row()

            # Если активно правое поле
            elif int(str(self.window.root.focus_get())[24]) == 4:
                object_dict = self.window.file_row.file_row.set(self.window.file_row.file_row.selection())
                if object_dict:
                    middle_folder = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
                    object_address = self.window.tree.current_folder + "\\" + \
                                     middle_folder['folder'] + "\\" + object_dict['file']
                    # Если выделена папка
                    if os.path.isdir(object_address):
                        if self.window.tree.folder_dict[object_address][1]:
                            self.window.tree.current_folder = object_address
                            self.window.address.set_address_label_text()
                            self.window.folder_row.insert_values_in_folder_frame()
                            self.set_file_row()

    def go_to_prev_folder_event(self, event):
        if int(str(self.window.root.focus_get())[24]) == 3:
            self.go_to_prev_folder()

    def go_to_prev_folder(self):
        if self.window.mode.search_flag == False:
            now_address = self.window.tree.current_folder
            if now_address != 'data':
                index = now_address.rfind('\\')
                next_address = now_address[0: index]
                self.window.tree.current_folder = next_address
                self.window.address.set_address_label_text()
                self.window.folder_row.insert_values_in_folder_frame()
                self.set_file_row()

    def get_name_from_address(self, address):
        index = address.rfind('\\')
        name = address[index:]
        return name
