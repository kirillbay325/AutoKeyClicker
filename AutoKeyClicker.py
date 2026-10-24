#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import math
import os
import queue
import threading
import time
import tkinter as tk
from ctypes import wintypes
from tkinter import messagebox, ttk

try:
    import keyboard
except ImportError:
    keyboard = None


FONT = "Segoe UI"
FONT_SEMIBOLD = "Segoe UI Semibold"
UI_WIDTH = 500

# Light palette (Material 3 inspired, flat surfaces only)
BG = "#d8e0ec"
CARD = "#ffffff"
FG = "#1b1f27"
MUTED = "#5f6b7a"
ACCENT = "#0b57d0"
ACCENT_ACTIVE = "#0a4cb8"
ACCENT_PRESSED = "#083f9b"
DANGER = "#c13b31"
DANGER_ACTIVE = "#ad3229"
OK = "#137d4b"
HINT = "#8a6d1a"
SURFACE_VARIANT = "#e6ebf3"
TONAL_HOVER = "#dde4ee"
TONAL_PRESSED = "#d5dde9"
OUTLINE = "#bcc7d8"
OUTLINE_STRONG = "#aab7ca"
PRIMARY_CONTAINER = "#cfe0fb"
PRIMARY_CONTAINER_HOVER = "#c4d8f9"
ON_PRIMARY_CONTAINER = "#0c3f8f"
ON_PRIMARY = "#ffffff"
ON_DANGER = "#ffffff"
DISABLED_BG = "#e7ebf1"
DISABLED_FG = "#a2aab6"

# --- Translations (Russian / English) ---
TRANSLATIONS = {
    "ru": {
        "app_title": "AutoKeyClicker",
        "app_subtitle": "Автоклик клавиш и мыши с горячей клавишей",
        "device_label": "Устройство",
        "device_keyboard": "Клавиатура",
        "device_mouse": "Мышь",
        "mode_label": "Режим",
        "mode_click": "Автоклик",
        "mode_hold": "Удержание",
        "target_label": "Что нажимать",
        "btn_record": "Записать",
        "btn_capturing": "Жду…",
        "target_hint": "a, 1, tab, shift, f5, alt+q, ctrl+shift+s. Названия клавиш — на английской раскладке.",
        "params_label": "Параметры",
        "interval_click": "Интервал автоклика, мс",
        "work_time": "Время работы, сек (0 — бесконечно)",
        "hold_duration": "Длительность удержания, сек (0 — до стопа)",
        "mouse_button_label": "Кнопка мыши",
        "mouse_left": "ЛКМ",
        "mouse_right": "ПКМ",
        "mouse_middle": "СКМ",
        "mouse_hint": "ЛКМ — левая, ПКМ — правая, СКМ — средняя.",
        "mouse_interval": "Интервал между кликами, мс",
        "mouse_work_time": "Время работы, сек (0 — бесконечно)",
        "mouse_hint2": "Клики выполняются в текущей позиции курсора. Остановка — горячей клавишей или кнопкой.",
        "hotkey_label": "Горячая клавиша старт/стоп",
        "hotkey_hint": "Повторное нажатие останавливает. Работает поверх других окон.",
        "btn_start": "Начать",
        "btn_stop": "Остановить",
        "status_stopped": "Остановлен",
        "status_running": "Работает — {}",
        "status_capture": "Нажми клавишу или сочетание клавиш…",
        "status_capture_fail": "Не удалось распознать клавишу",
        "lang_label": "Язык",
        "lang_ru": "Русский",
        "lang_en": "English",
        "theme_label": "Тема",
        "theme_light": "Светлая",
        "theme_dark": "Тёмная",
        "err_target_empty": "Укажи клавишу или сочетание",
        "err_target_invalid": "Некорректное сочетание: лишний «+»",
        "err_target_unknown": "Неизвестная клавиша: «{}»",
        "err_number_empty": "{}: введи число",
        "err_number_negative": "{}: значение не может быть отрицательным",
        "err_number_too_big": "{}: слишком большое значение",
        "err_hotkey_empty": "Задай горячую клавишу",
        "err_hotkey_modifiers_only": "Горячая клавиша не может состоять только из модификаторов",
        "err_hotkey_conflict": "Целевая клавиша совпадает с горячей клавишей — выбери другую",
        "err_mouse_send": "не удалось отправить клик мыши",
        "err_generic": "Ошибка: {}",
        "err_keyboard_missing": "Не найдена библиотека keyboard.\n\nУстанови её командой:\npython -m pip install keyboard",
    },
    "en": {
        "app_title": "AutoKeyClicker",
        "app_subtitle": "Auto-click keys and mouse with a hotkey",
        "device_label": "Device",
        "device_keyboard": "Keyboard",
        "device_mouse": "Mouse",
        "mode_label": "Mode",
        "mode_click": "Auto-click",
        "mode_hold": "Hold",
        "target_label": "Key to press",
        "btn_record": "Record",
        "btn_capturing": "Waiting…",
        "target_hint": "a, 1, tab, shift, f5, alt+q, ctrl+shift+s. Use English keyboard layout names.",
        "params_label": "Parameters",
        "interval_click": "Auto-click interval, ms",
        "work_time": "Work time, sec (0 — infinite)",
        "hold_duration": "Hold duration, sec (0 — until stop)",
        "mouse_button_label": "Mouse button",
        "mouse_left": "LMB",
        "mouse_right": "RMB",
        "mouse_middle": "MMB",
        "mouse_hint": "LMB — left, RMB — right, MMB — middle.",
        "mouse_interval": "Interval between clicks, ms",
        "mouse_work_time": "Work time, sec (0 — infinite)",
        "mouse_hint2": "Clicks are performed at the current cursor position. Stop with hotkey or button.",
        "hotkey_label": "Start/Stop hotkey",
        "hotkey_hint": "Press again to stop. Works over other windows.",
        "btn_start": "Start",
        "btn_stop": "Stop",
        "status_stopped": "Stopped",
        "status_running": "Running — {}",
        "status_capture": "Press a key or key combination…",
        "status_capture_fail": "Failed to recognize key",
        "lang_label": "Language",
        "lang_ru": "Russian",
        "lang_en": "English",
        "theme_label": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "err_target_empty": "Specify a key or combination",
        "err_target_invalid": "Invalid combination: extra '+'",
        "err_target_unknown": "Unknown key: '{}'",
        "err_number_empty": "{}: enter a number",
        "err_number_negative": "{}: value cannot be negative",
        "err_number_too_big": "{}: value too large",
        "err_hotkey_empty": "Set a hotkey",
        "err_hotkey_modifiers_only": "Hotkey cannot consist only of modifiers",
        "err_hotkey_conflict": "Target key matches hotkey — choose another",
        "err_mouse_send": "failed to send mouse click",
        "err_generic": "Error: {}",
        "err_keyboard_missing": "keyboard library not found.\n\nInstall it with:\npython -m pip install keyboard",
    },
}

# --- Dark theme colors ---
DARK_BG = "#0f1115"
DARK_CARD = "#171a20"
DARK_FG = "#e6e9ef"
DARK_MUTED = "#9aa4b2"
DARK_ACCENT = "#8ab4f8"
DARK_ACCENT_ACTIVE = "#a3c5fa"
DARK_ACCENT_PRESSED = "#7aa7ef"
DARK_DANGER = "#f28b82"
DARK_DANGER_ACTIVE = "#f6a29b"
DARK_OK = "#6dd58c"
DARK_HINT = "#e3c46b"
DARK_ENTRY_BG = "#171a20"
DARK_SURFACE_VARIANT = "#22262e"
DARK_TONAL_HOVER = "#2a2f38"
DARK_TONAL_PRESSED = "#303641"
DARK_OUTLINE = "#2a2f38"
DARK_OUTLINE_STRONG = "#3a414d"
DARK_PRIMARY_CONTAINER = "#1d3357"
DARK_PRIMARY_CONTAINER_HOVER = "#24406b"
DARK_ON_PRIMARY_CONTAINER = "#c6dafa"
DARK_ON_PRIMARY = "#08192e"
DARK_ON_DANGER = "#2b0b08"
DARK_DISABLED_BG = "#22262e"
DARK_DISABLED_FG = "#5a626e"


