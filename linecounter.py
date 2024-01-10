import os

def count_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def scan_directory(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.css') or file.endswith(".html") or file.endswith(".js") or file.endswith(".py") and not file == 'linecounter.py':
                file_path = os.path.join(root, file)
                total_lines += count_lines(file_path)
    return total_lines

directory_path = '.'  # Replace with the path of the directory you want to scan
lines_count = scan_directory(directory_path)
print(f'Total lines in files: {lines_count}')
