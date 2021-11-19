from search import *
from modal_window import *

from  tkinter import ttk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Home Library')
        self.root.geometry('895x600+300+30')
        self.root.resizable(False, False)
        self.root.iconbitmap('img/icon.ico')

        self.tree = FolderTree()
        self.swl = SearchWordsList()

        self.mode = MenuSearchFlag(self)
        self.view = ViewOperations(self)
        self.search = Search(self)
        self.operations = Operations(self)
        self.modal_window = ModalWindow(self)

        self.place_main_frame()
        self.img = LoadImages()
        self.set_frames()

        self.root.bind("<Button-1>", self.view.show_selected_objects)
        self.root.bind("<Up>", self.view.show_selected_objects)
        self.root.bind("<Down>", self.view.show_selected_objects)
        self.root.bind("<Right>", self.view.move_focus_right)
        self.root.bind("<Left>", self.view.move_focus_left)
        self.root.bind("<Double-Button-1>", self.view.go_to_next_folder)
        self.root.bind("<Return>", self.view.go_to_next_folder)
        self.root.bind("<Escape>", self.view.go_to_prev_folder_event)

    def set_frames(self):
        self.menu = MenuFrame(self)
        self.address = AddressFrame(self)
        self.folder_row = FolderRow(self)
        self.file_row = FileRow(self)
        self.view.set_file_row()
        self.reader_box = ReaderBoxFrame(self)
        self.folder_buttons = FolderButtons(self)
        self.file_buttons = FileButtons(self)
        self.save_button = SaveButton(self)

    def run(self):
        self.root.mainloop()

    def place_main_frame(self):
        self.main_frame = tk.LabelFrame(self.root, width=895, height=600, bd=0, bg="#3C3F41")
        self.main_frame.place(x=0, y=0)


class MenuFrame:
    def __init__(self, window):
        self.window = window
        self.create_menu_frame()
        self.menu_buttons()

    def create_menu_frame(self):
        self.search_frame = tk.LabelFrame(self.window.main_frame, width=431, height=74, bd=10, bg="#6C6E6F",
                                          relief="raised")
        self.search_frame.place(x=10, y=10)

    def menu_buttons(self):
        if self.window.mode.search_flag:
            self.__catalog_text = "Каталог"
            self.__catalog_relief = "raised"
            self.__catalog_fg = "#F8F8F8"
            self.__search_text = "Режим Поиска"
            self.__search_relief = "groove"
            self.__search_fg = "#94558D"
        else:
            self.__catalog_text = "Режим Каталога"
            self.__catalog_relief = "groove"
            self.__catalog_fg = "#94558D"
            self.__search_text = "Поиск"
            self.__search_relief = "raised"
            self.__search_fg = "#F8F8F8"

        self.button_catalog = tk.Button(self.search_frame, width=17, text=self.__catalog_text, font="TimesNewRoman 12",
                                     bg="#141414", fg=self.__catalog_fg, bd=8, relief=self.__catalog_relief,
                                     command=lambda:self.window.mode.change_search_flag())
        self.button_catalog.place(x=7, y=3)

        self.button_search = tk.Button(self.search_frame, width=17, text=self.__search_text, font="TimesNewRoman 12",
                                        bg="#141414", fg=self.__search_fg, bd=8,  relief=self.__search_relief,
                                        command=lambda:self.window.mode.change_search_flag())
        self.button_search.place(x=227, y=3)


class AddressFrame:
    def __init__(self, window):
        self.window = window
        self.create_address_frame()
        self.set_address_label_text()
        self.create_address_button_back()
        self.create_address_button_copy()

    def create_address_frame(self):
        self.address_frame = tk.LabelFrame(self.window.main_frame, width=431, height=26, bd=0, bg="#3C3F41")
        self.address_frame.place(x=10, y=94)

    def create_address_button_back(self):
        self.button_back = tk.Button(self.address_frame, image=self.window.img.back,
                                           font="TimesNewRoman 8", bg="#141414", bd=3, relief="raised",
                                           width=18, height=18,
                                           command=lambda: self.window.view.go_to_prev_folder())
        self.button_back.place(x=0, y=0)

    def create_address_button_copy(self):
        self.button_copy = tk.Button(self.address_frame, image=self.window.img.copy,
                                     font="TimesNewRoman 8", bg="#141414", bd=3, relief="raised",
                                     width=18, height=18,
                                     command=lambda:self.copy_address())
        self.button_copy.place(x=406, y=0)

    def create_address_label(self):
        self.lable_address = tk.Label(self.address_frame, text=self.text, relief="ridge", font="TimesNewRoman 11",
                                       width="40", bg="#141414", fg="#BCCF62", bd="3", anchor="w")
        self.lable_address.place(x=32, y=0)

    def set_address_label_text(self):
        self.text = self.window.tree.current_folder + "\\"
        self.create_address_label()

    def copy_address(self):
        self.window.root.clipboard_clear()
        self.window.root.clipboard_append(self.text)


