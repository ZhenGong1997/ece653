import unittest


from .token_with_escape import token_with_escape
from .token_with_escape_mutant1 import token_with_escape_mutant1
from .token_with_escape_mutant2 import token_with_escape_mutant2
class CoverageTests(unittest.TestCase):
    def test_statement_coverage(self):
        """Add tests to achieve statement coverage (as many as needed)."""
        # YOUR CODE HERE
        # unit test for q2a
        input = 'have|^fun'
        result = token_with_escape(input)
        self.assertEquals(result, ['have', 'fun'])

        # unit test from mutant_1 shall pass
        input2 = 'one^|two^^'
        result2 = token_with_escape(input2)
        self.assertEquals(result2, ['one|two^'])

        # unit test from mutant_2 shall pass
        input3 = 'ece^|653|is|fun'
        result3 = token_with_escape(input3)
        self.assertEquals(result3, ['ece|653','is','fun'])
        pass

    def test_kill_mutant_1(self):
        """Kill mutant 1"""
        # YOUR CODE HERE

        # add unit test for q3c, it shall fail
        input2 = 'one^|^two^^'
        result2 = token_with_escape_mutant1(input2)
        self.assertEquals(result2, ['one|two^'])
        pass

    def test_kill_mutant_2(self):
        """Kill mutant 2"""
        # YOUR CODE HERE

        # add unit test for q3c, it shall fail
        input2 = 'ece^|653|is|fun'
        result2 = token_with_escape_mutant2(input2)
        self.assertEquals(result2, ['ece|653','is','fun'])
        pass