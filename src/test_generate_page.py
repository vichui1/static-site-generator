import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
    # Heading h1
    ## Heading h2        
    """
        self.assertEqual(
            extract_title(md),
            "Heading h1"
        )

if __name__ == "__main__":
    unittest.main()