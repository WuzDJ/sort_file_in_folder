import re
from pathlib import Path
import shutil
import sys

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
    
def translate():  
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):   
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()    

Extensions = {
      "pictures": ['.jpeg', '.png', '.jpg', '.svg'],
      "videos": ['.avi', '.mp4', '.mov', '.mkv'],
      "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
      "audio": ['.mp3', '.ogg', '.wav', '.amr'],
      "archives": ['.zip', '.gz', '.tar'],
}

#it creates folders with names == key from Extensions dict
def create_sort_folders(path):
    for key in Extensions:
        new_sort_dir = Path(path/key)
        if not new_sort_dir.exists():
            new_sort_dir.mkdir()

#it dels all empty folders(no sort_folders)
def delete_empty_folders(path):
    for file in path.iterdir():
        if file.is_dir():
            if file.name in Extensions:
                continue
            delete_empty_folders(file)
            try:
                file.rmdir()
            except:
                pass
                
            
#it edits file name without extension
def normalize(file_name):
    file_name = file_name.translate(TRANS)
    file_name = re.sub(r'\W', '_', file_name)
    return file_name

#it main process function. It goes through all folders except sort folders
def folder_processing(path, root_path):
    p = path
    for file in p.iterdir():
        if file.is_dir():
            if file.name in Extensions.keys():
                continue   
            folder_processing(file, root_path)
            continue
        elif file.is_file():
            sort_file(file, root_path)

#it takes files and sorts them
def sort_file(file, root_path):
    file_extension = file.suffix.lower()
    for key, value in Extensions.items():
        if file_extension in value:
            if key == "archives":
                handle_archive(file, root_path, key)
                break
            handle_file(file, root_path, key)
            break
        else:
            continue

#it works with archive files. It renames and moves them to ./archives then unpacks
def handle_archive(file, root_path, key):
    file_extension = file.suffix.lower()
    file_name = file.name.removesuffix(file_extension)
    file_name = normalize(file_name)
    new_file_name = (file_name + file_extension)

    new_dir = Path(root_path/key/file_name)
    new_dir.mkdir(exist_ok=True)

    new_file_path = root_path/key/new_file_name
    file.rename(new_file_path)

    try:
        shutil.unpack_archive(new_file_path, new_dir)
    except shutil.ReadError:
        new_dir.rmdir()
    except PermissionError:
        new_dir.rmdir()
    new_file_path.unlink()

#it works with files. It renames and moves them to sort_folder with name == key
def handle_file(file, root_path, key):
    file_extension = file.suffix.lower()
    file_name = file.name.removesuffix(file_extension)
    file_name = normalize(file_name)
    new_file_name = (file_name + file_extension)
    try:
        file.rename(root_path/key/new_file_name)
    except FileExistsError:
        file.unlink()
   
def main():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()

    translate()
    root_path = Path(sys.argv[1])
    create_sort_folders(root_path)
    folder_processing(root_path, root_path)
    delete_empty_folders(root_path)

if __name__ == '__main__':
   main()
   print("Finish") 
   exit()            
               