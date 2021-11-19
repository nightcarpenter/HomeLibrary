class Search:
    def __init__(self, window):
        self.window = window

    def search_files(self, word):
        self.found_file_array = list()

        for file_address in self.window.tree.file_list:
            file = open(file_address, encoding='utf-8')
            file_text = file.read()
            file.close()
            if file_text:
                if not(word[0].isalnum()):
                    word = word[1:]
                if not(file_text[0].isalnum()):
                    file_text = file_text[1:]
                if word.strip().lower() in file_text.lower():
                    self.found_file_array.append(file_address)

        self.window.file_row.insert_values_in_found_files_row(self.found_file_array)