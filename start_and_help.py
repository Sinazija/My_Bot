# импорт необходимых модулей,функций
from main_code_bot import main, command_func
from sort import Sorter
from note import run_command, command_list

# инициализируем объект класса Sorter
sort_folder = Sorter()

# список команд главного меню бота
func_list = ['contact book', 'note', 'sort', 'help', 'exit']

# переменные пример для ввода пути папки на разных OS
windows = r"Windows: C:\Users\Username\Documents\My_Folder"
macOS = r"macOS: /Users/Username/Documents/My_folder"
Linux = r"Linux: /home/Username/Documents/My_folder"


# функция хелпер основного меню бота
def main_help():
    print(f"\nThe personal assistant console program can implement the following functionality:\n1) A contact book that can:\n- save contacts with names, addresses, phone numbers, email, and birthdays to the contacts book;\n- display a list of contacts whose birthday is a specified number of days from the current date;\n- check the correctness of the entered phone number and email when creating or editing a record and notify the user in case of incorrect entry;\n- search for contacts among book contacts;\n- edit and delete entries from the contact book;\nTo switch to the contact book functionality, please enter 'Сontact book'\n\n2) Notebook that can:\n- save notes with text information;\n- search for notes;\n- edit and delete notes;\n- add 'tags' to notes, keywords describing the subject and subject of the record;\nsearch and sort notes by keywords (tags);\nTo switch to the Notebook functionality, please enter 'Note'\n\n3) Sort, which can sort files in the specified folder by categories (images, documents, videos, etc.).\nTo switch to the Sort function, please enter 'Sort'\n\nTo exit the Assistant bot, enter 'Exit'\n")


# функция меню адресной книги
def contact_book():
    print(f"\nI am a contact book helper bot!\nI can:\n- Save contacts in Сontact book with names, addresses, phone numbers, email and birthdays (to access this function, please enter 'Add')\n- Display a list of contacts whose birthday is a specified number of days from the current date (to use this function, please enter 'Birthday-list (number)')\n- Search for contacts among contacts in the book (to use this function, please enter 'Search'\n- Edit entries from the contact book (to use this function, please enter 'Edit');\n- Delete entries from the contact book (to use this function, please enter 'Delete')\n- Save contacts to a file (to use this function, please enter 'Save')\n- View contacts saved in the file (to use this function, please enter 'Read')\n\nI also check the correctness of the entered phone number and email when creating or editing a record and notify you in case of an incorrect entry\nFor more detailed information, enter 'Help' or 'Exit' to return to the main menu")


# функция хелпер адресной книги
def contact_book_help():
    print(f"\nThe contact book can implement the following functionality:\n'Add' - adds contact book with names, addresses, phone numbers, email, and birthdays. In order to save the contact, click Add and enter all the necessary information, the required field is Name - this is a unique property of the contact. Also, in the Add function, a check for the adds connput parameters such as Phone number and Email is implemented.\n\nThe contact book has the ability to save contacts' birthdays:\n'Birthday-list (number)' -  display a list of contacts whose birthday is a specified number of days from the current date\n\nWork with the list of contacts is implemented using advanced functions:\n'Search contact' - search for contacts,instead of a contact, enter a request (name/part of a name);\n'Show all' - show all contacts\n'Edit contact'- edit entries from the contact book, instead of contact, enter the name contact;\n'Remove-contact' - delete contact, enter the name for delete;\n'Save' - save contacts to a file (.csv file format).\n'Read' - read data from file (.csv file format)\n\nEnter the command you need from the list above.\nReturn to the main menu, enter 'Exit'")


# функция меню заметок
def notebook():
    print(f"\nI am a notebook helper bot!\nI can:\n- Save notes with text information and keywords (tags) (to access this function, please enter 'Add')\n- Search for notes (to use this function, please enter 'Search')\n- Search for notes and show all notes (to use this function, please enter 'Search-all')\n- Edit notes by index (to use this function, please enter 'Edit-index')\n- Edit notes by keywords (tags)  (to use this keyword, please enter 'Edit-keyword')\n- Delete notes by index (to use this function, please enter 'Delete-index')\n- Delete notes by keywords (tags)  (to use this function, please enter 'Delete-keyword')\n- Sort notes (to use this function, please enter 'Sort')\nFor more detailed information, enter 'Help'")


