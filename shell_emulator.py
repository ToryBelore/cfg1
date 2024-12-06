import os
import csv
import zipfile
import json
from datetime import datetime

class ShellEmulator:
    def __init__(self, username, zip_path, log_path):
        self.username = username
        self.zip_path = zip_path
        self.log_path = log_path
        self.current_directory = '/Fs'  
        self.filesystem = self.load_filesystem(zip_path)  
        self.load_saved_filesystem()  

    def load_filesystem(self, zip_path):
        """Load the filesystem from a ZIP file."""
        filesystem = {}
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                print(f"Reading file: {file_name}")  
                parts = file_name.split('/')
                current_level = filesystem

                for part in parts[:-1]:  
                    if part not in current_level:
                        current_level[part] = {}  
                    current_level = current_level[part]

                if parts[-1]:  
                    try:
                        content = zip_ref.read(file_name).decode('utf-8')
                    except UnicodeDecodeError:
                        content = zip_ref.read(file_name).decode('utf-8', errors='ignore')  
                    current_level[parts[-1]] = {
                        'content': content,
                        'owner': 'default_owner',  
                        'permissions': 'rw-r--r--'  # Права доступа по умолчанию
                    }
        return filesystem

    def load_saved_filesystem(self):
        """Load existing filesystem from JSON file."""
        try:
            with open('filesystem.json', 'r') as f:
                self.filesystem.update(json.load(f))  
        except FileNotFoundError:
            print("No saved filesystem found. Starting fresh.")

    def log_command(self, command):
        """Log the command into the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, mode='a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow([self.username, command, timestamp])

    def execute_command(self, command):
        self.log_command(command)
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args[0] if args else "")
        elif cmd == "exit":
            return "Exiting emulator..."
        elif cmd == "tree":
            return self.tree()
        elif cmd == "wc":
            if len(args) < 1:
                return "Error: wc requires a filename."
            return self.wc(args[0])
        elif cmd == "chmod":
            if len(args) < 2:
                return "Error: chmod requires a mode and a filename."
            return self.chmod(args[0], args[1])
        else:
            return f"Unknown command: {cmd}"

    def ls(self):
        """List the contents of the current directory."""
        current_level = self.get_current_directory()
        if current_level is not None:
            return list(current_level.keys())  
        return "Current directory not found."

    def cd(self, path):
        if path == "..":
            if self.current_directory != '/Fs':
                self.current_directory = '/'.join(self.current_directory.strip('/').split('/')[:-1]) or '/Fs'
            return ""
    
        target = '/'.join(self.current_directory.strip('/').split('/')[:-1] + [path.strip('/')])
        current_level = self.get_current_directory()
        if current_level is not None and target in current_level:
            self.current_directory = '/Fs/' + target  
            return ""
        else:
            return f"Directory '{path}' not found."

    def tree(self):
        """Display the directory structure as a tree."""
        current_level = self.get_current_directory()
        if current_level is None:
            return "Current directory not found."

        tree_str = ""

        def build_tree(level, indent):
            for index, entry in enumerate(level.keys()):
                if entry in ['content', 'owner', 'permissions']:
                    continue

                tree_str_entry = indent + ("└── " if index == len(level) - 1 else "├── ") + entry + "\n"
                nonlocal tree_str
                tree_str += tree_str_entry

                if isinstance(level[entry], dict):
                    new_indent = indent + ("    " if index == len(level) - 1 else "│   ")
                    build_tree(level[entry], new_indent)

        build_tree(current_level, "")
        return tree_str or "(empty)"

    def wc(self, filename):
        """Count lines, words, and characters in a file."""
        current_level = self.get_current_directory()
        if current_level is None:
            return "Current directory not found."
        
        if filename in current_level:
            content = current_level[filename]['content']
            lines = content.splitlines()
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
            return f"{len(lines)} lines, {word_count} words, {char_count} characters"
        else:
            return f"{filename}: No such file"

    def chmod(self, mode, filename):
        """Change the permissions of a file."""
        current_level = self.get_current_directory()
        if current_level is None:
            return "Current directory not found."

        if filename in current_level:
            current_level[filename]['permissions'] = mode
            return f"Permissions of {filename} changed to {mode}"
        else:
            return f"{filename}: No such file"

    def save_filesystem(self):
        """Save the current filesystem to a JSON file."""
        with open('filesystem.json', 'w') as f:
            json.dump(self.filesystem, f)

    def get_current_directory(self):
        """Return the contents of the current directory."""
        current_level = self.filesystem
        for part in self.current_directory.strip('/').split('/'):
            if part:
                current_level = current_level.get(part)
                if current_level is None:
                    return None
        return current_level

if __name__ == '__main__':
    username = 'test_user'
    zip_path = 'Fs.zip'
    log_path = 'log.csv'

    emulator = ShellEmulator(username, zip_path, log_path)
    while True:
        command = input(f"{username}@emulator:~$ ")
        output = emulator.execute_command(command)
        print(output)
        if command == 'exit':
            break
