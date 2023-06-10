import os
import json
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def display_notes(self, note, tags):
        pass


class Note(UserInterface):
    def __init__(self, note, tags):
        self.note = note
        self.tags = tags

    def display_notes(self, note, tags):
        self.note = note
        self.tags = tags

    def __repr__(self) -> str:
        return f"Note: {self.note}"

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.note == other.note and self.tags == other.tags
        return False

# Метод __getitem__ дозволяє отримувати значення властивостей tags
# і note об'єкту Note за допомогою синтаксису з квадратними дужками
    def __getitem__(self, key):
        if key == 'tags':
            return self.tags
        elif key == 'note':
            return self.note
        else:
            raise KeyError(f"Invalid key: {key}")

# забезпечує коректну серіалізацію об'єкту Note до формату JSON.
    @staticmethod
    def default(obj):
        if isinstance(obj, Note):
            return {
                'note': obj.note,
                'tags': obj.tags
            }
        return super().default(obj)


class NoteManager:
    def __init__(self):
        self.notes = {}
        self.load_notes()

    def __str__(self) -> str:
        return f"{self.notes}"

    def __repr__(self) -> str:
        return f"{self.notes}"

# Збереження нотатків в notes.json
    def save_notes(self):
        with open('notes.json', 'w', encoding='utf-8') as file:
            data = {
                key: [{'note': note.note, 'tags': note.tags} for note in value]
                for key, value in self.notes.items()
            }
            json.dump(data, file, default=Note.default,
                      ensure_ascii=False, indent=2, separators=(',', ': '))

# Зчитування нотаток
    def load_notes(self):
        if os.path.exists('notes.json'):
            with open('notes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.notes = {
                    key: [Note(note['note'], note['tags']) for note in value]
                    for key, value in data.items()
                }
# Добавлення нотаток

    def add_notes(self, note, tags):
        if not tags or all(tag == '' for tag in tags):
            tags = ['Ключове слово']
        new_note = Note(note, tags)
        for tag in tags:
            if tag in self.notes:
                self.notes[tag].append(new_note)
            else:
                self.notes[tag] = [new_note]
        print(f"Note added: {new_note}")
        self.save_notes()

# Пошук нотаток по ключовому слову
    def search_notes(self, word):
        result_search = []
        for notes in self.notes.values():
            for note in notes:
                if word.lower() in note.note.lower() or any(word.lower() in tag.lower() for tag in note.tags):
                    result_search.append(note)
        if result_search:
            for note in result_search:
                print(note.note)
        else:
            print("No notes found")

# Пошук усіх нотаток
    def search_all(self):
        if self.notes:
            print("All notes:")
            for tag, notes in self.notes.items():
                for note in notes:
                    print(f"Note: {note.note} (Tags: {', '.join(note.tags)})")
        else:
            print("No notes found")

# Заміна нотатки по індексу
    def edit_note_by_index(self, index, new_note):
        if not str(index).isdigit():
            print("Invalid input. Index must be a digit.")
            return

        index = int(index)
        found = False
        for notes in self.notes.values():
            if 0 <= index < len(notes):
                notes[index].note = new_note
                found = True
                break

        if found:
            print("Note edited")
        else:
            print("Invalid note index")
        self.save_notes()

# Заміна нотатки по ключовому слову
    def edit_note_by_keyword(self, keyword, new_note):
        found = False
        for notes in self.notes.values():
            for note in notes:
                if keyword.lower() in note.tags:
                    note.note = new_note
                    found = True
                    break

        if found:
            print("Note edited")
        else:
            print(f"No note found with keyword '{keyword}'")
        self.save_notes()

# Видалення нотатки по індексу
    def delete_note_by_index(self, index):
        found = False
        for notes in self.notes.values():
            if index >= 0 and index < len(notes):
                del notes[index]
                found = True
                break

        if found:
            print("Note deleted")
        else:
            print("Invalid note index")
        self.save_notes()

# Видалення нотатки по ключовому слову
    def delete_note_by_keyword(self, keyword):
        found = False
        for tag, notes in self.notes.items():
            for index, note in enumerate(notes):
                if keyword.lower() in [tag.lower() for tag in note.tags]:
                    del notes[index]
                    found = True
                    break

        if found:
            print("Note with the specified keyword deleted")
        else:
            print(f"No notes found with keyword '{keyword}'")
        self.save_notes()

# Слортування нотаток по алфавіту
    def sort_notes_alphabetically(self):
        sorted_notes = []
        for tag, notes in self.notes.items():
            sorted_notes.extend(sorted(notes, key=lambda x: x.note.lower()))

        if sorted_notes:
            print("Sorted notes:")
            for note in sorted_notes:
                print(note.note)
        else:
            print("No notes found for sorting")

# Функція для запуску


def run_command(command):
    command = command.lower()
    if command == 'add':
        note = input("Enter the note: ")
        tags = input("Enter the tags (comma-separated): ").split(",")
        note_manager.add_notes(note, tags)
    elif command == 'search':
        word = input("Enter the search word: ")
        note_manager.search_notes(word)
    elif command == 'edit-index':
        try:
            index = int(input("Enter the note index: "))
            new_note = input("Enter the new note: ")
            note_manager.edit_note_by_index(index, new_note)
        except ValueError:
            print("Invalid input. Index must be a digit.")
    elif command == 'edit-keyword':
        keyword = input("Enter the keyword: ")
        new_note = input("Enter the new note: ")
        note_manager.edit_note_by_keyword(keyword, new_note)
    elif command == 'delete-index':
        try:
            index = int(input("Enter the note index: "))
            note_manager.delete_note_by_index(index)
        except ValueError:
            print("Invalid input. Index must be a digit.")
    elif command == 'delete-keyword':
        keyword = input("Enter the keyword: ")
        note_manager.delete_note_by_keyword(keyword)
    elif command == 'sort':
        note_manager.sort_notes_alphabetically()
    elif command == 'search-all':
        note_manager.search_all()
    elif command == 'exit':
        return False
    else:
        print("Invalid command")
        return True


note_manager = NoteManager()


command_list = ['add', 'search', 'search-all', 'edit-index', 'edit-keyword',
                'delete-index', 'delete-keyword', 'sort', 'exit']
#while True:
    #command = input("Enter a command: ")
    #if not run_command(command):
        #break
