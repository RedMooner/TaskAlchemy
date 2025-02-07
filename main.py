import os
import subprocess
import logging
from pathlib import Path
from colorama import Fore, Style, init

# Инициализация colorama для работы с цветами
init()

# Настройка логирования
logging.basicConfig(filename='command_shell.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Папка для хранения командлетов
CMDlets_DIR = "cmdlets"

def list_cmdlets():
    """Функция для вывода списка доступных командлетов."""
    cmdlets = []
    for root, dirs, files in os.walk(CMDlets_DIR):
        for file in files:
            if file.endswith(".py") or file.endswith(".ps1"):
                cmdlets.append(os.path.splitext(file)[0])  # Возвращаем только имя без расширения
    return cmdlets

def get_cmdlet_path(cmdlet_name):
    """Функция для получения полного пути к командлету по его имени."""
    for root, dirs, files in os.walk(CMDlets_DIR):
        for file in files:
            if file.endswith(".py") or file.endswith(".ps1"):
                if os.path.splitext(file)[0] == cmdlet_name:
                    return os.path.join(root, file)
    return None

def run_cmdlet(cmdlet_name, args):
    """Функция для запуска командлета."""
    cmdlet_path = get_cmdlet_path(cmdlet_name)
    if not cmdlet_path:
        print(Fore.RED + f"Командлет {cmdlet_name} не найден." + Style.RESET_ALL)
        logging.error(f"cmdlet {cmdlet_name} not found.")
        return

    # Вывод заголовка
    title = f"-------------------------------------{cmdlet_name}-------------------------------------"
    print(Fore.GREEN + title + Style.RESET_ALL)

    # Вывод информации из info.txt
    info_path = os.path.join(os.path.dirname(cmdlet_path), "info.txt")
    if os.path.exists(info_path):
        with open(info_path, "r") as info_file:
            print(Fore.YELLOW + info_file.read() + Style.RESET_ALL)

    if cmdlet_path.endswith(".py"):
        # Запуск Python скрипта с аргументами
        try:
            command = ["python", cmdlet_path] + args
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(Fore.RED + result.stderr + Style.RESET_ALL)
                logging.error(f"Ошибка при выполнении {cmdlet_name}: {result.stderr}")
            else:
                logging.info(f"Командлет {cmdlet_name} выполнен успешно.")
        except Exception as e:
            print(Fore.RED + f"Ошибка при выполнении {cmdlet_name}: {e}" + Style.RESET_ALL)
            logging.error(f"Ошибка при выполнении {cmdlet_name}: {e}")

    elif cmdlet_path.endswith(".ps1"):
        # Запуск PowerShell скрипта
        try:
            command = ["powershell", "-File", cmdlet_path] + args
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(Fore.RED + result.stderr + Style.RESET_ALL)
                logging.error(f"Ошибка при выполнении {cmdlet_name}: {result.stderr}")
            else:
                logging.info(f"Командлет {cmdlet_name} выполнен успешно.")
        except Exception as e:
            print(Fore.RED + f"Ошибка при выполнении {cmdlet_name}: {e}" + Style.RESET_ALL)
            logging.error(f"Ошибка при выполнении {cmdlet_name}: {e}")

def create_cmdlet(cmdlet_name):
    """Функция для создания нового командлета."""
    if not cmdlet_name.endswith(".py") and not cmdlet_name.endswith(".ps1"):
        print(Fore.RED + "Ошибка: командлет должен иметь расширение .py или .ps1." + Style.RESET_ALL)
        return

    cmdlet_dir = os.path.join(CMDlets_DIR, os.path.splitext(cmdlet_name)[0])
    cmdlet_path = os.path.join(cmdlet_dir, cmdlet_name)
    if os.path.exists(cmdlet_path):
        print(Fore.YELLOW + f"Командлет {cmdlet_name} уже существует." + Style.RESET_ALL)
        return

    os.makedirs(cmdlet_dir, exist_ok=True)

    with open(cmdlet_path, "w") as f:
        if cmdlet_name.endswith(".py"):
            f.write("""# Ваш Python скрипт
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-name", help="Имя")
args = parser.parse_args()

if args.name:
    print(f"Привет, {args.name}!")
else:
    print("Привет, мир!")
""")
        elif cmdlet_name.endswith(".ps1"):
            f.write("""# Ваш PowerShell скрипт
param (
    [string]$name
)

if ($name) {
    Write-Output "Привет, $name!"
} else {
    Write-Output "Привет, мир!"
}
""")

    # Создание файла info.txt
    info_path = os.path.join(cmdlet_dir, "info.txt")
    with open(info_path, "w") as info_file:
        info_file.write(f"Информация о командлете {cmdlet_name}.\n")

    print(Fore.GREEN + f"Командлет {cmdlet_name} создан." + Style.RESET_ALL)
    logging.info(f"Командлет {cmdlet_name} создан.")

def delete_cmdlet(cmdlet_name):
    """Функция для удаления командлета."""
    cmdlet_dir = os.path.join(CMDlets_DIR, cmdlet_name)
    cmdlet_path = os.path.join(cmdlet_dir, f"{cmdlet_name}.py")  # Ищем .py файл
    if not os.path.exists(cmdlet_path):
        cmdlet_path = os.path.join(cmdlet_dir, f"{cmdlet_name}.ps1")  # Ищем .ps1 файл
        if not os.path.exists(cmdlet_path):
            print(Fore.RED + f"Командлет {cmdlet_name} не найден." + Style.RESET_ALL)
            return

    os.remove(cmdlet_path)
    os.remove(os.path.join(cmdlet_dir, "info.txt"))
    os.rmdir(cmdlet_dir)
    print(Fore.GREEN + f"Командлет {cmdlet_name} удален." + Style.RESET_ALL)
    logging.info(f"Командлет {cmdlet_name} удален.")

def man_cmdlet(cmdlet_name):
    """Функция для вывода информации о командлете."""
    cmdlet_dir = os.path.join(CMDlets_DIR, cmdlet_name)
    info_path = os.path.join(cmdlet_dir, "info.txt")
    if not os.path.exists(info_path):
        print(Fore.RED + f"Информация о командлете {cmdlet_name} не найдена." + Style.RESET_ALL)
        return

    with open(info_path, "r") as info_file:
        print(Fore.YELLOW + info_file.read() + Style.RESET_ALL)

def help():
    """Функция для вывода справки."""
    print("Доступные команды:")
    print("help - вывести справку")
    print("list - вывести список доступных командлетов")
    print("run <cmdlet_name> [args] - запустить командлет с аргументами")
    print("create <cmdlet_name> - создать новый командлет")
    print("delete <cmdlet_name> - удалить командлет")
    print("man <cmdlet_name> - вывести информацию о командлете")

def main():
    """Основная функция командной оболочки."""
    # Создаем папку для командлетов, если она не существует
    Path(CMDlets_DIR).mkdir(exist_ok=True)

    print("Добро пожаловать в командную оболочку. Введите 'help' для справки.")
    while True:
        command = input("> ").strip().split()
        if not command:
            continue

        cmd = command[0]
        if cmd == "help":
            help()
        elif cmd == "list":
            cmdlets = list_cmdlets()
            if cmdlets:
                print("Доступные командлеты:")
                for cmdlet in cmdlets:
                    print(cmdlet)
            else:
                print(Fore.YELLOW + "Командлеты не найдены." + Style.RESET_ALL)
        elif cmd == "run":
            if len(command) < 2:
                print(Fore.RED + "Ошибка: укажите имя командлета." + Style.RESET_ALL)
            else:
                args = command[2:] if len(command) > 2 else []
                run_cmdlet(command[1], args)
        elif cmd == "create":
            if len(command) < 2:
                print(Fore.RED + "Ошибка: укажите имя командлета." + Style.RESET_ALL)
            else:
                create_cmdlet(command[1])
        elif cmd == "delete":
            if len(command) < 2:
                print(Fore.RED + "Ошибка: укажите имя командлета." + Style.RESET_ALL)
            else:
                delete_cmdlet(command[1])
        elif cmd == "man":
            if len(command) < 2:
                print(Fore.RED + "Ошибка: укажите имя командлета." + Style.RESET_ALL)
            else:
                man_cmdlet(command[1])
        else:
            print(Fore.RED + f"Неизвестная команда: {cmd}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
