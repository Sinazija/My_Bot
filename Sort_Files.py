from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re


class Sorter:
    def __init__(self) -> None:
        self.MY_OTHER = []
        self.REGISTER_EXTENSION = {
            'JPEG': [[], 'images'],
            'JPG': [[], 'images'],
            'PNG': [[], 'images'],
            'SVG': [[], 'images'],
            'AVI': [[], 'video'],
            'MP4': [[], 'video'],
            'MOV': [[], 'video'],
            'MKV': [[], 'video'],
            'DOC': [[], 'documents'],
            'DOCX': [[], 'documents'],
            'TXT': [[], 'documents'],
            'PDF': [[], 'documents'],
            'XLSX': [[], 'documents'],
            'PPTX': [[], 'documents'],
            'MP3': [[], 'audio'],
            'OGG': [[], 'audio'],
            'WAV': [[], 'audio'],
            'AMR': [[], 'audio'],
            'ZIP': [[], 'archives'],
            'GZ': [[], 'archives'],
            'TAR': [[], 'archives']
        }
        self.FOLDERS = []
        self.CREATED_FOLDERS = set()
        self.EXTENTIONS = set()
        self.UNKNOWN = set()

    def cyrillic_symbols(self):
        return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'

    def transcription(self):
        return ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

    def trans(self):
        TRANSLATION = {}
        for cyrillic, latin in zip(self.cyrillic_symbols(), self.transcription()):
            TRANSLATION[ord(cyrillic)] = latin
            TRANSLATION[ord(cyrillic.upper())] = latin.upper()
        return TRANSLATION

    def normalize(self, name: str) -> str:
        el_name = name.translate(self.trans())
        el_name = re.sub(r'\W', '_', el_name)
        return el_name

    def get_extension(self, filename: str) -> str:
        return Path(filename).suffix[1:].upper()

    def handle_file(self, filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_name = self.normalize(filename.stem) + filename.suffix
        filename.replace(target_folder / new_file_name)

    def scan_folder(self, folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'other'):
                    self.FOLDERS.append(item)
            else:
                ext = self.get_extension(item.name)
                full_name = folder / item.name
                if not ext:
                    self.MY_OTHER.append(full_name)
                else:
                    try:
                        container = self.REGISTER_EXTENSION[ext][0]
                        self.EXTENTIONS.add(ext)
                        container.append(full_name)
                    except KeyError:
                        self.UNKNOWN.add(ext)
                        self.MY_OTHER.append(full_name)

    def handle_folder(self, folder: Path) -> None:
        try:
            for item in folder.iterdir():
                if item.is_file():
                    item.unlink()  # Видаляємо всі файли у папці
                elif item.is_dir():
                    # Рекурсивно видаляємо вкладені папки
                    self.handle_folder(item)
            folder.rmdir()  # Видаляємо порожню папку
        except OSError:
            print(f'Sorry, we cannot delete folder: {folder}')

    def process_file(self, file: Path, target_folder: Path) -> None:
        self.handle_file(file, target_folder)

    def process_folder(self, folder: Path) -> None:
        self.scan_folder(folder)

        for ext, (folder_list, folder_name) in self.REGISTER_EXTENSION.items():
            target_folder = folder / folder_name / ext
            target_folder.mkdir(exist_ok=True, parents=True)
            self.CREATED_FOLDERS.add(target_folder)
            for file in folder_list:
                self.process_file(file, target_folder)

        for file in self.MY_OTHER:
            target_folder = folder / 'MY_OTHERS'
            target_folder.mkdir(exist_ok=True)
            self.CREATED_FOLDERS.add(target_folder)
            self.process_file(file, target_folder)

        for folder in self.FOLDERS[::-1]:
            self.handle_folder(folder)

        # Видаляємо порожні створені папки
        for folder in self.CREATED_FOLDERS:
            try:
                folder.rmdir()
            except OSError:
                print(f'Sorry, we cannot delete folder: {folder}')

    def sort(self, folder_path: str, num_threads: int) -> None:
        folder = Path(folder_path)
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.submit(self.process_folder, folder)

        self.MY_OTHER = []
        self.FOLDERS = []
        self.EXTENTIONS = set()
        self.UNKNOWN = set()

        print(
            f'The "{folder.name}" directory has been successfully sorted!\nPath: {folder}')


sorter = Sorter()
sorter.sort('D:\Diagrama', num_threads=4)
