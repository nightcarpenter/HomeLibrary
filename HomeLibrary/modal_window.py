from images import *
from backend import *


class ModalWindow:
    def __init__(self, main_window):
        self.window = main_window

    def create_add_window_from_left(self):
        if self.window.mode.search_flag:
            self.create_modal_window('', '', 'key_word', 'add', 'left')
        else:
            pass
            # object_address = '***----find_address----***'
            # self.create_modal_window('', object_address, 'folder', 'add', 'left')

    def create_add_window_from_right(self):
        object_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
        if object_dict:
            middle_folder = object_dict['folder']
            object_address = self.window.tree.current_folder + '\\' + middle_folder
        else:
            object_address = self.window.tree.current_folder
        self.create_modal_window('', object_address, 'file', 'add', 'right')

    def create_edit_window_from_left(self):
        if self.window.mode.search_flag:
            object_dict = self.window.folder_row.folder_row.set(self.window.folder_row.search_words_row.selection())
            if object_dict:
                object_name = object_dict['folder']
                pass
            else:
                tk_message_box.showerror("Ошибка", "Объект не выбран")
        else:
            object_dict = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
            if object_dict:
                object_name = object_dict['folder']
                object_address = self.window.tree.current_folder + '\\' + object_name
                if os.path.isdir(object_address):
                    self.create_modal_window(object_name, object_address, 'folder', 'edit', 'left')
                else:
                    self.create_modal_window(object_name, object_address, 'file', 'edit', 'left')
            else:
                tk_message_box.showerror("Ошибка", "Объект не выбран")

    def create_edit_window_from_right(self):
        if self.window.mode.search_flag:
            object_dict = self.window.file_row.found_files_row.set(self.window.file_row.found_files_row.selection())
            if object_dict:
                object_name = object_dict['file']
                object_address = self.window.operations.displayed_file_address
                if os.path.isfile(object_address):
                    self.create_modal_window(object_name, object_address, 'file', 'edit', 'right')
            else:
                tk_message_box.showerror("Ошибка", "Объект не выбран")
        else:
            object_dict = self.window.file_row.file_row.set(self.window.file_row.file_row.selection())
            if object_dict:
                object_name = object_dict['file']
                middle_folder = self.window.folder_row.folder_row.set(self.window.folder_row.folder_row.selection())
                object_address = self.window.tree.current_folder + '\\' + middle_folder['folder'] + '\\' + object_name
                if os.path.isdir(object_address):
                    self.create_modal_window(object_name, object_address, 'folder', 'edit', 'right')
                else:
                    self.create_modal_window(object_name, object_address, 'file', 'edit', 'right')
            else:
                tk_message_box.showerror("Ошибка", "Объект не выбран")

    def create_modal_window(self, object_name, object_address, object_type, action, frame):
        self._object_type = object_type
        self._action = action
        self._object_addres = object_address
        self._object_name = object_name
        self._frame = frame

        self.root = tk.Toplevel()
        self.root.title('Home Library')
        self.root.geometry('625x134+445+200')
        self.root.resizable(False, False)
        self.root.iconbitmap('img/icon.ico')

        self.main_frame = tk.LabelFrame(self.root, width=625, height=134, bd=0, bg="#3C3F41")
        self.main_frame.place(x=0, y=0)

        self.create_label()

        if action == 'add':
            if self._object_type == 'key_word':
                self.create_entry_add()
                self.create_button_add_word()
            else:
                if self._object_type == 'file':
                    self.create_button_add_file()
                elif self._object_type == 'folder':
                    self.create_button_add_folder()
                self.create_entry_add()
                self.entry_name.insert(0, object_address + '\\')

        elif action == 'edit':
            self.create_button_edit()
            self.create_entry_edit()

        self.root.grab_set()
        self.root.focus()
        self.entry_name.focus_set()
        self.root.wait_window()

    def create_label(self):
        label_text = ''
        if self._object_type == 'folder':
            label_text = 'Имя папки'
        elif self._object_type == 'file':
            label_text = 'Имя файла'
        elif self._object_type == 'key_word':
            label_text = 'Ключевое слово'
        self.search_label_name = tk.Label(self.main_frame, text=label_text, relief="ridge",
                                          font="TimesNewRoman 12",
                                          width="15", bg="#141414", fg="#BCCF62", bd="3")
        self.search_label_name.place(x=10, y=20)

    def create_button_add_file(self):
        self.button_add = tk.Button(self.main_frame, width=13, text='Создать', font="TimesNewRoman 12",
                                    bg="#141414", fg="#F8F8F8", bd=8,
                                    command=lambda: self.window.operations.add_new_file(
                                        self.entry_name.get().strip()))
        self.button_add.place(x=248, y=70)

        self.root.bind("<Return>", self.add_file_enter_go)

    def create_button_add_folder(self):
        self.button_add = tk.Button(self.main_frame, width=13, text='Создать', font="TimesNewRoman 12",
                                    bg="#141414", fg="#F8F8F8", bd=8,
                                    command=lambda: self.window.operations.add_new_folder(
                                        self.entry_name.get().strip()))
        self.button_add.place(x=248, y=70)

        self.root.bind("<Return>", self.add_folder_enter_go)

    def create_button_add_word(self):
        self.button_add = tk.Button(self.main_frame, width=13, text='Добавить', font="TimesNewRoman 12",
                                    bg="#141414", fg="#F8F8F8", bd=8,
                                    command=lambda: self.window.operations.add_new_word(
                                        self.entry_name.get().strip()))
        self.button_add.place(x=248, y=70)

        self.root.bind("<Return>", self.add_word_enter_go)

    def add_file_enter_go(self, event):
        self.window.operations.add_new_file(self.entry_name.get().strip())

    def add_folder_enter_go(self, event):
        self.window.operations.add_new_folder(self.entry_name.get().strip())

    def add_word_enter_go(self, event):
        self.window.operations.add_new_word(self.entry_name.get().strip())

    def create_button_edit(self):
        self.button_edit = tk.Button(self.main_frame, width=13, text='Изменить', font="TimesNewRoman 12",
                                    bg="#141414", fg="#F8F8F8", bd=8,
                                    command=lambda: self.window.operations.edit_object(self._object_type,
                                    self._object_addres, self.entry_name.get().strip(), self._frame))
        self.button_edit.place(x=248, y=70)

        self.root.bind("<Return>", self.edit_enter_go)

    def edit_enter_go(self, event):
        self.window.operations.edit_object(
            self._object_type,self._object_addres, self.entry_name.get().strip(), self._frame)

    def create_entry_add(self):
        self.entry_name = tk.Entry(self.main_frame, bd="2", font="TimesNewRoman 12", width="50",
                                       bg="#F8F8F8")
        self.entry_name.place(x=157, y=20)

    def create_entry_edit(self):
        self.create_entry_add()
        index = self._object_name.rfind('.')

        if index != -1:
            if self._object_name[index:] == '.txt':
                self.entry_name.insert('0', self._object_name[0: index])
        else:
            self.entry_name.insert('0', self._object_name)

    def close_modal_window(self):
        self.root.destroy()
