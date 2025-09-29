#!/usr/bin/env python3
"""Text file manager for lab 21 with CLI and Tkinter GUI."""
from __future__ import annotations

import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Iterable

PAGE_SIZE = 25
DEFAULT_ENCODING = "utf-8"


def prompt_path(prompt: str) -> Path:
    value = input(prompt).strip()
    if not value:
        raise ValueError("Path must not be empty")
    return Path(value).expanduser().resolve()


def ask_encoding(prompt: str = "Enter encoding (blank for utf-8): ") -> str:
    value = input(prompt).strip()
    return value or DEFAULT_ENCODING


def ensure_parent_directory(path: Path) -> None:
    if not path.parent.exists():
        raise FileNotFoundError(f"Parent directory does not exist: {path.parent}")


def create_text_file(path: Path, encoding: str, initial_content: str | None = None, overwrite: bool = False) -> None:
    ensure_parent_directory(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")
    data = initial_content or ""
    with path.open("w", encoding=encoding, newline="") as handle:
        handle.write(data)


def read_lines(path: Path, encoding: str) -> Iterable[str]:
    with path.open("r", encoding=encoding, errors="replace") as handle:
        for line in handle:
            yield line.rstrip("\n")


def display_file(path: Path, encoding: str, page_size: int = PAGE_SIZE) -> None:
    line_number = 1
    for line in read_lines(path, encoding):
        print(f"{line_number:>6}: {line}")
        if line_number % page_size == 0:
            if input("-- press Enter to continue or q to quit -- ").strip().lower().startswith("q"):
                return
        line_number += 1


def append_text(path: Path, encoding: str, text: str) -> None:
    with path.open("a", encoding=encoding, newline="") as handle:
        handle.write(text)


def clear_file(path: Path) -> None:
    path.write_text("", encoding=DEFAULT_ENCODING)


def find_and_replace(path: Path, encoding: str, target: str, replacement: str) -> int:
    content = path.read_text(encoding=encoding, errors="replace")
    updated = content.replace(target, replacement)
    path.write_text(updated, encoding=encoding)
    return content.count(target)


def convert_encoding(source: Path, source_encoding: str, target: Path, target_encoding: str) -> None:
    data = source.read_text(encoding=source_encoding)
    ensure_parent_directory(target)
    target.write_text(data, encoding=target_encoding)


@dataclass
class TextAnalysis:
    characters: int
    words: int
    lines: int

    def format_report(self) -> str:
        return (
            f"Characters: {self.characters}\n"
            f"Words: {self.words}\n"
            f"Lines: {self.lines}\n"
        )


def analyze_text(path: Path, encoding: str) -> TextAnalysis:
    characters = 0
    words = 0
    lines = 0
    with path.open("r", encoding=encoding, errors="replace") as handle:
        for raw_line in handle:
            lines += 1
            stripped = raw_line.rstrip("\n")
            characters += len(stripped)
            words += len(stripped.split())
    return TextAnalysis(characters=characters, words=words, lines=lines)


def save_analysis(report_path: Path, analysis: TextAnalysis, encoding: str) -> None:
    ensure_parent_directory(report_path)
    report_path.write_text(analysis.format_report(), encoding=encoding)


def prompt_initial_content() -> str:
    print("Enter initial content. Submit an empty line to finish.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")


def prompt_append_text() -> str:
    print("Enter text to append. Submit an empty line to finish.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")


def handle_create() -> None:
    try:
        path = prompt_path("Enter path for new text file: ")
        encoding = ask_encoding()
        overwrite = False
        if path.exists():
            overwrite = input("File exists. Overwrite? [y/N]: ").strip().lower().startswith("y")
        initial_content = prompt_initial_content()
        create_text_file(path, encoding, initial_content, overwrite)
        print(f"File created at {path}")
    except Exception as exc:
        print(f"Error: {exc}")


def handle_display() -> None:
    try:
        path = prompt_path("Enter path to display: ")
        encoding = ask_encoding()
        if not path.exists():
            raise FileNotFoundError(path)
        display_file(path, encoding)
    except Exception as exc:
        print(f"Error: {exc}")


def handle_append() -> None:
    try:
        path = prompt_path("Enter path to append: ")
        encoding = ask_encoding()
        if not path.exists():
            raise FileNotFoundError(path)
        text = prompt_append_text()
        append_text(path, encoding, text)
        print("Text appended")
    except Exception as exc:
        print(f"Error: {exc}")


def handle_clear() -> None:
    try:
        path = prompt_path("Enter path to clear: ")
        if not path.exists():
            raise FileNotFoundError(path)
        if input("Confirm clearing file? This cannot be undone. [y/N]: ").strip().lower().startswith("y"):
            clear_file(path)
            print("File cleared")
        else:
            print("Cancelled")
    except Exception as exc:
        print(f"Error: {exc}")


def handle_find_replace() -> None:
    try:
        path = prompt_path("Enter path for find/replace: ")
        encoding = ask_encoding()
        if not path.exists():
            raise FileNotFoundError(path)
        target = input("Text to find: ")
        replacement = input("Replacement text: ")
        occurrences = find_and_replace(path, encoding, target, replacement)
        print(f"Replaced {occurrences} occurrence(s)")
    except Exception as exc:
        print(f"Error: {exc}")


def handle_convert() -> None:
    try:
        source = prompt_path("Enter source file path: ")
        if not source.exists():
            raise FileNotFoundError(source)
        source_encoding = ask_encoding("Enter source encoding (blank for utf-8): ")
        target = prompt_path("Enter destination file path: ")
        target_encoding = ask_encoding("Enter target encoding (blank for utf-8): ")
        convert_encoding(source, source_encoding, target, target_encoding)
        print(f"Saved converted file to {target}")
    except Exception as exc:
        print(f"Error: {exc}")


def handle_analysis() -> None:
    try:
        path = prompt_path("Enter path to analyze: ")
        encoding = ask_encoding()
        if not path.exists():
            raise FileNotFoundError(path)
        analysis = analyze_text(path, encoding)
        print(analysis.format_report())
        save_path_input = input("Enter path to save report (blank to skip): ").strip()
        if save_path_input:
            report_path = Path(save_path_input).expanduser().resolve()
            report_encoding = ask_encoding("Enter report encoding (blank for utf-8): ")
            save_analysis(report_path, analysis, report_encoding)
            print(f"Report saved to {report_path}")
    except Exception as exc:
        print(f"Error: {exc}")


def print_menu() -> None:
    print("\nText File Manager")
    print("1. Create new text file")
    print("2. Display file contents")
    print("3. Append text to file")
    print("4. Clear file contents")
    print("5. Find and replace text")
    print("6. Convert file encoding")
    print("7. Analyze text file")
    print("8. Exit")


def run_cli() -> None:
    handlers = {
        "1": handle_create,
        "2": handle_display,
        "3": handle_append,
        "4": handle_clear,
        "5": handle_find_replace,
        "6": handle_convert,
        "7": handle_analysis,
    }
    while True:
        print_menu()
        choice = input("Choose option: ").strip()
        if choice == "8":
            print("Goodbye")
            break
        handler = handlers.get(choice)
        if handler is None:
            print("Invalid option")
            continue
        handler()


class TextFileManagerGUI:
    """Tkinter interface that wraps backend operations."""

    def __init__(self, master: tk.Tk) -> None:
        self.root = master
        self.root.title("Менеджер текстовых файлов")
        self.root.geometry("900x600")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._init_create_tab()
        self._init_view_tab()
        self._init_append_tab()
        self._init_clear_tab()
        self._init_find_replace_tab()
        self._init_convert_tab()
        self._init_analyze_tab()

        self.analysis_result: TextAnalysis | None = None

    # ---- helpers ----
    def _file_error(self, exc: Exception) -> None:
        messagebox.showerror("Ошибка", str(exc))

    def _info(self, message: str) -> None:
        messagebox.showinfo("Успешно", message)

    def _ask_overwrite(self, path: Path) -> bool:
        return messagebox.askyesno("Перезапись", f"Файл {path} уже существует. Перезаписать?")

    def _ask_confirm(self, message: str) -> bool:
        return messagebox.askyesno("Подтверждение", message)

    def _encoding_or_default(self, value: str) -> str:
        return value.strip() or DEFAULT_ENCODING

    def _select_open_file(self, var: tk.StringVar) -> None:
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

    def _select_save_file(self, var: tk.StringVar) -> None:
        filename = filedialog.asksaveasfilename()
        if filename:
            var.set(filename)

    # ---- tabs ----
    def _init_create_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Создание файла")

        self.create_path_var = tk.StringVar()
        self.create_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)

        path_row = ttk.Frame(frame)
        path_row.pack(fill=tk.X, pady=4)
        ttk.Label(path_row, text="Путь к файлу:").pack(side=tk.LEFT)
        ttk.Entry(path_row, textvariable=self.create_path_var, width=80).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(path_row, text="Выбрать...", command=lambda: self._select_save_file(self.create_path_var)).pack(side=tk.LEFT)

        enc_row = ttk.Frame(frame)
        enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(enc_row, text="Кодировка:").pack(side=tk.LEFT)
        ttk.Entry(enc_row, textvariable=self.create_encoding_var, width=20).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame, text="Начальное содержимое:").pack(anchor=tk.W)
        self.create_text = scrolledtext.ScrolledText(frame, height=15, wrap=tk.WORD)
        self.create_text.pack(fill=tk.BOTH, expand=True, pady=4)

        ttk.Button(frame, text="Создать", command=self._handle_create_gui).pack(pady=6)

    def _init_view_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Просмотр файла")

        self.view_path_var = tk.StringVar()
        self.view_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)

        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Файл:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.view_path_var, width=80).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(row, text="Выбрать...", command=lambda: self._select_open_file(self.view_path_var)).pack(side=tk.LEFT)

        enc_row = ttk.Frame(frame)
        enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(enc_row, text="Кодировка:").pack(side=tk.LEFT)
        ttk.Entry(enc_row, textvariable=self.view_encoding_var, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Button(enc_row, text="Показать", command=self._handle_view).pack(side=tk.LEFT, padx=4)

        self.view_text = scrolledtext.ScrolledText(frame, height=20, wrap=tk.NONE)
        self.view_text.pack(fill=tk.BOTH, expand=True, pady=4)
        self.view_text.config(state=tk.DISABLED)

    def _init_append_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Добавление текста")

        self.append_path_var = tk.StringVar()
        self.append_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)

        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Файл:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.append_path_var, width=80).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(row, text="Выбрать...", command=lambda: self._select_open_file(self.append_path_var)).pack(side=tk.LEFT)

        enc_row = ttk.Frame(frame)
        enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(enc_row, text="Кодировка:").pack(side=tk.LEFT)
        ttk.Entry(enc_row, textvariable=self.append_encoding_var, width=20).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame, text="Текст для добавления:").pack(anchor=tk.W)
        self.append_text_widget = scrolledtext.ScrolledText(frame, height=12, wrap=tk.WORD)
        self.append_text_widget.pack(fill=tk.BOTH, expand=True, pady=4)

        ttk.Button(frame, text="Добавить", command=self._handle_append_gui).pack(pady=6)

    def _init_clear_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Очистка файла")

        self.clear_path_var = tk.StringVar()

        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Файл:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.clear_path_var, width=80).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(row, text="Выбрать...", command=lambda: self._select_open_file(self.clear_path_var)).pack(side=tk.LEFT)

        ttk.Button(frame, text="Очистить", command=self._handle_clear_gui).pack(pady=10)

    def _init_find_replace_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Поиск и замена")

        self.replace_path_var = tk.StringVar()
        self.replace_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)
        self.replace_target_var = tk.StringVar()
        self.replace_replacement_var = tk.StringVar()

        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Файл:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.replace_path_var, width=70).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(row, text="Выбрать...", command=lambda: self._select_open_file(self.replace_path_var)).pack(side=tk.LEFT)

        enc_row = ttk.Frame(frame)
        enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(enc_row, text="Кодировка:").pack(side=tk.LEFT)
        ttk.Entry(enc_row, textvariable=self.replace_encoding_var, width=20).pack(side=tk.LEFT, padx=4)

        target_row = ttk.Frame(frame)
        target_row.pack(fill=tk.X, pady=4)
        ttk.Label(target_row, text="Что найти:").pack(side=tk.LEFT)
        ttk.Entry(target_row, textvariable=self.replace_target_var, width=30).pack(side=tk.LEFT, padx=4)
        ttk.Label(target_row, text="Чем заменить:").pack(side=tk.LEFT)
        ttk.Entry(target_row, textvariable=self.replace_replacement_var, width=30).pack(side=tk.LEFT, padx=4)

        ttk.Button(frame, text="Заменить", command=self._handle_replace_gui).pack(pady=6)

    def _init_convert_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Конвертация кодировки")

        self.convert_source_var = tk.StringVar()
        self.convert_target_var = tk.StringVar()
        self.convert_source_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)
        self.convert_target_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)

        src_row = ttk.Frame(frame)
        src_row.pack(fill=tk.X, pady=4)
        ttk.Label(src_row, text="Исходный файл:").pack(side=tk.LEFT)
        ttk.Entry(src_row, textvariable=self.convert_source_var, width=70).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(src_row, text="Выбрать...", command=lambda: self._select_open_file(self.convert_source_var)).pack(side=tk.LEFT)

        src_enc_row = ttk.Frame(frame)
        src_enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(src_enc_row, text="Кодировка источника:").pack(side=tk.LEFT)
        ttk.Entry(src_enc_row, textvariable=self.convert_source_encoding_var, width=20).pack(side=tk.LEFT, padx=4)

        tgt_row = ttk.Frame(frame)
        tgt_row.pack(fill=tk.X, pady=4)
        ttk.Label(tgt_row, text="Целевой файл:").pack(side=tk.LEFT)
        ttk.Entry(tgt_row, textvariable=self.convert_target_var, width=70).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(tgt_row, text="Сохранить как...", command=lambda: self._select_save_file(self.convert_target_var)).pack(side=tk.LEFT)

        tgt_enc_row = ttk.Frame(frame)
        tgt_enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(tgt_enc_row, text="Кодировка назначения:").pack(side=tk.LEFT)
        ttk.Entry(tgt_enc_row, textvariable=self.convert_target_encoding_var, width=20).pack(side=tk.LEFT, padx=4)

        ttk.Button(frame, text="Конвертировать", command=self._handle_convert_gui).pack(pady=6)

    def _init_analyze_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Анализ текста")

        self.analysis_path_var = tk.StringVar()
        self.analysis_encoding_var = tk.StringVar(value=DEFAULT_ENCODING)

        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Файл:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.analysis_path_var, width=70).pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        ttk.Button(row, text="Выбрать...", command=lambda: self._select_open_file(self.analysis_path_var)).pack(side=tk.LEFT)

        enc_row = ttk.Frame(frame)
        enc_row.pack(fill=tk.X, pady=4)
        ttk.Label(enc_row, text="Кодировка:").pack(side=tk.LEFT)
        ttk.Entry(enc_row, textvariable=self.analysis_encoding_var, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Button(enc_row, text="Анализировать", command=self._handle_analyze_gui).pack(side=tk.LEFT, padx=4)

        self.analysis_text = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self.analysis_text, justify=tk.LEFT).pack(anchor=tk.W, pady=6)

        ttk.Button(frame, text="Сохранить отчет", command=self._handle_save_report_gui).pack(pady=6)

    # ---- event handlers ----
    def _handle_create_gui(self) -> None:
        try:
            path_value = self.create_path_var.get().strip()
            if not path_value:
                raise ValueError("Не выбран путь для создания файла")
            path = Path(path_value).expanduser().resolve()
            encoding = self._encoding_or_default(self.create_encoding_var.get())
            content = self.create_text.get("1.0", tk.END)
            if path.exists() and not self._ask_overwrite(path):
                return
            create_text_file(path, encoding, content, overwrite=True)
            self._info(f"Файл создан: {path}")
        except Exception as exc:
            self._file_error(exc)

    def _handle_view(self) -> None:
        try:
            path = Path(self.view_path_var.get().strip()).expanduser().resolve()
            encoding = self._encoding_or_default(self.view_encoding_var.get())
            if not path.exists():
                raise FileNotFoundError(path)
            lines = list(read_lines(path, encoding))
            self.view_text.config(state=tk.NORMAL)
            self.view_text.delete("1.0", tk.END)
            for idx, line in enumerate(lines, 1):
                self.view_text.insert(tk.END, f"{idx:6}: {line}\n")
            self.view_text.config(state=tk.DISABLED)
        except Exception as exc:
            self._file_error(exc)

    def _handle_append_gui(self) -> None:
        try:
            path = Path(self.append_path_var.get().strip()).expanduser().resolve()
            encoding = self._encoding_or_default(self.append_encoding_var.get())
            if not path.exists():
                raise FileNotFoundError(path)
            text_to_append = self.append_text_widget.get("1.0", tk.END)
            append_text(path, encoding, text_to_append)
            self._info("Текст добавлен")
        except Exception as exc:
            self._file_error(exc)

    def _handle_clear_gui(self) -> None:
        try:
            path = Path(self.clear_path_var.get().strip()).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(path)
            if not self._ask_confirm("Очистить выбранный файл? Операция необратима."):
                return
            clear_file(path)
            self._info("Файл очищен")
        except Exception as exc:
            self._file_error(exc)

    def _handle_replace_gui(self) -> None:
        try:
            path = Path(self.replace_path_var.get().strip()).expanduser().resolve()
            encoding = self._encoding_or_default(self.replace_encoding_var.get())
            target = self.replace_target_var.get()
            replacement = self.replace_replacement_var.get()
            if not path.exists():
                raise FileNotFoundError(path)
            if not target:
                raise ValueError("Строка для поиска не может быть пустой")
            occurrences = find_and_replace(path, encoding, target, replacement)
            self._info(f"Заменено вхождений: {occurrences}")
        except Exception as exc:
            self._file_error(exc)

    def _handle_convert_gui(self) -> None:
        try:
            source = Path(self.convert_source_var.get().strip()).expanduser().resolve()
            target = Path(self.convert_target_var.get().strip()).expanduser().resolve()
            if not source.exists():
                raise FileNotFoundError(source)
            source_encoding = self._encoding_or_default(self.convert_source_encoding_var.get())
            target_encoding = self._encoding_or_default(self.convert_target_encoding_var.get())
            if target.exists() and not self._ask_overwrite(target):
                return
            convert_encoding(source, source_encoding, target, target_encoding)
            self._info(f"Файл сохранен: {target}")
        except Exception as exc:
            self._file_error(exc)

    def _handle_analyze_gui(self) -> None:
        try:
            path = Path(self.analysis_path_var.get().strip()).expanduser().resolve()
            encoding = self._encoding_or_default(self.analysis_encoding_var.get())
            if not path.exists():
                raise FileNotFoundError(path)
            self.analysis_result = analyze_text(path, encoding)
            self.analysis_text.set(self.analysis_result.format_report())
        except Exception as exc:
            self.analysis_result = None
            self.analysis_text.set("")
            self._file_error(exc)

    def _handle_save_report_gui(self) -> None:
        if self.analysis_result is None:
            self._file_error(ValueError("Сначала выполните анализ"))
            return
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filename:
            return
        try:
            path = Path(filename).expanduser().resolve()
            encoding = self._encoding_or_default(self.analysis_encoding_var.get())
            save_analysis(path, self.analysis_result, encoding)
            self._info(f"Отчет сохранен: {path}")
        except Exception as exc:
            self._file_error(exc)


def run_gui() -> None:
    root = tk.Tk()
    TextFileManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        try:
            run_cli()
        except KeyboardInterrupt:
            print("\nInterrupted by user", file=sys.stderr)
            sys.exit(1)
    else:
        run_gui()
