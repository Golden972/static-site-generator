import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_extract_title_multiline(self):
        title = extract_title("""
## Nav

[home](./home.html)
[about](./about.html)

# Title

some text here
""")

        self.assertEqual(title, "Title")

    def test_extract_title_multiple_headings(self):
        title = extract_title("""
# Primary Title

# Another heading on the page that shoudn't be extracted
""")
        self.assertEqual(title, "Primary Title")

    def test_extract_title_none(self):
        try:
            extract_title("no title to be found")
            self.fail("Exception should've been raised")
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
