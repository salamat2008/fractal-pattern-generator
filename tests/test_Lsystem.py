"""

"""
import unittest

from Lsystems.Lsystem import LSystem


# noinspection PyTypeChecker,SpellCheckingInspection
class TestLSystem(unittest.TestCase):
    def test_rules_setter(self):
        # Positive test case: setting rules as a dictionary
        lsystem = LSystem()
        lsystem.rules = {"F": "FLFRRFLF"}
        self.assertEqual(lsystem.rules, {"F": "FLFRRFLF"})
        
        # Positive test case: setting rules as a string
        lsystem.rules = "F FLFRRFLF"
        self.assertEqual(lsystem.rules, {"F": "FLFRRFLF"})
        
        # Positive test case: setting rules as an iterable
        lsystem.rules = ["F FLFRRFLF", "L LF"]
        self.assertEqual(lsystem.rules, {"F": "FLFRRFLF", "L": "LF"})
        
        # Negative test case: setting rules with invalid type
        lsystem = LSystem()
        with self.assertRaises(TypeError):
            lsystem.rules = 123
    
    def test_keywords_setter(self):
        # Positive test case: setting keywords as a list of strings
        lsystem = LSystem()
        lsystem.keywords = ["F", "B", "L", "R"]
        self.assertEqual(lsystem.keywords, [["F"], ["B"], ["L"], ["R"]])
        
        # Positive test case: setting keywords as a list of lists
        lsystem.keywords = [["F", "Forward"], ["B", "Back"], ["L", "Left"], ["R", "Right"]]
        self.assertEqual(lsystem.keywords, [["F", "Forward"], ["B", "Back"], ["L", "Left"], ["R", "Right"]])
        
        # Negative test case: setting keywords with invalid type
        lsystem = LSystem()
        with self.assertRaises(TypeError):
            lsystem.keywords = 123
    
    def test_generate_action_string(self):
        lsystem = LSystem({"F": "FLFRRFLF"}, [("F", "forward"), ("B", "back")])
        
        # Positive test case: generating action string with string input
        result = lsystem.generate_action_string('F', 1)
        self.assertEqual(
                result,
                (
                    ('F', 1),
                    ('F', 1),
                    ('F', 1),
                    ('F', 1))
        )
        
        # Negative test case: generating action string with invalid number of iterations
        lsystem = LSystem({"F": "FLFRRFLF"}, (("F", "forward"), ("B", "back")))
        with self.assertRaises(OverflowError):
            lsystem.generate_action_string('F', 1000000)
    
    def test_formatting(self):
        lsystem = LSystem()
        lsystem.keywords = ["F", "B", "L", "R"]
        
        # Positive test case: formatting string with keywords
        result = lsystem.formatting("FFBLLRF")
        self.assertEqual(
                tuple(result),
                (
                    ("F", 2),
                    ("B", 1),
                    ("L", 2),
                    ("R", 1),
                    ("F", 1))
        )
        
        # Negative test case: formatting string with invalid input
        lsystem = LSystem()
        with self.assertRaises(TypeError):
            lsystem.formatting(123)
    
    def test_multiplication(self):
        lsystem = LSystem()
        lsystem.keywords = ["F", "B", "L", "R"]
        
        # Positive test case: multiplying string with keywords
        result = lsystem.multiplication("F(3)B(2)L(4)R(1)")
        self.assertEqual(result, "FFFBBLLLLR")
        
        # Negative test case: multiplying string with invalid input
        lsystem = LSystem()
        with self.assertRaises(TypeError):
            lsystem.multiplication(123)


if __name__ == "__main__":
    unittest.main()
