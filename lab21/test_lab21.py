import io
import os
import tempfile
import unittest
from pathlib import Path

from lab21 import (
    DEFAULT_ENCODING,
    TextAnalysis,
    analyze_text,
    append_text,
    clear_file,
    convert_encoding,
    create_text_file,
    find_and_replace,
    save_analysis,
)


class TextFileManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base = Path(self.temp_dir.name)

    def test_create_text_file_with_initial_content(self) -> None:
        path = self.base / "sample.txt"
        create_text_file(path, DEFAULT_ENCODING, "hello\n", overwrite=False)
        self.assertTrue(path.exists())
        self.assertEqual(path.read_text(encoding=DEFAULT_ENCODING), "hello\n")

    def test_append_text_appends_content(self) -> None:
        path = self.base / "append.txt"
        create_text_file(path, DEFAULT_ENCODING, "one\n", overwrite=False)
        append_text(path, DEFAULT_ENCODING, "two\n")
        self.assertEqual(path.read_text(encoding=DEFAULT_ENCODING), "one\ntwo\n")

    def test_clear_file_empties_content(self) -> None:
        path = self.base / "clear.txt"
        create_text_file(path, DEFAULT_ENCODING, "data\n", overwrite=True)
        clear_file(path)
        self.assertEqual(path.read_text(encoding=DEFAULT_ENCODING), "")

    def test_find_and_replace_counts_occurrences(self) -> None:
        path = self.base / "replace.txt"
        create_text_file(path, DEFAULT_ENCODING, "aa bb aa\n", overwrite=False)
        replaced = find_and_replace(path, DEFAULT_ENCODING, "aa", "xx")
        self.assertEqual(replaced, 2)
        self.assertEqual(path.read_text(encoding=DEFAULT_ENCODING), "xx bb xx\n")

    def test_convert_encoding_creates_target_file(self) -> None:
        source = self.base / "source.txt"
        target = self.base / "target.txt"
        create_text_file(source, DEFAULT_ENCODING, "тест\n", overwrite=False)
        convert_encoding(source, DEFAULT_ENCODING, target, "cp1251")
        self.assertTrue(target.exists())
        self.assertEqual(target.read_text(encoding="cp1251"), "тест\n")

    def test_analyze_text_counts(self) -> None:
        path = self.base / "analyze.txt"
        create_text_file(path, DEFAULT_ENCODING, "one two\nthree\n", overwrite=False)
        analysis = analyze_text(path, DEFAULT_ENCODING)
        self.assertEqual(analysis.characters, len("one two") + len("three"))
        self.assertEqual(analysis.words, 3)
        self.assertEqual(analysis.lines, 2)

    def test_save_analysis_writes_report(self) -> None:
        report = self.base / "report.txt"
        analysis = TextAnalysis(characters=5, words=2, lines=1)
        save_analysis(report, analysis, DEFAULT_ENCODING)
        self.assertEqual(
            report.read_text(encoding=DEFAULT_ENCODING),
            "Characters: 5\nWords: 2\nLines: 1\n",
        )


if __name__ == "__main__":
    unittest.main()
