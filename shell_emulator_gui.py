import os
import sys
import tkinter as tk
import zipfile
from tkinter import scrolledtext
from shell_emulator import ShellEmulator

# Убедимся, что Python находит модуль shell_emulator
sys.path.insert(0, os.path.dirname(__file__))

class EmulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Shell Emulator GUI")

        # Создание виджета для отображения вывода
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=20, width=80)
        self.output_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Поле для ввода команд
        self.command_entry = tk.Entry(master, width=80)
        self.command_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.command_entry.bind("<Return>", self.execute_command)  # Привязка нажатия Enter к выполнению команды
        self.command_entry.focus_set()  # Установка фокуса на поле ввода

        # Кнопка выхода из эмулятора
        self.exit_button = tk.Button(master, text="Выход", command=self.quit)
        self.exit_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Настройка строк и столбцов для изменения размера
        master.grid_rowconfigure(0, weight=1)  # Разрешаем текстовому полю менять размер
        master.grid_columnconfigure(0, weight=1)  # Разрешаем изменять размер по горизонтали

        # Инициализация эмулятора с тестовыми данными
        self.username = "user"
        self.zip_path = "Fs.zip"  # Путь к вашему ZIP файлу с файловой системой
        self.log_path = "log.csv"
        self.emulator = ShellEmulator(self.username, self.zip_path, self.log_path)

    def execute_command(self, event=None):
        # Получаем команду из поля ввода
        command = self.command_entry.get().strip()
        print(f"Выполняется команда: '{command}'")  # Отладочный вывод
        if command:
            # Выполняем команду и получаем результат
            output = self.emulator.execute_command(command)
            # Выводим результат в текстовое поле
            self.output_text.insert(tk.END, f"{self.username}@emulator:~$ {command}\n{output}\n")
            self.output_text.see(tk.END)  # Скроллим до последней строки
            # Очищаем поле ввода
            self.command_entry.delete(0, tk.END)
        else:
            print("Пустая команда. Попробуйте снова.")  # Отладочный вывод

    def quit(self):
        print("Закрытие эмулятора...")  # Отладочный вывод
        self.emulator.execute_command("exit")
        self.master.destroy()  # Закрываем окно

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorGUI(root)
    root.mainloop()
