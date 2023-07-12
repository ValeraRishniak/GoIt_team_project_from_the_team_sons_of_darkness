import pickle

class Note:
    def __init__(self, title, description, tag):
        self.title = title
        self.description = description
        self.tag = tag

class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, title, description, tag):
        note = Note(title, description, tag)
        self.notes.append(note)

    def search_notes(self, keyword):
        found_notes = []
        for note in self.notes:
            if keyword in note.title or keyword in note.description or keyword in note.tag:
                found_notes.append(note)
        return found_notes

    def edit_note(self, note_index, new_title, new_description, new_tag):
        note = self.notes[note_index]
        note.title = new_title
        note.description = new_description
        note.tag = new_tag

    def delete_note(self, note_index):
        del self.notes[note_index]

    def sort_notes_by_tag(self):
        sorted_notes = sorted(self.notes, key=lambda note: note.tag)
        return sorted_notes
    
    filename = "bf.Notes.bin"
    def save_notes(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.notes, file)

    def load_notes(self, filename):
        with open(filename, 'rb') as file:
            self.notes = pickle.load(file)

def get_user_input(prompt):
    return input(prompt)

notebook = Notebook()
# notebook.load_notes("Notes.bin")

def main():
    while True:
        print("Меню:")
        print("1 - Додати нотатку")
        print("2 - Пошук нотаток")
        print("3 - Редагувати нотатку")
        print("4 - Видалити нотатку")
        print("5 - Сортувати нотатки за тегами")
        print("6 - Зберегти")
        print("0 - Вийти")

        choice = get_user_input("Виберіть опцію: ")

        if choice == "1":
            title = get_user_input("Введіть заголовок: ")
            description = get_user_input("Введіть опис: ")
            tag = get_user_input("Введіть тег: ")
            notebook.add_note(title, description, tag)
            print("Нотатку додано!")
            print("-" * 25)

        elif choice == "2":
            keyword = get_user_input("Введіть ключове слово для пошуку: ")
            found_notes = notebook.search_notes(keyword)
            if found_notes:
                print("Результати пошуку:")
                for note in found_notes:
                    print(f"Заголовок: {note.title}")
                    print(f"Опис: {note.description}")
                    print(f"Тег: {note.tag}")
                    print("-" * 25)
            else:
                print("Нотатки не знайдено.")
                print("-" * 25)

        elif choice == "3":
            note_index = int(get_user_input("Введіть індекс нотатки, яку потрібно редагувати: "))
            new_title = get_user_input("Введіть новий заголовок: ")
            new_description = get_user_input("Введіть новий опис: ")
            new_tag = get_user_input("Введіть новий тег: ")
            notebook.edit_note(note_index, new_title, new_description, new_tag)
            print("Нотатку відредаговано!")
            print("-" * 25)

        elif choice == "4":
            note_index = int(get_user_input("Введіть індекс нотаткі яку потрібно видалити: "))
            notebook.delete_note(note_index)
            print("Готово! Нотатка видалена.")
            print("-" * 25)
        elif choice == "5":
            sorted_notes = notebook.sort_notes_by_tag()
            if sorted_notes:
                print("Відсортовані нотаткт:")
                for note in sorted_notes:
                    print(f"Заголовок: {note.title}")
                    print(f"Опис: {note.description}")
                    print(f"Тег: {note.tag}")
                    print("-" * 25)
            else:
                print("Вибачте, будь-які записи відсутні.")
                print("-" * 25)

        elif choice == "6":
            notebook.save_notes(filename='bf.Notes.bin')
            print("Нотатки збережено!")
            print("-" * 25)

        elif choice == "0":
            print('До нових зустрічей!')
            break

        else:
            print("Неправильний вибір. Будь ласка, спробуйте ще раз.")
            print("-" * 25)

# Запуск бота-помічника
if __name__ == "__main__":
    main()