class FolderRow:
    def __init__(self, window):
        self.window = window
        self.create_folder_frame()
        self.create_folder_row()
        self.view_folder_row()
        self.insert_values_in_folder_frame()
        self.create_search_words_row()

    def create_folder_frame(self):
        self.folder_frame = tk.LabelFrame(self.window.main_frame, width=205, height=397, bd=5, bg="#141414",
                                          relief="sunken")
        self.folder_frame.place(x=10, y=130)

    def create_folder_row(self):
        self.folder_row = ttk.Treeview(self.folder_frame, columns=('folder'), height=18, show='headings')
        self.folder_row.column('folder', width=192, anchor='w')
        self.folder_row.heading('folder', text='Список папок и файлов')

    def insert_values_in_folder_frame(self):
        for folder in self.folder_row.get_children():
            self.folder_row.delete(folder)
        for folder_address in self.window.tree.folder_dict[self.window.tree.current_folder][1]:
            folder_name = self.window.view.get_name_from_address(folder_address)
            self.folder_row.insert('', 'end', value=folder_name)

        # Проверяем есть ли списке файлы, добавляем их после черты
        if self.window.tree.folder_dict[self.window.tree.current_folder][2]:
            self.folder_row.insert('', 'end', value='-------------------------------------')
            for file_address in self.window.tree.folder_dict[self.window.tree.current_folder][2]:
                file_name = self.window.view.get_name_from_address(file_address)
                self.folder_row.insert('', 'end', value=file_name)

        if self.folder_row.get_children():
            self.__child_id = self.folder_row.get_children()[0]
            self.folder_row.focus_set()
            self.folder_row.focus(self.__child_id)
            self.folder_row.selection_set(self.__child_id)

    def create_search_words_row(self):
        self.search_words_row = ttk.Treeview(self.folder_frame, columns=('word'), height=18, show='headings')
        self.search_words_row.column('word', width=192, anchor='w')
        self.search_words_row.heading('word', text='Список ключевых слов')

    def insert_search_row(self):
        for search_word in self.search_words_row.get_children():
            self.search_words_row.delete(search_word)
        for word in self.window.swl.search_words_list:
            self.search_words_row.insert('', 'end', value=word)

    def show_selected_files(self, event):
        self.window.file_row.show_files_row()

    def hide_folder_row(self):
        self.folder_row.place_forget()

    def view_folder_row(self):
        self.folder_row.place(x=0, y=0)

    def hide_search_words_row(self):
        self.search_words_row.place_forget()

    def view_search_words_row(self):
        self.search_words_row.place(x=0, y=0)


class FileRow:
    def __init__(self, window):
        self.window = window
        self.create_file_frame()
        self.create_file_row()
        self.create_found_files_row()
        self.view_file_row()

    def create_file_frame(self):
        self.folder_frame = tk.LabelFrame(self.window.main_frame, width=205, height=397, bd=5, bg="#141414",
                                          relief="sunken")
        self.folder_frame.place(x=236, y=130)

    def create_file_row(self):
        self.file_row = ttk.Treeview(self.folder_frame, columns=('file'), height=18, show='headings')
        self.file_row.column('file', width=192, anchor='w')
        self.file_row.heading('file', text='Содержимое папок')

    def insert_values_in_file_frame(self, file_array):
        self.clear_file_row()

        # Проверяем есть ли списке папки, добавляем их до черты
        folder_name = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
        if folder_name:
            folder_address = self.window.tree.current_folder + "\\" + folder_name['folder']
            if self.window.tree.folder_dict[folder_address][1]:
                for folder_address in self.window.tree.folder_dict[folder_address][1]:
                    folder_name = self.window.view.get_name_from_address(folder_address)
                    self.file_row.insert('', 'end', value=folder_name)
                self.file_row.insert('', 'end', value='-------------------------------------')

        for file_address in file_array:
            file_name = self.window.view.get_name_from_address(file_address)
            self.file_row.insert('', 'end', value=file_name)

    def clear_file_row(self):
        for file in self.file_row.get_children():
            self.file_row.delete(file)

    def create_found_files_row(self):
        self.found_files_row = ttk.Treeview(self.folder_frame, columns=('file'), height=18, show='headings')
        self.found_files_row.column('file', width=192, anchor='w')
        self.found_files_row.heading('file', text='Найденные файлы')

    def insert_values_in_found_files_row(self, found_file_array):
        self.clear_found_files_row()
        for file_address in found_file_array:
            file_name = self.window.view.get_name_from_address(file_address)
            self.found_files_row.insert('', 'end', value=file_name)

        children_array = self.found_files_row.get_children()
        self.children_dict = dict()
        for i in range(len(children_array)):
            self.children_dict[children_array[i]] = found_file_array[i]

    def clear_found_files_row(self):
        for file in self.found_files_row.get_children():
            self.found_files_row.delete(file)

    def hide_file_row(self):
        self.file_row.place_forget()

    def view_file_row(self):
        self.file_row.place(x=0, y=0)

    def hide_found_files_row(self):
        self.found_files_row.place_forget()

    def view_found_files_row(self):
        self.found_files_row.place(x=0, y=0)