# функция хелпер заметок
def notebook_help():
    print(f"\nThe notebook has the following list of functions, it can store notes with text information, search for notes, edit and delete notes, it is also possible to add 'tags' to notes, keywords describing the topic and subject of the record, search and sort notes by keywords (tags).\n\nThe list of commands is as follows:\n'Add' - save notes with text information and keywords (tags);\n'Search' - search for notes;\n'Search-all' - search for notes and show all notes;\n'Edit-index' - edit notes by index\n'Edit-keyword' - edit notes by keywords (tags)\n'Delete-index' - delete notes by index \n'Delete-keyword' - delete notes by keywords (tags)\n'Sort' - sort notesEnter the command you need from the list above.\nReturn to the main menu, enter 'Exit'")


# функция меню сортировщика
def sort():
    print(
        f'\nI am a sort of helper bot!\n\nI can:\n- Sort files in the specified folder by category (to use this function, please enter "Sort folder path")\n Folder path for different OS:\n{windows}\n{macOS}\n{Linux}')


# функция для старта бота
def start_bot():
    user_input = input(
        "Hello, I'm a personal assistant console bot, to get started, use, please enter 'Hello': ")
    if user_input.lower().strip() == 'hello':
        user_input = input("\nI can help with the following tasks\n\n- Maintain your personal contact book (to access this function, please enter 'Сontact book')\n\n- Enter any of your test notes (to access this function, please enter 'Note')\n\n- Sort files in the specified folder by category (to access this function, please enter 'Sort')\n\nFor more detailed information, enter 'Help'\nFor finish bot, enter 'Exit'\n\nPlease select a task: ")
        while True:
            if user_input.lower().strip() == 'help':
                main_help()
                user_input = input(
                    "Hi, this main menu bot, please enter your choice or 'help' to see my options: ")

            if user_input.lower().strip() == 'contact book':
                contact_book()
                while True:
                    user_input = input(
                        "\nThis menu contact_ book, please enter your choice or 'help' to view a list of commands or 'exit' for return to the main menu: ")
                    if user_input.lower().strip() == 'help':
                        while user_input == 'help':
                            contact_book_help()
                            user_input = input(
                                "\nPlease enter your choice or 'help' to view a list of commands: ")
                    if user_input.lower().strip() == 'exit':
                        break
                    if user_input in command_func:
                        main(user_input)
                    if user_input:
                        continue
                user_input = input(
                    "\nHi, this main menu bot, please enter your choice or 'help' to see my options: ")

            if user_input.lower().strip() == 'note':
                notebook()
                while True:
                    user_input = input(
                        "\nThis menu notebook, please enter your choice or 'help' to view a list of commands or 'exit' for return to the main menu: ")
                    if user_input.lower().strip() == 'help':
                        while user_input == 'help':
                            notebook_help()
                            user_input = input(
                                "\nPlease enter your choice or 'help' to view a list of commands: ")
                    if user_input.lower().strip() == 'exit':
                        break
                    if user_input.lower() in command_list:
                        run_command(user_input)
                    elif user_input:
                        print("Invalid command")
                        continue
            user_input = input(
                "\nHi, this main menu bot, please enter your choice or 'help' to see my options: ")

            if user_input.lower().strip() == 'sort':
                sort()
                while True:
                    user_input = input(
                        "\nThis menu sort, please enter commands 'sort folder path' or 'exit' for return to the main menu,\n have any questions - enter 'help': ")
                    if user_input.lower().strip() == 'help':
                        sort()
                    if user_input.lower().strip() == 'exit':
                        break
                    try:
                        if user_input.lower().strip().startswith('sort') and user_input.lower().strip()[5:]:
                            sort_folder.sort(user_input.lower().strip()[5:])
                    except FileNotFoundError:
                        print(
                            f'Not find the path, please repeat the command and enter correct path to folder')
                    if user_input:
                        continue
                user_input = input(
                    "\nHi, this main menu bot, please enter your choice or 'help' to see my options: ")

            if user_input.lower().strip() == 'exit':
                print(f'Good bye!')
                break
            if user_input.lower().strip() in func_list:
                continue
            else:
                user_input = input(
                    "\nHi, this main menu bot, please enter your choice or 'help' to see my options: ")
    else:
        start_bot()


start_bot()