def palette_for(theme):
    if theme == "dark":
        return {
            "bg": DARK_BG,
            "surface": DARK_CARD,
            "fg": DARK_FG,
            "muted": DARK_MUTED,
            "primary": DARK_ACCENT,
            "primary_hover": DARK_ACCENT_ACTIVE,
            "primary_pressed": DARK_ACCENT_PRESSED,
            "on_primary": DARK_ON_PRIMARY,
            "primary_container": DARK_PRIMARY_CONTAINER,
            "primary_container_hover": DARK_PRIMARY_CONTAINER_HOVER,
            "on_primary_container": DARK_ON_PRIMARY_CONTAINER,
            "surface_variant": DARK_SURFACE_VARIANT,
            "tonal_hover": DARK_TONAL_HOVER,
            "tonal_pressed": DARK_TONAL_PRESSED,
            "outline": DARK_OUTLINE,
            "outline_strong": DARK_OUTLINE_STRONG,
            "danger": DARK_DANGER,
            "danger_hover": DARK_DANGER_ACTIVE,
            "danger_pressed": "#e07b72",
            "on_danger": DARK_ON_DANGER,
            "success": DARK_OK,
            "hint": DARK_HINT,
            "entry_bg": DARK_ENTRY_BG,
            "disabled_bg": DARK_DISABLED_BG,
            "disabled_fg": DARK_DISABLED_FG,
        }
    return {
        "bg": BG,
        "surface": CARD,
        "fg": FG,
        "muted": MUTED,
        "primary": ACCENT,
        "primary_hover": ACCENT_ACTIVE,
        "primary_pressed": ACCENT_PRESSED,
        "on_primary": ON_PRIMARY,
        "primary_container": PRIMARY_CONTAINER,
        "primary_container_hover": PRIMARY_CONTAINER_HOVER,
        "on_primary_container": ON_PRIMARY_CONTAINER,
        "surface_variant": SURFACE_VARIANT,
        "tonal_hover": TONAL_HOVER,
        "tonal_pressed": TONAL_PRESSED,
        "outline": OUTLINE,
        "outline_strong": OUTLINE_STRONG,
        "danger": DANGER,
        "danger_hover": DANGER_ACTIVE,
        "danger_pressed": "#9c2c24",
        "on_danger": ON_DANGER,
        "success": OK,
        "hint": HINT,
        "entry_bg": CARD,
        "disabled_bg": DISABLED_BG,
        "disabled_fg": DISABLED_FG,
    }

MODIFIERS = {"ctrl", "alt", "shift", "windows"}
MODIFIER_ORDER = {"ctrl": 0, "alt": 1, "shift": 2, "windows": 3}
ALIASES = {
    "super": "windows",
    "cmd": "windows",
    "command": "windows",
    "pgdn": "page down",
}

ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong
INPUT_MOUSE = 0
MOUSE_BUTTONS = {
    "left": (0x0002, 0x0004),
    "right": (0x0008, 0x0010),
    "middle": (0x0020, 0x0040),
}
USER32 = ctypes.windll.user32 if hasattr(ctypes, "windll") else None
WINMM = ctypes.windll.winmm if hasattr(ctypes, "windll") else None


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("mi", MOUSEINPUT)]


def normalize_key(name):
    key = keyboard.normalize_name(name.strip().lower())
    return ALIASES.get(key, key)


class ValidationError(ValueError):
    """ValueError carrying a translation key instead of a ready message."""

    def __init__(self, key, *params):
        super().__init__(key)
        self.key = key
        self.params = params


def parse_combo(text):
    if not text or not text.strip():
        raise ValidationError("err_target_empty")
    parts = [part.strip() for part in text.split("+")]
    if any(not part for part in parts):
        raise ValidationError("err_target_invalid")
    keys = []
    for part in parts:
        key = normalize_key(part)
        try:
            keyboard.key_to_scan_codes(key)
        except Exception:
            raise ValidationError("err_target_unknown", part)
        if key not in keys:
            keys.append(key)
    keys.sort(key=lambda item: MODIFIER_ORDER.get(item, 4))
    return keys


def parse_number(text, title, maximum):
    value_text = (text or "").strip().replace(",", ".")
    if not value_text:
        raise ValidationError("err_number_empty", title)
    try:
        value = float(value_text)
    except ValueError:
        raise ValidationError("err_number_empty", title)
    if value < 0:
        raise ValidationError("err_number_negative", title)
    if value > maximum:
        raise ValidationError("err_number_too_big", title)
    return value


def precise_wait(stop_event, delay):
    if delay <= 0:
        return stop_event.is_set()
    deadline = time.perf_counter() + delay
    while True:
        if stop_event.is_set():
            return True
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            return False
        if remaining > 0.02:
            if stop_event.wait(remaining - 0.015):
                return True
        else:
            time.sleep(0.001)


def setup_style(root, theme="light"):
    p = palette_for(theme)
    root.configure(bg=p["bg"])
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", font=(FONT, 10), background=p["surface"], foreground=p["fg"])
    style.configure("TFrame", background=p["surface"])
    style.configure("Window.TFrame", background=p["bg"])
    style.configure("Window.TLabel", background=p["bg"], foreground=p["fg"])
    style.configure("WindowMuted.TLabel", background=p["bg"], foreground=p["muted"],
                    font=(FONT, 9))
    style.configure("TLabel", background=p["surface"], foreground=p["fg"])
    style.configure("Muted.TLabel", background=p["surface"], foreground=p["muted"],
                    font=(FONT, 9))

    style.configure("TEntry", fieldbackground=p["entry_bg"], foreground=p["fg"],
                    bordercolor=p["outline_strong"], lightcolor=p["outline_strong"],
                    darkcolor=p["outline_strong"], insertcolor=p["fg"],
                    padding=(10, 4), relief="flat")
    style.map("TEntry",
              bordercolor=[("focus", p["primary"]), ("disabled", p["outline"])],
              lightcolor=[("focus", p["primary"]), ("disabled", p["outline"])],
              darkcolor=[("focus", p["primary"]), ("disabled", p["outline"])],
              fieldbackground=[("disabled", p["surface_variant"])],
              foreground=[("disabled", p["disabled_fg"])])

    style.configure("TButton", background=p["surface_variant"], foreground=p["fg"],
                    bordercolor=p["surface_variant"], lightcolor=p["surface_variant"],
                    darkcolor=p["surface_variant"], focuscolor=p["surface_variant"],
                    padding=(12, 6), font=(FONT, 10), relief="flat")
    style.map("TButton",
              background=[("active", p["tonal_hover"]), ("pressed", p["tonal_pressed"])],
              foreground=[("disabled", p["disabled_fg"])])
    return style


