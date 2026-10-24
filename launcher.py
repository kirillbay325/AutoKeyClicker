#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

APP_NAME = "AutoKeyClicker"
SCRIPT_NAME = "AutoKeyClicker.py"
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "location.txt"
LOG_PATH = BASE_DIR / "launcher.log"

FILE_ATTRIBUTE_REPARSE_POINT = 0x400
SKIP_DIRS = {
    "appdata",
    "windows",
    "program files",
    "program files (x86)",
    "programdata",
    "system volume information",
    "$recycle.bin",
    "recovery",
    "perflogs",
    "msocache",
    "config.msi",
    "$windows.~bt",
    "$windows.~ws",
    "$winreagent",
    "node_modules",
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
}

PROFILE_SEARCH_SECONDS = 10.0
DRIVE_SEARCH_SECONDS = 5.0
MAX_DRIVE_DEPTH = 4


def log(text):
    try:
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {text}\n")
    except OSError:
        pass


def quit_with_error(message):
    log("ERROR: " + message)
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror(APP_NAME, message)
        root.destroy()
    except Exception:
        pass
    sys.exit(1)


def app_script(folder):
    return Path(folder) / SCRIPT_NAME


def read_cached():
    try:
        text = CONFIG_PATH.read_text(encoding="utf-8").strip().strip('"')
    except OSError:
        return None
    if not text:
        return None
    folder = Path(text)
    if app_script(folder).is_file():
        return folder
    return None


def save_cached(folder):
    try:
        CONFIG_PATH.write_text(str(Path(folder).resolve()), encoding="utf-8")
    except OSError as exc:
        log(f"Не удалось сохранить путь: {exc}")


def registry_folders():
    names = (
        "Desktop",
        "Personal",
        "{374DE290-123F-4565-9164-39C4925E467B}",
    )
    folders = []
    try:
        import winreg

        key_name = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name) as key:
            for name in names:
                try:
                    value, _ = winreg.QueryValueEx(key, name)
                except OSError:
                    continue
                folders.append(Path(os.path.expandvars(value)))
    except OSError:
        pass
    return folders


def candidate_roots():
    roots = []

    def add(path):
        if not path:
            return
        try:
            folder = Path(path).expanduser().resolve()
        except OSError:
            return
        if folder not in roots and folder.is_dir():
            roots.append(folder)

    for folder in registry_folders():
        add(folder)
    add(Path.home())
    for env_name in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial"):
        add(os.environ.get(env_name))
    return roots


def fixed_drives():
    drives = []
    try:
        import ctypes

        mask = ctypes.windll.kernel32.GetLogicalDrives()
        for index in range(26):
            if not mask & (1 << index):
                continue
            letter = chr(ord("A") + index)
            root = f"{letter}:\\"
            if ctypes.windll.kernel32.GetDriveTypeW(root) == 3:
                drives.append(Path(root))
    except Exception:
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            root = Path(f"{letter}:\\")
            if root.is_dir():
                drives.append(root)
    return drives


def is_reparse_point(entry):
    try:
        attrs = entry.stat(follow_symlinks=False).st_file_attributes
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except (AttributeError, OSError):
        try:
            return entry.is_symlink()
        except OSError:
            return True


def find_in_tree(root, deadline, max_depth=None):
    root = Path(root)
    if app_script(root).is_file():
        return root
    queue = deque([(root, 0)])
    while queue:
        if time.monotonic() > deadline:
            return None
        folder, depth = queue.popleft()
        try:
            with os.scandir(folder) as entries:
                for entry in entries:
                    if time.monotonic() > deadline:
                        return None
                    try:
                        if entry.is_file(follow_symlinks=False):
                            if entry.name.lower() == SCRIPT_NAME.lower():
                                candidate = Path(entry.path)
                                if candidate.is_file():
                                    return candidate.parent
                            continue
                        if not entry.is_dir(follow_symlinks=False):
                            continue
                        if entry.name.lower() in SKIP_DIRS or entry.name.startswith("."):
                            continue
                        if is_reparse_point(entry):
                            continue
                        if max_depth is None or depth < max_depth:
                            queue.append((Path(entry.path), depth + 1))
                    except OSError:
                        continue
        except OSError:
            continue
    return None


def locate():
    cached = read_cached()
    if cached is not None:
        log(f"Использую сохранённый путь: {cached}")
        return cached

    started = time.monotonic()
    log("Сохранённый путь не найден, ищу папку приложения")
    deadline = started + PROFILE_SEARCH_SECONDS
    for root in candidate_roots():
        if time.monotonic() > deadline:
            break
        found = find_in_tree(root, deadline)
        if found is not None:
            save_cached(found)
            log(f"Нашёл: {found}")
            return found

    for drive in fixed_drives():
        if time.monotonic() > started + PROFILE_SEARCH_SECONDS + DRIVE_SEARCH_SECONDS:
            break
        drive_deadline = min(
            time.monotonic() + DRIVE_SEARCH_SECONDS,
            started + PROFILE_SEARCH_SECONDS + DRIVE_SEARCH_SECONDS,
        )
        found = find_in_tree(drive, drive_deadline, max_depth=MAX_DRIVE_DEPTH)
        if found is not None:
            save_cached(found)
            log(f"Нашёл на диске {drive}: {found}")
            return found

    log("Автопоиск не дал результата")
    return ask_folder()


def ask_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showinfo(
            APP_NAME,
            "Не удалось автоматически найти папку AutoKeyClicker.\n\n"
            "Выбери папку, в которой лежит AutoKeyClicker.py.\n"
            "Я запомню её для следующих запусков.",
        )
        for _ in range(3):
            selected = filedialog.askdirectory(title="Папка AutoKeyClicker")
            if not selected:
                root.destroy()
                return None
            folder = Path(selected)
            if app_script(folder).is_file():
                root.destroy()
                save_cached(folder)
                log(f"Папка выбрана вручную: {folder}")
                return folder
            messagebox.showerror(
                APP_NAME,
                "В этой папке нет AutoKeyClicker.py.\nВыбери папку приложения.",
            )
        root.destroy()
    except Exception as exc:
        log(f"Ошибка диалога выбора папки: {exc}")
    return None


def launch(folder):
    script = app_script(folder)
    log(f"Запускаю: {script}")
    try:
        subprocess.Popen(
            [sys.executable, str(script)],
            cwd=str(script.parent),
            close_fds=True,
        )
    except OSError as exc:
        quit_with_error(
            "Не удалось запустить AutoKeyClicker.\n\n"
            f"{exc}\n\n"
            "Проверь, что Python установлен и папка с программой не повреждена."
        )
        return False
    return True


def main():
    folder = locate()
    if folder is None:
        quit_with_error(
            "Папка с AutoKeyClicker.py не найдена.\n\n"
            "Запусти create_shortcut.bat из папки программы, чтобы ярлык снова знал, где она лежит."
        )
    if app_script(folder).is_file():
        launch(folder)
    else:
        quit_with_error("Файл AutoKeyClicker.py не найден.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        quit_with_error(f"Ошибка запуска AutoKeyClicker:\n{exc}")