class ReaderBoxFrame:
    def __init__(self, window):
        self.window = window
        self.create_reader_frame()
        self.create_text_box()

    def create_reader_frame(self):
        self.reader_frame = tk.LabelFrame(self.window.main_frame, width=424, height=517, bd=11, bg="#141414",
                                          relief="sunken")
        self.reader_frame.place(x=461, y=10)

    def create_text_box(self):
        self.text_box = tk.Text(self.reader_frame, bd=0, font="TimesNewRoman 11", bg="#F8F8F8", wrap="word",
                                width=50, height=29)
        self.text_box.place(x=0, y=0)

    def insert_text(self, text):
        self.clear_text_box()
        self.text_box.insert(1.0, text.strip())

    def insert_text_with_key_word(self, text, begin_index, end_index):
        self.clear_text_box()
        self.text_box.insert(1.0, text.strip())
        self.text_box.tag_add("hg1", '1.' + str(begin_index), '1.' + str(end_index))
        self.text_box.tag_config("hg1", background="#3399FF", foreground="#FFFFFF")

    def get_value(self):
        return self.text_box.get(1.0, 'end')

    def clear_text_box(self):
        self.window.operations.displayed_file_address = ''
        self.text_box.delete(1.0, "end")


class FolderButtons:
    def __init__(self, window):
        self.window = window
        self.create_folder_button_frame()
        if self.window.mode.search_flag:
            self.word_buttons()
        else:
            self.folder_buttons()

    def create_folder_button_frame(self):
        self.folder_button_frame = tk.LabelFrame(self.window.main_frame, width=165, height=54, bd=5, bg="#6C6E6F",
                                          relief="raised")
        self.folder_button_frame.place(x=30, y=538)

    def folder_buttons(self):
        self.button_add_folder = tk.Button(self.folder_button_frame, image=self.window.img.add_folder,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_add_window_from_left())
        self.button_add_folder.place(x=4, y=1)

        self.button_edit_folder = tk.Button(self.folder_button_frame, image=self.window.img.edit,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_edit_window_from_left())
        self.button_edit_folder.place(x=56, y=1)

        self.button_delete_folder = tk.Button(self.folder_button_frame, image=self.window.img.delete_folder,
                                              font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                              width=30, height=30,
                                              command=lambda: self.window.operations.delete_file_or_folder_left())
        self.button_delete_folder.place(x=108, y=1)

    def word_buttons(self):
        self.button_add_word = tk.Button(self.folder_button_frame, image=self.window.img.add_word,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_add_window_from_left())
        self.button_add_word.place(x=4, y=1)

        self.button_edit_word = tk.Button(self.folder_button_frame, image=self.window.img.edit,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_edit_window_from_left())
        self.button_edit_word.place(x=56, y=1)

        self.button_delete_word = tk.Button(self.folder_button_frame, image=self.window.img.delete_word,
                                              font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                              width=30, height=30,
                                              command=lambda: self.window.operations.delete_key_word())
        self.button_delete_word.place(x=108, y=1)

    def destroy_word_buttons(self):
        self.button_add_word.destroy()
        self.button_edit_word.destroy()
        self.button_delete_word.destroy()

    def destroy_folder_buttons(self):
        self.button_add_folder.destroy()
        self.button_edit_folder.destroy()
        self.button_delete_folder.destroy()

class FileButtons:
    def __init__(self, window):
        self.window = window
        self.create_file_button_frame()
        self.file_buttons()

    def create_file_button_frame(self):
        self.file_button_frame = tk.LabelFrame(self.window.main_frame, width=165, height=54, bd=5, bg="#6C6E6F",
                                               relief="raised")
        self.file_button_frame.place(x=256, y=538)

    def file_buttons(self):
        self.button_add_file = tk.Button(self.file_button_frame, image=self.window.img.add_file,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_add_window_from_right())
        self.button_add_file.place(x=4, y=1)

        self.button_edit_file = tk.Button(self.file_button_frame, image=self.window.img.edit,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.modal_window.create_edit_window_from_right())
        self.button_edit_file.place(x=56, y=1)

        self.button_delete_file = tk.Button(self.file_button_frame, image=self.window.img.delete_file,
                                           font="TimesNewRoman 8", bg="#141414", bd=4, relief="raised",
                                           width=30, height=30,
                                           command=lambda: self.window.operations.delete_file_or_folder_right())
        self.button_delete_file.place(x=108, y=1)

class SaveButton:
    def __init__(self, window):
        self.window = window
        self.create_save_frame()
        self.create_save_button()

    def create_save_frame(self):
        self.save_frame = tk.LabelFrame(self.window.main_frame, width=331, height=54, bd=5, bg="#6C6E6F",
                                          relief="raised")
        self.save_frame.place(x=508, y=538)

    def create_save_button(self):
        self.button_save = tk.Button(self.save_frame, width=17, text="Сохранить", font="TimesNewRoman 12",
                                     bg="#141414", fg="#F8F8F8", bd=4, relief="raised",
                                     command=lambda: self.window.operations.save_file())
        self.button_save.place(x=75, y=3)