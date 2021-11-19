import tkinter as tk

class LoadImages():
    def __init__(self):
        self.LoadImages()

    def LoadImages(self):
        self.edit = tk.PhotoImage(file=r'img\edit.png')
        self.add_file = tk.PhotoImage(file=r'img\add_file.png')
        self.delete_file = tk.PhotoImage(file=r'img\delete_file.png')
        self.add_folder = tk.PhotoImage(file=r'img\add_folder.png')
        self.delete_folder = tk.PhotoImage(file=r'img\delete_folder.png')
        self.add_word = tk.PhotoImage(file=r'img\add_word.png')
        self.delete_word = tk.PhotoImage(file=r'img\delete_word.png')

        self.back = tk.PhotoImage(file=r'img\back.png')
        self.copy = tk.PhotoImage(file=r'img\copy.png')


if __name__ == "__main__":

    # окно
    root = tk.Tk()
    root.geometry("300x200+100+100")

    # функция читающая буфер
    def read(e):
        bufer_data['text'] = root.clipboard_get()

    # функция записывающая в буфер
    def write(e):
        root.clipboard_clear()
        root.clipboard_append('akzo rulez:)')

    # текст с содержанием буфера
    bufer_data = tk.Label(root, text="No Data")
    bufer_data.pack(expand='YES')

    # кнопка вызывающая фкнуцию для чтения
    button = tk.Button(root, text="Read Bufer Data")
    button.pack(expand='YES')
    button.bind("<Button-1>", read)

    # кнопка для записи
    button = tk.Button(root, text="Write Bufer Data")
    button.pack(expand='YES')
    button.bind("<Button-1>", write)

    root.mainloop()