def _round_points(x1, y1, x2, y2, r, steps=8):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    points = []
    corners = (
        (x2 - r, y1 + r, -90, 0),
        (x2 - r, y2 - r, 0, 90),
        (x1 + r, y2 - r, 90, 180),
        (x1 + r, y1 + r, 180, 270),
    )
    for cx, cy, start, end in corners:
        for index in range(steps + 1):
            angle = math.radians(start + (end - start) * index / steps)
            points.extend((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def draw_round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    return canvas.create_polygon(_round_points(x1, y1, x2, y2, r), **kwargs)


class RoundedButton(tk.Canvas):
    """Flat rounded button drawn on a canvas so its corners stay smooth in Tk."""

    def __init__(self, master, text, command=None, palette=None, kind="tonal",
                 width=120, height=34, radius=9, font=None, padx=12, anchor="center"):
        self._outer_bg = master.cget("bg")
        super().__init__(master, width=width, height=height, bg=self._outer_bg,
                         highlightthickness=0, bd=0, cursor="hand2", takefocus=0)
        self._palette = palette or palette_for("light")
        self._kind = kind
        self._state = "normal"
        self._text = text
        self._command = command
        self._bw = width
        self._bh = height
        self._radius = radius
        self._font = font or (FONT, 10)
        self._padx = padx
        self._anchor = anchor
        self._hover = False
        self._pressed = False
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", self._on_resize)
        self._redraw()

    def _on_resize(self, event):
        if event.width != self._bw or event.height != self._bh:
            self._bw = max(event.width, 2)
            self._bh = max(event.height, 2)
            self._redraw()

    def _colors(self):
        p = self._palette
        kind = self._kind
        if self._state == "disabled":
            return p["disabled_bg"], p["disabled_fg"], p["disabled_bg"]
        if kind == "filled":
            bg = p["primary"]
            if self._pressed:
                bg = p["primary_pressed"]
            elif self._hover:
                bg = p["primary_hover"]
            return bg, p["on_primary"], bg
        if kind == "danger":
            bg = p["danger"]
            if self._pressed:
                bg = p["danger_pressed"]
            elif self._hover:
                bg = p["danger_hover"]
            return bg, p["on_danger"], bg
        if kind == "outline":
            active = self._hover or self._pressed
            bg = p["primary_container"] if active else p["surface"]
            border = p["primary"] if active else p["outline_strong"]
            return bg, p["primary"], border
        if kind == "outlined":
            active = self._hover or self._pressed
            bg = p["surface_variant"] if active else p["surface"]
            border = p["outline_strong"]
            return bg, p["fg"], border
        if kind == "field":
            if self._pressed:
                return p["primary_container"], p["on_primary_container"], p["primary"]
            if self._hover:
                return p["surface_variant"], p["fg"], p["outline_strong"]
            return p["surface"], p["fg"], p["outline_strong"]
        if kind == "segment":
            bg = p["tonal_hover"] if (self._hover or self._pressed) else p["surface"]
            return bg, p["fg"], p["outline_strong"]
        if kind == "segment_on":
            bg = p["primary_container_hover"] if (self._hover or self._pressed) else p["primary_container"]
            return bg, p["on_primary_container"], p["primary"]
        bg = p["surface_variant"]
        if self._pressed:
            bg = p["tonal_pressed"]
        elif self._hover:
            bg = p["tonal_hover"]
        return bg, p["fg"], p["outline"]

    def _redraw(self):
        self.delete("all")
        bg, fg, border = self._colors()
        draw_round_rect(self, 1, 1, self._bw - 1, self._bh - 1, self._radius,
                        fill=bg, outline=border, width=1)
        if self._anchor == "w":
            tx, anchor = self._padx, "w"
        elif self._anchor == "e":
            tx, anchor = self._bw - self._padx, "e"
        else:
            tx, anchor = self._bw / 2, "center"
        self.create_text(tx, self._bh / 2, text=self._text, fill=fg, font=self._font,
                         anchor=anchor)

    def _on_enter(self, _event):
        if self._state == "normal":
            self._hover = True
            self._redraw()

    def _on_leave(self, _event):
        self._hover = False
        self._pressed = False
        self._redraw()

    def _on_press(self, _event):
        if self._state == "normal":
            self._pressed = True
            self._redraw()

    def _on_release(self, event):
        was_pressed = self._pressed
        self._pressed = False
        self._redraw()
        if (was_pressed and self._state == "normal"
                and 0 <= event.x < self._bw and 0 <= event.y < self._bh):
            if self._command is not None:
                self._command()

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self._redraw()

    def set_state(self, state):
        if state != self._state:
            self._state = state
            self._hover = False
            self._pressed = False
            self.configure(cursor="hand2" if state == "normal" else "arrow")
            self._redraw()

    def set_kind(self, kind):
        if kind != self._kind:
            self._kind = kind
            self._redraw()


class Card(tk.Frame):
    """Rounded flat surface card with a section title and a content frame."""

    def __init__(self, master, title, palette, radius=14, pad=7):
        outer_bg = master.cget("bg")
        super().__init__(master, bg=outer_bg, bd=0, highlightthickness=0)
        self._radius = radius
        self._pad = pad
        self._canvas = tk.Canvas(self, bg=outer_bg, highlightthickness=0, bd=0)
        self._canvas.pack(fill="both", expand=True)
        self._shape = draw_round_rect(self._canvas, 0.5, 0.5, 1.5, 1.5, radius,
                                      fill=palette["surface"], outline=palette["outline"],
                                      width=1)
        self.body = tk.Frame(self._canvas, bg=palette["surface"])
        self._window = self._canvas.create_window(pad, pad, window=self.body, anchor="nw")
        self.title_label = tk.Label(self.body, text=title, bg=palette["surface"],
                                    fg=palette["muted"], anchor="w",
                                    font=(FONT_SEMIBOLD, 10))
        self.title_label.pack(fill="x")
        self.content = tk.Frame(self.body, bg=palette["surface"])
        self.content.pack(fill="both", expand=True, pady=(2, 0))
        self._canvas.bind("<Configure>", self._on_canvas)
        self.body.bind("<Configure>", self._on_body)

    def _on_canvas(self, event):
        w = max(event.width, 2)
        h = max(event.height, 2)
        self._canvas.coords(self._shape, *_round_points(1, 1, w - 1, h - 1, self._radius))
        self._canvas.itemconfigure(self._window, width=max(w - 2 * self._pad, 2))

    def _on_body(self, event):
        height = event.height + 2 * self._pad
        if int(self._canvas.cget("height")) != height:
            self._canvas.configure(height=height)

    def set_title(self, text):
        self.title_label.configure(text=text)


class ChoicePopup(tk.Toplevel):
    """Flat popup list. Unlike ttk.Combobox the popup owns no focus, so a click
    on an inactive window cannot close it right after it opens."""

    def __init__(self, master, anchor, options, current, on_pick, palette, on_close):
        super().__init__(master, bg=palette["outline"], bd=0)
        self.withdraw()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self._on_pick = on_pick
        self._on_close = on_close

        body = tk.Frame(self, bg=palette["surface"], bd=0,
                        highlightthickness=1, highlightbackground=palette["outline"])
        body.pack(fill="both", expand=True)
        for value, label in options:
            mark = "\u2713  " if value == current else "     "
            color = palette["primary"] if value == current else palette["fg"]
            row = tk.Label(body, text=mark + label, anchor="w", justify="left",
                           bg=palette["surface"], fg=color, padx=14, pady=7,
                           font=(FONT, 10), cursor="hand2")
            row.pack(fill="x")
            row.bind("<Enter>", lambda _e, r=row: r.configure(bg=palette["primary_container"],
                                                              fg=palette["on_primary_container"]))
            row.bind("<Leave>", lambda _e, r=row, c=color: r.configure(bg=palette["surface"], fg=c))
            row.bind("<ButtonRelease-1>", lambda _e, v=value: self._choose(v))

        self.update_idletasks()
        width = max(anchor.winfo_width(), body.winfo_reqwidth())
        height = body.winfo_reqheight()
        x = anchor.winfo_rootx()
        y = anchor.winfo_rooty() + anchor.winfo_height() + 2
        if y + height > self.winfo_screenheight():
            y = max(0, anchor.winfo_rooty() - height - 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
        self.grab_set()
        self._escape_bind = master.bind("<Escape>", lambda _e: self.close(), add="+")
        self.bind("<Button-1>", self._on_press)

    def _on_press(self, event):
        if not (0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height()):
            self.close()

    def _choose(self, value):
        self.close()
        self._on_pick(value)

    def close(self):
        if not self.winfo_exists():
            self._on_close()
            return
        try:
            self.grab_release()
        except tk.TclError:
            pass
        try:
            self.master.unbind("<Escape>", self._escape_bind)
        except tk.TclError:
            pass
        self.destroy()
        self._on_close()


class AutoKeyClicker:
    def __init__(self, root):
        self.root = root
        self._queue = queue.Queue()
        self._hotkey_hook = None
        self._hotkey_scans = []
        self._hotkey_combo = None
        self._hotkey_pressed = set()
        self._hotkey_triggered = False
        self._capturing = None
        self._running = False
        self._run_token = 0
        self._worker = None
        self._stop_event = None
        self._closing = False
        self._window_width = 0
        self._timer_boost = False

        if WINMM is not None:
            try:
                WINMM.timeBeginPeriod(1)
                self._timer_boost = True
            except Exception:
                pass

        self.device_var = tk.StringVar(value="keyboard")
        self.mode_var = tk.StringVar(value="click")
        self.target_var = tk.StringVar(value="a")
        self.interval_var = tk.StringVar(value="100")
        self.work_var = tk.StringVar(value="0")
        self.hold_var = tk.StringVar(value="1")
        self.mouse_button_var = tk.StringVar(value="left")
        self.mouse_interval_var = tk.StringVar(value="100")
        self.mouse_work_var = tk.StringVar(value="0")
        self.hotkey_var = tk.StringVar(value="f8")
        self._lang = "ru"
        self.theme_var = tk.StringVar(value="light")
        self._menu = None

        root.title(self.t("app_title"))
        setup_style(root, self.theme_var.get())
        self._build_ui()

        root.protocol("WM_DELETE_WINDOW", self._on_close)
        root.resizable(False, False)
        root.update_idletasks()
        self._window_width = min(UI_WIDTH, max(360, int(root.winfo_screenwidth() * 0.9)))
        content_height = self._outer.winfo_reqheight()
        height = min(content_height, self._max_height())
        x = max(0, (root.winfo_screenwidth() - self._window_width) // 2)
        y = max(0, (root.winfo_screenheight() - height) // 3)
        root.geometry(f"{self._window_width}x{height}+{x}+{y}")
        self.root.after(60, self._fit_window)
        self.root.bind("<MouseWheel>", self._on_mousewheel)

        if keyboard is not None:
            self._hotkey_hook = keyboard.hook(self._on_key_event)
        self._register_hotkey()
        self.root.after(25, self._poll_queue)

    def _build_ui(self):
        if getattr(self, "_viewport", None) is not None:
            self._viewport.destroy()
            self._menu = None
        p = self._palette()
        viewport = tk.Frame(self.root, bg=p["bg"])
        viewport.pack(fill="both", expand=True)
        self._viewport = viewport
        self._canvas = tk.Canvas(viewport, bg=p["bg"], highlightthickness=0, bd=0,
                                 yscrollincrement=24)
        self._canvas.pack(fill="both", expand=True)
        self._scrollbar = tk.Canvas(viewport, bg=p["bg"], highlightthickness=0, bd=0,
                                    width=5)
        self._scrollbar.bind("<Button-1>", self._on_scroll_drag)
        self._scrollbar.bind("<B1-Motion>", self._on_scroll_drag)
        self._drag_offset = None
        self._wrap_value = 0

        outer = tk.Frame(self._canvas, bg=p["bg"], padx=14, pady=8)
        outer.columnconfigure(0, weight=1)
        self._outer = outer
        self._canvas_window = self._canvas.create_window(0, 0, window=outer, anchor="nw")
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        header = tk.Frame(outer, bg=p["bg"])
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        self.title_label = tk.Label(header, text=self.t("app_title"), bg=p["bg"], fg=p["fg"],
                                    anchor="w", font=(FONT_SEMIBOLD, 17))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.subtitle_label = tk.Label(header, text=self.t("app_subtitle"), bg=p["bg"],
                                       fg=p["muted"], anchor="w", font=(FONT, 9))
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(1, 0))

        settings = tk.Frame(header, bg=p["bg"])
        settings.grid(row=0, column=1, rowspan=2, sticky="e")
        self.lang_caption = tk.Label(settings, text=self.t("lang_label"), bg=p["bg"],
                                     fg=p["muted"], font=(FONT, 9))
        self.lang_caption.grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.lang_combo = RoundedButton(settings, self._dropdown_text("lang_" + self._lang),
                                        command=self._show_lang_menu, palette=p, kind="field",
                                        width=118, height=24, radius=7, font=(FONT, 9))
        self.lang_combo.grid(row=0, column=1, sticky="e")
        self.theme_caption = tk.Label(settings, text=self.t("theme_label"), bg=p["bg"],
                                      fg=p["muted"], font=(FONT, 9))
        self.theme_caption.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(3, 0))
        self.theme_combo = RoundedButton(settings, self._dropdown_text("theme_" + self.theme_var.get()),
                                         command=self._show_theme_menu, palette=p, kind="field",
                                         width=118, height=24, radius=7, font=(FONT, 9))
        self.theme_combo.grid(row=1, column=1, sticky="e", pady=(3, 0))

        self.device_box_ref = Card(outer, self.t("device_label"), p)
        self.device_box_ref.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        device_seg = tk.Frame(self.device_box_ref.content, bg=p["surface"])
        device_seg.pack(fill="x")
        device_seg.columnconfigure(0, weight=1)
        device_seg.columnconfigure(1, weight=1)
        self.device_kb = RoundedButton(device_seg, self.t("device_keyboard"), palette=p,
                                       kind="segment", command=lambda: self._choose_device("keyboard"),
                                       height=28, radius=8)
        self.device_kb.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.device_mouse = RoundedButton(device_seg, self.t("device_mouse"), palette=p,
                                          kind="segment", command=lambda: self._choose_device("mouse"),
                                          height=28, radius=8)
        self.device_mouse.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.mode_section = tk.Frame(self.device_box_ref.content, bg=p["surface"])
        self.mode_section.pack(fill="x", pady=(12, 0))
        tk.Frame(self.mode_section, bg=p["outline"], height=1).pack(fill="x", pady=(0, 10))
        self.mode_title = tk.Label(self.mode_section, text=self.t("mode_label"), bg=p["surface"],
                                   fg=p["muted"], anchor="w", font=(FONT_SEMIBOLD, 10))
        self.mode_title.pack(anchor="w", pady=(0, 6))
        mode_seg = tk.Frame(self.mode_section, bg=p["surface"])
        mode_seg.pack(fill="x")
        mode_seg.columnconfigure(0, weight=1)
        mode_seg.columnconfigure(1, weight=1)
        self.radio_click = RoundedButton(mode_seg, self.t("mode_click"), palette=p, kind="segment",
                                         command=lambda: self._choose_mode("click"), height=28, radius=8)
        self.radio_click.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.radio_hold = RoundedButton(mode_seg, self.t("mode_hold"), palette=p, kind="segment",
                                        command=lambda: self._choose_mode("hold"), height=28, radius=8)
        self.radio_hold.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.keyboard_container = tk.Frame(outer, bg=p["bg"])
        self.keyboard_container.grid(row=2, column=0, sticky="ew", pady=(3, 0))
        self.keyboard_container.columnconfigure(0, weight=1)

        self.key_box_ref = Card(self.keyboard_container, self.t("target_label"), p)
        self.key_box_ref.grid(row=0, column=0, sticky="ew")
        key_row = tk.Frame(self.key_box_ref.content, bg=p["surface"])
        key_row.pack(fill="x")
        key_row.columnconfigure(0, weight=1)
        self.target_entry = ttk.Entry(key_row, textvariable=self.target_var, font=(FONT, 10))
        self.target_entry.grid(row=0, column=0, sticky="ew")
        self.target_capture_btn = RoundedButton(key_row, self.t("btn_record"), palette=p,
                                                kind="outlined", command=self._capture_target,
                                                width=96, height=28, radius=8)
        self.target_capture_btn.grid(row=0, column=1, padx=(8, 0))
        self.target_hint_label = tk.Label(self.key_box_ref.content, text=self.t("target_hint"),
                                          bg=p["surface"], fg=p["muted"], anchor="w", justify="left",
                                          wraplength=430, font=(FONT, 9))
        self.target_hint_label.pack(fill="x", pady=(5, 0))

        params_block = tk.Frame(self.key_box_ref.content, bg=p["surface"])
        params_block.pack(fill="x", pady=(10, 0))
        tk.Frame(params_block, bg=p["outline"], height=1).pack(fill="x", pady=(0, 9))
        self.params_title = tk.Label(params_block, text=self.t("params_label"), bg=p["surface"],
                                     fg=p["muted"], anchor="w", font=(FONT_SEMIBOLD, 10))
        self.params_title.pack(anchor="w", pady=(0, 3))
        grid = tk.Frame(params_block, bg=p["surface"])
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        self.interval_label = tk.Label(grid, text=self.t("interval_click"), bg=p["surface"],
                                       fg=p["fg"], anchor="w", font=(FONT, 10))
        self.interval_label.grid(row=0, column=0, sticky="w", pady=2)
        self.interval_entry = ttk.Entry(grid, textvariable=self.interval_var, width=9,
                                        justify="right", font=(FONT, 10))
        self.interval_entry.grid(row=0, column=1, sticky="e", pady=2)
        self.work_label = tk.Label(grid, text=self.t("work_time"), bg=p["surface"],
                                   fg=p["fg"], anchor="w", font=(FONT, 10))
        self.work_label.grid(row=1, column=0, sticky="w", pady=2)
        self.work_entry = ttk.Entry(grid, textvariable=self.work_var, width=9,
                                    justify="right", font=(FONT, 10))
        self.work_entry.grid(row=1, column=1, sticky="e", pady=2)
        self.hold_label = tk.Label(grid, text=self.t("hold_duration"), bg=p["surface"],
                                   fg=p["fg"], anchor="w", font=(FONT, 10))
        self.hold_label.grid(row=2, column=0, sticky="w", pady=2)
        self.hold_entry = ttk.Entry(grid, textvariable=self.hold_var, width=9,
                                    justify="right", font=(FONT, 10))
        self.hold_entry.grid(row=2, column=1, sticky="e", pady=2)

        self.mouse_container = tk.Frame(outer, bg=p["bg"])
        self.mouse_container.grid(row=2, column=0, sticky="ew", pady=(3, 0))
        self.mouse_container.columnconfigure(0, weight=1)
        self.mouse_container.grid_remove()

        self.mouse_button_box_ref = Card(self.mouse_container, self.t("mouse_button_label"), p)
        self.mouse_button_box_ref.grid(row=0, column=0, sticky="ew")
        mouse_seg = tk.Frame(self.mouse_button_box_ref.content, bg=p["surface"])
        mouse_seg.pack(fill="x")
        for index in range(3):
            mouse_seg.columnconfigure(index, weight=1)
        self.mouse_left = RoundedButton(mouse_seg, self.t("mouse_left"), palette=p, kind="segment",
                                        command=lambda: self._choose_mouse("left"), height=28, radius=8)
        self.mouse_left.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        self.mouse_right = RoundedButton(mouse_seg, self.t("mouse_right"), palette=p, kind="segment",
                                         command=lambda: self._choose_mouse("right"), height=28, radius=8)
        self.mouse_right.grid(row=0, column=1, sticky="ew", padx=3)
        self.mouse_middle = RoundedButton(mouse_seg, self.t("mouse_middle"), palette=p, kind="segment",
                                          command=lambda: self._choose_mouse("middle"), height=28, radius=8)
        self.mouse_middle.grid(row=0, column=2, sticky="ew", padx=(3, 0))
        self.mouse_hint_label = tk.Label(self.mouse_button_box_ref.content, text=self.t("mouse_hint"),
                                         bg=p["surface"], fg=p["muted"], anchor="w", justify="left",
                                         wraplength=430, font=(FONT, 9))
        self.mouse_hint_label.pack(fill="x", pady=(5, 0))

        self.mouse_params_ref = Card(self.mouse_container, self.t("params_label"), p)
        self.mouse_params_ref.grid(row=1, column=0, sticky="ew", pady=(3, 0))
        mgrid = self.mouse_params_ref.content
        mgrid.columnconfigure(0, weight=1)
        self.mouse_interval_label = tk.Label(mgrid, text=self.t("mouse_interval"), bg=p["surface"],
                                             fg=p["fg"], anchor="w", font=(FONT, 10))
        self.mouse_interval_label.grid(row=0, column=0, sticky="w", pady=2)
        self.mouse_interval_entry = ttk.Entry(mgrid, textvariable=self.mouse_interval_var, width=9,
                                              justify="right", font=(FONT, 10))
        self.mouse_interval_entry.grid(row=0, column=1, sticky="e", pady=2)
        self.mouse_work_label = tk.Label(mgrid, text=self.t("mouse_work_time"), bg=p["surface"],
                                         fg=p["fg"], anchor="w", font=(FONT, 10))
        self.mouse_work_label.grid(row=1, column=0, sticky="w", pady=2)
        self.mouse_work_entry = ttk.Entry(mgrid, textvariable=self.mouse_work_var, width=9,
                                          justify="right", font=(FONT, 10))
        self.mouse_work_entry.grid(row=1, column=1, sticky="e", pady=2)

        self.mouse_hint2_label = tk.Label(self.mouse_container, text=self.t("mouse_hint2"),
                                          bg=p["bg"], fg=p["muted"], anchor="w", justify="left",
                                          wraplength=468, font=(FONT, 9))
        self.mouse_hint2_label.grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.hotkey_box_ref = Card(outer, self.t("hotkey_label"), p)
        self.hotkey_box_ref.grid(row=3, column=0, sticky="ew", pady=(3, 0))
        hotkey_row = tk.Frame(self.hotkey_box_ref.content, bg=p["surface"])
        hotkey_row.pack(fill="x")
        hotkey_row.columnconfigure(0, weight=1)
        self.hotkey_entry = ttk.Entry(hotkey_row, textvariable=self.hotkey_var, font=(FONT, 10))
        self.hotkey_entry.grid(row=0, column=0, sticky="ew")
        self.hotkey_capture_btn = RoundedButton(hotkey_row, self.t("btn_record"), palette=p,
                                                kind="outlined", command=self._capture_hotkey,
                                                width=96, height=28, radius=8)
        self.hotkey_capture_btn.grid(row=0, column=1, padx=(8, 0))
        self.hotkey_hint_label = tk.Label(self.hotkey_box_ref.content, text=self.t("hotkey_hint"),
                                          bg=p["surface"], fg=p["muted"], anchor="w", justify="left",
                                          wraplength=430, font=(FONT, 9))
        self.hotkey_hint_label.pack(fill="x", pady=(5, 0))

        self.start_btn = RoundedButton(outer, self.t("btn_start"), palette=p, kind="filled",
                                       command=self._toggle, height=38, radius=19,
                                       font=(FONT_SEMIBOLD, 11))
        self.start_btn.grid(row=4, column=0, sticky="ew", pady=(5, 0))

        self.status_label = tk.Label(outer, text="", bg=p["bg"], fg=p["muted"], anchor="w",
                                     justify="left", wraplength=468, font=(FONT, 9))
        self.status_label.grid(row=5, column=0, sticky="ew", pady=(3, 0))
        self._set_status(self.t("status_stopped"), "idle")

        self.hotkey_entry.bind("<FocusOut>", lambda _event: self._register_hotkey())
        self.hotkey_entry.bind("<Return>", lambda _event: self._register_hotkey())
        for entry in (self.target_entry, self.interval_entry, self.work_entry, self.hold_entry,
                      self.mouse_interval_entry, self.mouse_work_entry):
            entry.bind("<Return>", lambda _event: self._toggle())

        self._refresh_segments()
        self._apply_device_visibility()
        self._apply_theme_colors()
        self._sync_controls()
        self._rebuild_ui()

    def _refresh_segments(self):
        for button, var, value in (
            (self.device_kb, self.device_var, "keyboard"),
            (self.device_mouse, self.device_var, "mouse"),
            (self.radio_click, self.mode_var, "click"),
            (self.radio_hold, self.mode_var, "hold"),
            (self.mouse_left, self.mouse_button_var, "left"),
            (self.mouse_right, self.mouse_button_var, "right"),
            (self.mouse_middle, self.mouse_button_var, "middle"),
        ):
            button.set_kind("segment_on" if var.get() == value else "segment")

    def _choose_device(self, value):
        if self.device_var.get() == value:
            return
        self.device_var.set(value)
        self._refresh_segments()
        self._switch_device()

    def _choose_mode(self, value):
        if self.mode_var.get() == value:
            return
        self.mode_var.set(value)
        self._refresh_segments()
        self._sync_controls()

    def _choose_mouse(self, value):
        if self.mouse_button_var.get() == value:
            return
        self.mouse_button_var.set(value)
        self._refresh_segments()
        self._sync_controls()

    def _dropdown_text(self, key):
        return self.t(key) + "  \u25be"

    def _palette(self):
        return palette_for(self.theme_var.get())

    def _close_menu(self):
        if self._menu is not None:
            self._menu.close()

    def _show_choice_menu(self, anchor, options, current, on_pick):
        self.root.focus_force()
        self._close_menu()
        self._menu = ChoicePopup(self.root, anchor, options, current, on_pick, self._palette(),
                                 self._on_menu_closed)

    def _on_menu_closed(self):
        self._menu = None

    def _show_lang_menu(self):
        self._show_choice_menu(
            self.lang_combo,
            [("ru", self.t("lang_ru")), ("en", self.t("lang_en"))],
            self._lang,
            self._set_lang,
        )

    def _show_theme_menu(self):
        self._show_choice_menu(
            self.theme_combo,
            [("light", self.t("theme_light")), ("dark", self.t("theme_dark"))],
            self.theme_var.get(),
            self._set_theme,
        )

    def _set_lang(self, value):
        if value == self._lang:
            return
        self._lang = value
        self._rebuild_ui()

    def _set_theme(self, value):
        if value == self.theme_var.get():
            return
        fraction = 0.0
        if getattr(self, "_canvas", None) is not None:
            try:
                fraction = self._canvas.yview()[0]
            except tk.TclError:
                fraction = 0.0
        self.theme_var.set(value)
        setup_style(self.root, value)
        self._pending_scroll = fraction or None
        self._build_ui()
        self._fit_window()

    def _scroll_to(self, fraction):
        if getattr(self, "_canvas", None) is None or not self._canvas.winfo_exists():
            return
        self._canvas.yview_moveto(min(1.0, max(0.0, fraction)))
        self._draw_scroll_thumb()

    def _rebuild_ui(self):
        """Refresh all translated texts after a language change."""
        self.root.title(self.t("app_title"))
        self.title_label.configure(text=self.t("app_title"))
        self.subtitle_label.configure(text=self.t("app_subtitle"))

        self.lang_caption.configure(text=self.t("lang_label"))
        self.theme_caption.configure(text=self.t("theme_label"))
        self.lang_combo.set_text(self._dropdown_text("lang_" + self._lang))
        self.theme_combo.set_text(self._dropdown_text("theme_" + self.theme_var.get()))

        self.device_box_ref.set_title(self.t("device_label"))
        self.mode_title.configure(text=self.t("mode_label"))
        self.key_box_ref.set_title(self.t("target_label"))
        self.mouse_button_box_ref.set_title(self.t("mouse_button_label"))
        self.mouse_params_ref.set_title(self.t("params_label"))
        self.hotkey_box_ref.set_title(self.t("hotkey_label"))

        self.device_kb.set_text(self.t("device_keyboard"))
        self.device_mouse.set_text(self.t("device_mouse"))
        self.radio_click.set_text(self.t("mode_click"))
        self.radio_hold.set_text(self.t("mode_hold"))
        self.mouse_left.set_text(self.t("mouse_left"))
        self.mouse_right.set_text(self.t("mouse_right"))
        self.mouse_middle.set_text(self.t("mouse_middle"))

        if self._capturing is not None:
            capture_button = self.target_capture_btn if self._capturing == "target" else self.hotkey_capture_btn
            capture_button.set_text(self.t("btn_capturing"))
        else:
            self.target_capture_btn.set_text(self.t("btn_record"))
            self.hotkey_capture_btn.set_text(self.t("btn_record"))
        if self._running:
            self.start_btn.set_text(self.t("btn_stop"))
            self.start_btn.set_kind("danger")
        else:
            self.start_btn.set_text(self.t("btn_start"))
            self.start_btn.set_kind("filled")

        self.target_hint_label.configure(text=self.t("target_hint"))
        self.interval_label.configure(text=self.t("interval_click"))
        self.work_label.configure(text=self.t("work_time"))
        self.hold_label.configure(text=self.t("hold_duration"))
        self.mouse_hint_label.configure(text=self.t("mouse_hint"))
        self.mouse_interval_label.configure(text=self.t("mouse_interval"))
        self.mouse_work_label.configure(text=self.t("mouse_work_time"))
        self.mouse_hint2_label.configure(text=self.t("mouse_hint2"))
        self.hotkey_hint_label.configure(text=self.t("hotkey_hint"))

        if self._running:
            if self.device_var.get() == "keyboard":
                action = self.t("mode_click") if self.mode_var.get() == "click" else self.t("mode_hold")
            else:
                action = self.t("mouse_" + self.mouse_button_var.get())
            self._set_status(self.t("status_running").format(action), "running")
        else:
            self._set_status(self.t("status_stopped"), "idle")

        self._fit_window()

    def _max_height(self):
        return max(360, int(self.root.winfo_screenheight() * 0.8))

    def _fit_window(self):
        if not self._window_width or self._closing:
            return
        self.root.update_idletasks()
        content_height = self._outer.winfo_reqheight()
        self.root.geometry(f"{self._window_width}x{min(content_height, self._max_height())}")
        self.root.after_idle(self._refresh_scroll)

    def _on_canvas_configure(self, event):
        width = max(event.width, 2)
        self._canvas.itemconfigure(self._canvas_window, width=width)
        if not hasattr(self, "status_label"):
            return
        wrap = max(220, width - 28 - 14 - 4)
        if wrap != self._wrap_value:
            self._wrap_value = wrap
            for label in (self.target_hint_label, self.hotkey_hint_label,
                          self.mouse_hint_label):
                label.configure(wraplength=wrap)
            outer_wrap = max(220, width - 28 - 4)
            self.mouse_hint2_label.configure(wraplength=outer_wrap)
            self.status_label.configure(wraplength=outer_wrap)
        self._refresh_scroll()

    def _refresh_scroll(self):
        if self._closing or not getattr(self, "_canvas", None):
            return
        if not self._canvas.winfo_exists():
            return
        width = self._canvas.winfo_width()
        content_height = self._outer.winfo_reqheight()
        self._canvas.configure(scrollregion=(0, 0, width, content_height))
        pending = getattr(self, "_pending_scroll", None)
        if pending is not None and self._canvas.winfo_height() > 50:
            self._pending_scroll = None
            self._canvas.yview_moveto(min(1.0, max(0.0, pending)))
        if content_height > self._canvas.winfo_height() + 1:
            self._scrollbar.place(relx=1.0, x=-9, y=0, relheight=1.0, width=5)
            self._draw_scroll_thumb()
        else:
            self._scrollbar.place_forget()
            self._canvas.yview_moveto(0)

    def _draw_scroll_thumb(self):
        bar = self._scrollbar
        bar.delete("all")
        if not bar.winfo_ismapped():
            return
        height = bar.winfo_height()
        first, last = self._canvas.yview()
        top, bottom = first * height, last * height
        if bottom - top < 22:
            middle = (top + bottom) / 2
            top = max(0, middle - 11)
            bottom = min(height, middle + 11)
        p = self._palette()
        draw_round_rect(bar, 0.5, top + 2, 4.5, bottom - 2, 2,
                        fill=p["outline_strong"], outline=p["outline_strong"])

    def _on_mousewheel(self, event):
        if not getattr(self, "_canvas", None) or not self._canvas.winfo_exists():
            return
        if self._canvas.yview() == (0.0, 1.0):
            return
        self._canvas.yview_scroll(-2 if event.delta > 0 else 2, "units")
        self._draw_scroll_thumb()

    def _on_scroll_drag(self, event):
        bar = self._scrollbar
        height = bar.winfo_height()
        if height <= 1:
            return
        first, last = self._canvas.yview()
        span = last - first
        thumb_height = span * height
        if event.type == tk.EventType.ButtonPress:
            thumb_top = first * height
            if thumb_top <= event.y <= thumb_top + thumb_height:
                self._drag_offset = event.y - thumb_top
            else:
                self._drag_offset = thumb_height / 2
        if self._drag_offset is None:
            return
        free = max(1.0, height - thumb_height)
        fraction = min(1.0, max(0.0, (event.y - self._drag_offset) / free))
        self._canvas.yview_moveto(fraction)
        self._draw_scroll_thumb()

    def _apply_theme_colors(self):
        p = self._palette()
        self.status_label.configure(bg=p["bg"], fg=p["muted"])
        self.title_label.configure(bg=p["bg"], fg=p["fg"])
        self.subtitle_label.configure(bg=p["bg"], fg=p["muted"])

    def t(self, key, *args):
        table = TRANSLATIONS.get(self._lang, TRANSLATIONS["ru"])
        text = table.get(key, key)
        if args:
            text = text.format(*args)
        return text

    def _error_text(self, exc):
        if isinstance(exc, ValidationError):
            return self.t(exc.key, *exc.params)
        return str(exc)

    def _set_status(self, text, kind="idle"):
        p = self._palette()
        colors = {"idle": p["muted"], "running": p["success"], "error": p["danger"], "hint": p["hint"]}
        prefix = "● " if kind in ("idle", "running") else ""
        self.status_label.configure(text=prefix + text, fg=colors.get(kind, colors["idle"]))

    def _switch_device(self):
        if self._closing:
            return
        self._apply_device_visibility()
        self._fit_window()
        self._sync_controls()

    def _apply_device_visibility(self):
        if self.device_var.get() == "keyboard":
            self.mouse_container.grid_remove()
            self.keyboard_container.grid()
            if not self.mode_section.winfo_manager():
                self.mode_section.pack(fill="x", pady=(12, 0))
        else:
            self.keyboard_container.grid_remove()
            self.mouse_container.grid()
            self.mode_section.pack_forget()

    def _sync_controls(self):
        if self._closing:
            return
        running = self._running
        capturing = self._capturing is not None
        free = not running and not capturing
        device = self.device_var.get()
        keyboard_free = free and device == "keyboard"
        mouse_free = free and device == "mouse"
        mode = self.mode_var.get()

        for button in (self.device_kb, self.device_mouse, self.hotkey_capture_btn):
            button.set_state("normal" if free else "disabled")
        self.hotkey_entry.configure(state="normal" if free else "disabled")
        for button in (self.radio_click, self.radio_hold, self.target_capture_btn):
            button.set_state("normal" if keyboard_free else "disabled")
        self.target_entry.configure(state="normal" if keyboard_free else "disabled")
        for button in (self.mouse_left, self.mouse_right, self.mouse_middle):
            button.set_state("normal" if mouse_free else "disabled")
        self.interval_entry.configure(
            state="normal" if keyboard_free and mode == "click" else "disabled")
        self.work_entry.configure(
            state="normal" if keyboard_free and mode == "click" else "disabled")
        self.hold_entry.configure(
            state="normal" if keyboard_free and mode == "hold" else "disabled")
        self.mouse_interval_entry.configure(
            state="normal" if mouse_free else "disabled")
        self.mouse_work_entry.configure(
            state="normal" if mouse_free else "disabled")
        self.start_btn.set_state("disabled" if capturing else "normal")
        self.start_btn.set_text(self.t("btn_stop") if running else self.t("btn_start"))
        self.start_btn.set_kind("danger" if running else "filled")

    def _register_hotkey(self):
        if keyboard is None or self._closing:
            return None
        text = self.hotkey_var.get().strip()
        try:
            if not text:
                raise ValueError(self.t("err_hotkey_empty"))
            keys = parse_combo(text)
            if not any(key not in MODIFIERS for key in keys):
                raise ValueError(self.t("err_hotkey_modifiers_only"))
            scans = [set(keyboard.key_to_scan_codes(key)) for key in keys]
            combo = "+ ".join(keys)
        except ValueError as exc:
            self._hotkey_scans = []
            self._hotkey_combo = None
            self._set_status(self._error_text(exc), "error")
            return None
        if combo != self._hotkey_combo:
            self._hotkey_scans = scans
            self._hotkey_combo = combo
            self._hotkey_triggered = all(
                codes & self._hotkey_pressed for codes in self._hotkey_scans
            )
        self.hotkey_var.set(combo)
        return keys

    def _on_key_event(self, event):
        if not self._hotkey_scans or self._closing:
            return
        if event.event_type == "down":
            self._hotkey_pressed.add(event.scan_code)
            if not self._hotkey_triggered and all(
                codes & self._hotkey_pressed for codes in self._hotkey_scans
            ):
                self._hotkey_triggered = True
                if self._capturing is None:
                    self._queue.put(("toggle",))
        elif event.event_type == "up":
            self._hotkey_pressed.discard(event.scan_code)
            if not all(codes & self._hotkey_pressed for codes in self._hotkey_scans):
                self._hotkey_triggered = False

    def _capture_target(self):
        self._start_capture("target")

    def _capture_hotkey(self):
        self._start_capture("hotkey")

    def _start_capture(self, which):
        if keyboard is None or self._capturing is not None or self._running:
            return
        self._capturing = which
        button = self.target_capture_btn if which == "target" else self.hotkey_capture_btn
        button.set_text(self.t("btn_capturing"))
        self._sync_controls()
        self._set_status(self.t("status_capture"), "hint")

        def worker():
            result = None
            try:
                result = keyboard.read_hotkey(suppress=False)
            except Exception:
                result = None
            self._queue.put(("captured", which, result))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_capture(self, which, result):
        self._capturing = None
        self.target_capture_btn.set_text(self.t("btn_record"))
        self.hotkey_capture_btn.set_text(self.t("btn_record"))
        if not result:
            self._set_status(self.t("status_capture_fail"), "error")
        elif which == "target":
            self.target_var.set(result)
            self._set_status(self.t("status_stopped"), "idle")
        else:
            self.hotkey_var.set(result)
            if self._register_hotkey() is not None:
                self._set_status(self.t("status_stopped"), "idle")
        self._sync_controls()

    def _toggle(self):
        if self._capturing is not None:
            return
        if self._running:
            self._stop()
        else:
            self._start()

    def _start(self):
        if self._running:
            return
        device = self.device_var.get()
        try:
            if device == "keyboard":
                mode = self.mode_var.get()
                target = parse_combo(self.target_var.get())
                if mode == "click":
                    interval = parse_number(self.interval_var.get(), self.t("interval_click"), 3_600_000) / 1000.0
                    duration = parse_number(self.work_var.get(), self.t("work_time"), 86_400)
                else:
                    hold = parse_number(self.hold_var.get(), self.t("hold_duration"), 86_400)
                hotkey_keys = self._register_hotkey()
                if hotkey_keys is None:
                    return
                if set(hotkey_keys).issubset(set(target)):
                    raise ValueError(self.t("err_hotkey_conflict"))
            else:
                button = self.mouse_button_var.get()
                interval = parse_number(self.mouse_interval_var.get(), self.t("mouse_interval"), 3_600_000) / 1000.0
                duration = parse_number(self.mouse_work_var.get(), self.t("mouse_work_time"), 86_400)
                if self._register_hotkey() is None:
                    return
        except ValueError as exc:
            self._set_status(self._error_text(exc), "error")
            return

        self._running = True
        self._run_token += 1
        token = self._run_token
        self._stop_event = threading.Event()

        if device == "keyboard":
            self.target_var.set("+".join(target))
            if mode == "click":
                worker = threading.Thread(
                    target=self._click_worker,
                    args=(target, interval, duration, self._stop_event, token),
                    daemon=True,
                )
                label = self.t("mode_click")
            else:
                worker = threading.Thread(
                    target=self._hold_worker,
                    args=(target, hold, self._stop_event, token),
                    daemon=True,
                )
                label = self.t("mode_hold")
        else:
            worker = threading.Thread(
                target=self._mouse_worker,
                args=(button, interval, duration, self._stop_event, token),
                daemon=True,
            )
            label = self.t("mouse_" + button)

        self._worker = worker
        self._sync_controls()
        self._set_status(self.t("status_running").format(label), "running")
        worker.start()

    def _stop(self):
        if not self._running:
            return
        self._running = False
        self._run_token += 1
        event = self._stop_event
        if event is not None:
            event.set()
        worker = self._worker
        if worker is not None and worker.is_alive():
            worker.join(timeout=1.0)
        self._worker = None
        self._stop_event = None
        self._sync_controls()
        self._set_status(self.t("status_stopped"), "idle")

    @staticmethod
    def _press(keys):
        for key in keys:
            keyboard.press(key)

    @staticmethod
    def _release(keys):
        for key in reversed(keys):
            try:
                keyboard.release(key)
            except Exception:
                pass

    def _mouse_event(self, flag):
        data = INPUT()
        data.type = INPUT_MOUSE
        data.mi.dwFlags = flag
        if USER32 is None or USER32.SendInput(1, ctypes.byref(data), ctypes.sizeof(INPUT)) != 1:
            raise RuntimeError(self.t("err_mouse_send"))

    def _click_worker(self, keys, interval, duration, stop_event, token):
        deadline = time.monotonic() + duration if duration > 0 else None
        try:
            while not stop_event.is_set():
                if deadline is not None and time.monotonic() >= deadline:
                    break
                self._press(keys)
                self._release(keys)
                delay = interval
                if deadline is not None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    delay = min(delay, remaining)
                if precise_wait(stop_event, delay):
                    break
        except Exception as exc:
            self._queue.put(("error", token, self.t("err_generic", exc)))
        finally:
            self._release(keys)
            self._queue.put(("finished", token))

    def _hold_worker(self, keys, duration, stop_event, token):
        try:
            self._press(keys)
            if duration > 0:
                stop_event.wait(duration)
            else:
                stop_event.wait()
        except Exception as exc:
            self._queue.put(("error", token, self.t("err_generic", exc)))
        finally:
            self._release(keys)
            self._queue.put(("finished", token))

    def _mouse_worker(self, button, interval, duration, stop_event, token):
        down_flag, up_flag = MOUSE_BUTTONS[button]
        deadline = time.monotonic() + duration if duration > 0 else None
        try:
            while not stop_event.is_set():
                if deadline is not None and time.monotonic() >= deadline:
                    break
                self._mouse_event(down_flag)
                self._mouse_event(up_flag)
                delay = interval
                if deadline is not None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    delay = min(delay, remaining)
                if precise_wait(stop_event, delay):
                    break
        except Exception as exc:
            self._queue.put(("error", token, self.t("err_generic", exc)))
        finally:
            try:
                self._mouse_event(up_flag)
            except Exception:
                pass
            self._queue.put(("finished", token))

    def _poll_queue(self):
        if self._closing:
            return
        try:
            while True:
                message = self._queue.get_nowait()
                kind = message[0]
                if kind == "toggle":
                    self._toggle()
                elif kind == "finished":
                    token = message[1]
                    if token == self._run_token and self._running:
                        self._running = False
                        self._worker = None
                        self._stop_event = None
                        self._sync_controls()
                        self._set_status(self.t("status_stopped"), "idle")
                elif kind == "error":
                    token, text = message[1], message[2]
                    if token == self._run_token:
                        self._stop()
                        self._set_status(text, "error")
                elif kind == "captured":
                    self._finish_capture(message[1], message[2])
        except queue.Empty:
            pass
        self.root.after(25, self._poll_queue)

    def _on_close(self):
        if self._closing:
            return
        self._closing = True
        self._close_menu()
        if self._running:
            self._stop()
        if self._hotkey_hook is not None and keyboard is not None:
            try:
                keyboard.unhook(self._hotkey_hook)
            except Exception:
                pass
            self._hotkey_hook = None
        if self._timer_boost:
            try:
                WINMM.timeEndPeriod(1)
            except Exception:
                pass
            self._timer_boost = False
        self.root.destroy()


def main():
    if keyboard is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "AutoKeyClicker",
            TRANSLATIONS["ru"]["err_keyboard_missing"] + "\n\n---\n\n" + TRANSLATIONS["en"]["err_keyboard_missing"],
        )
        root.destroy()
        return
    root = tk.Tk()
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AutoKeyClicker.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except tk.TclError:
            pass
    AutoKeyClicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
