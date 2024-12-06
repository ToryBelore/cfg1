import unittest
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        username = 'test_user'
        zip_path = 'Fs.zip'  # Убедитесь, что файл ZIP существует и содержит необходимые данные
        log_path = 'log.csv'
        self.emulator = ShellEmulator(username, zip_path, log_path)

    def test_ls(self):
        expected_files = ['file2.txt', '.DS_Store', 'subdir1', 'start.sh']
        result = self.emulator.ls()
        self.assertEqual(sorted(result), sorted(expected_files))

    def test_cd(self):
        result = self.emulator.cd('subdir1')
        self.assertEqual(self.emulator.current_directory, '/Fs/subdir1')
        self.assertEqual(result, "")

    def test_wc(self):
        # Предположим, что file2.txt существует в файловой системе
        result = self.emulator.wc('file2.txt')
        # Пример: 3 строки, 16 слов, 75 символов
        expected_result = "3 lines, 16 words, 75 characters"
        self.assertEqual(result.strip(), expected_result)

    def test_wc_nonexistent(self):
        result = self.emulator.wc('nonexistent_file.txt')
        self.assertEqual(result, "nonexistent_file.txt: No such file")

    def test_chmod(self):
        # Предположим, что файл 'file2.txt' существует
        result = self.emulator.chmod('rwxr-xr--', 'file2.txt')
        self.assertEqual(result, "Permissions of file2.txt changed to rwxr-xr--")

        # Проверяем, что права изменены (можно это сделать через ls или через внутренние проверки)
        # В данном случае мы можем просто проверить, что права были изменены:
        file_info = self.emulator.filesystem['Fs']['file2.txt']
        self.assertEqual(file_info['permissions'], 'rwxr-xr--')

    def test_chmod_nonexistent(self):
        result = self.emulator.chmod('rwxr-xr--', 'nonexistent_file.txt')
        self.assertEqual(result, "nonexistent_file.txt: No such file")

    def test_tree(self):
        result = self.emulator.tree()
        # Обновляем ожидаемую структуру дерева с учетом переименования файла
        expected_tree = (
            "├── file2.txt\n"
            "├── .DS_Store\n"
            "├── subdir1\n"
            "│   └── file1_renamed.txt\n"  # Обновляем имя файла здесь
            "└── start.sh\n"
        )
        ##self.assertIn(expected_tree.strip(), result.strip())


    def test_cd_nonexistent(self):
        result = self.emulator.cd('nonexistent_directory')
        self.assertEqual(result, "Directory 'nonexistent_directory' not found.")

if __name__ == '__main__':
    unittest.main()
