import unittest

from Lsystems.Lsystem import LSystem


# noinspection PyTypeChecker,SpellCheckingInspection
class TestLSystem(unittest.TestCase):
    def setUp(self):
        self.lsystem = LSystem()
    
    def test_rules_setter(self):
        # Positive test case: setting rules as a dictionary
        self.lsystem.rules = {"F": "FLFRRFLF"}
        self.assertEqual({"F": "FLFRRFLF"}, self.lsystem.rules)
        
        # Positive test case: setting rules as a string
        self.lsystem.rules = "F FLFRRFLF"
        self.assertEqual({"F": "FLFRRFLF"}, self.lsystem.rules)
        
        # Positive test case: setting rules as an iterable
        self.lsystem.rules = ["F FLFRRFLF", "L LF"]
        self.assertEqual({"F": "FLFRRFLF", "L": "LF"}, self.lsystem.rules)
        
        # Negative test case: setting rules with invalid type
        with self.assertRaises(TypeError):
            self.lsystem.rules = 123
    
    def test_keywords_setter(self):
        self.lsystem.keywords = ["F", "B", "L", "R"]
        self.assertEqual((('F',), ('B',), ('L',), ('R',)), self.lsystem.keywords)
        
        self.lsystem.keywords = (("F", "Forward"), ["B", "Back"], ("L", "Left"), ["R", "Right"])
        self.assertEqual((('F', 'Forward'), ('B', 'Back'), ('L', 'Left'), ('R', 'Right')), self.lsystem.keywords)
        
        with self.assertRaises(TypeError):
            self.lsystem.keywords = 123
    
    def test_generate_action_string(self):
        self.lsystem = LSystem({"F": "FLFRRFLF"}, [("F", "forward"), ("B", "back")])
        
        # Positive test case: generating action string with string input
        result = self.lsystem.generate_action_string('F', 1)
        self.assertEqual(
                (
                    ('F', 1),
                    ('F', 1),
                    ('F', 1),
                    ('F', 1)),
                result
        )
        
        # Negative test case: generating action string with invalid number of iterations
        self.lsystem = LSystem({"F": "FLFRRFLF"}, (("F", "forward"), ("B", "back")))
        with self.assertRaises(OverflowError):
            self.lsystem.generate_action_string('F', 100)
    
    def test_formatting(self):
        self.lsystem.keywords = ["F", "B", "L", "R"]
        
        # Positive test case: formatting string with keywords
        result = tuple(self.lsystem.formatting("FFBLLRF"))
        self.assertEqual(
                (
                    ("F", 2),
                    ("B", 1),
                    ("L", 2),
                    ("R", 1),
                    ("F", 1)
                ),
                result
        )
        
        # Negative test case: formatting string with invalid input
        with self.assertRaises(TypeError):
            self.lsystem.formatting(123)
    
    def test_multiplication(self):
        self.lsystem.keywords = ["F", "B", "L", "R"]
        
        # Positive test case: multiplying string with keywords
        result = self.lsystem.multiplication("F(3)B(2)L(4)R(1)")
        self.assertEqual("FFFBBLLLLR", result)
        
        # Negative test case: multiplying string with invalid input
        with self.assertRaises(TypeError):
            self.lsystem.multiplication(123)


if __name__ == "__main__":
    unittest.main()
