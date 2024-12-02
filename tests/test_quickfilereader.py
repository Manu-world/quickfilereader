import unittest
from quickfilereader import read_txt

class TestQuickFileReader(unittest.TestCase):
    def test_read_file_success(self):
        with open("sample.txt", 'w') as f:
            f.write("hey Python!")
        content = read_txt("sample.txt")
        self.assertEqual(content, "hey Python!")
        
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_txt("nonexistent,.txt")
            

if __name__=="__main__":
    unittest.main()