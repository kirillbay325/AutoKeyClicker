#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "AutoKeyClicker"
BASE_DIR = Path(__file__).resolve().parent
APP_SCRIPT = BASE_DIR / "AutoKeyClicker.py"
LAUNCHER_SOURCE = BASE_DIR / "launcher.py"
ICON_SOURCE = BASE_DIR / "AutoKeyClicker.ico"
SHORTCUT_NAME = "AutoKeyClicker.lnk"


def print_header():
    print("=" * 58)
    print("  AutoKeyClicker — создание ярлыка")
    print("=" * 58)


def desktop_dir():
    try:
        import winreg

        key_name = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name) as key:
            value, _ = winreg.QueryValueEx(key, "Desktop")
        path = Path(os.path.expandvars(value))
        if path.is_dir():
            return path
    except OSError:
        pass
    for name in ("Desktop", "Рабочий стол"):
        path = Path.home() / name
        if path.is_dir():
            return path
    raise RuntimeError("Не удалось найти папку рабочего стола")


def stable_dir():
    return Path.home() / ".autokeyclicker"


def pythonw_executable():
    exe = Path(sys.executable)
    if exe.name.lower() == "python.exe":
        candidate = exe.with_name("pythonw.exe")
        if candidate.is_file():
            return candidate
    if exe.is_file():
        return exe
    found = shutil.which("pythonw") or shutil.which("python")
    if found:
        return Path(found)
    raise RuntimeError("Не удалось найти pythonw.exe")


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def create_lnk(lnk_path, target, arguments, workdir, icon):
    lines = [
        "$ErrorActionPreference = 'Stop'",
        "$shell = New-Object -ComObject WScript.Shell",
        f"$lnk = $shell.CreateShortcut({ps_quote(lnk_path)})",
        f"$lnk.TargetPath = {ps_quote(target)}",
        f"$lnk.Arguments = {ps_quote(arguments)}",
        f"$lnk.WorkingDirectory = {ps_quote(workdir)}",
        f"$lnk.IconLocation = {ps_quote(icon)}",
        f"$lnk.Description = {ps_quote('AutoKeyClicker — автокликер клавиш и мыши')}",
        "$lnk.WindowStyle = 1",
        "$lnk.Save()",
    ]
    script = "\n".join(lines)
    encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-EncodedCommand",
            encoded,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"PowerShell не смог создать ярлык.\n{details}")
    if not Path(lnk_path).is_file():
        raise RuntimeError("Ярлык не появился на рабочем столе.")


def main():
    print_header()
    if not APP_SCRIPT.is_file():
        raise RuntimeError(f"Не найден файл:\n{APP_SCRIPT}")
    if not LAUNCHER_SOURCE.is_file():
        raise RuntimeError(f"Не найден файл:\n{LAUNCHER_SOURCE}")

    target_dir = stable_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    launcher_target = target_dir / "launcher.py"
    if LAUNCHER_SOURCE.resolve() != launcher_target.resolve():
        shutil.copy2(LAUNCHER_SOURCE, launcher_target)

    icon_target = target_dir / "AutoKeyClicker.ico"
    icon_for_shortcut = Path(sys.executable)
    if ICON_SOURCE.is_file():
        if ICON_SOURCE.resolve() != icon_target.resolve():
            shutil.copy2(ICON_SOURCE, icon_target)
        icon_for_shortcut = icon_target

    (target_dir / "location.txt").write_text(str(BASE_DIR), encoding="utf-8")

    pythonw = pythonw_executable()
    desktop = desktop_dir()
    lnk_path = desktop / SHORTCUT_NAME
    try:
        lnk_path.unlink()
    except FileNotFoundError:
        pass
    except OSError as exc:
        print(f"Предупреждение: не удалось удалить старый ярлык: {exc}")

    create_lnk(
        lnk_path=lnk_path,
        target=pythonw,
        arguments=f'"{launcher_target}"',
        workdir=target_dir,
        icon=f"{icon_for_shortcut},0",
    )

    print()
    print("Готово. Ярлык создан:")
    print(f"  {lnk_path}")
    print()
    print("Служебные файлы ярлыка:")
    print(f"  {target_dir}")
    print()
    print("Приложение:")
    print(f"  {APP_SCRIPT}")
    print()
    print("Папку с программой можно перемещать — ярлык будет искать её сам.")
    print("Если ярлык удалён, просто запусти create_shortcut.bat снова.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print()
        print("ОШИБКА:", exc)
        print()
        print("Проверь, что Python установлен и папка программы не повреждена.")
        sys.exit(1)
