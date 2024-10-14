import os

def count_lines_in_directory(directory):
    total_lines = 0
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    total_lines += len(lines)
            except FileNotFoundError:
                print(f"Le fichier {file_path} n'a pas été trouvé.")
                continue
            except UnicodeDecodeError:
                print(f"Erreur de décodage lors de la lecture du fichier {file_path}.")
                continue
    return total_lines

def main():
    directory = os.getcwd()
    total_lines = count_lines_in_directory(directory)
    with open("total_lines.txt", "w") as output_file:
        output_file.write(f"Nombre total de lignes dans les fichiers .txt : {total_lines}")

if __name__ == "__main__":
    main()
