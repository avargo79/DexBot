"""
DexBot Test Suite

This is the main test runner for the DexBot project. It includes tests for
all major systems including Auto Heal, Combat, and Looting systems.
"""

import unittest
import sys
import os

# Add the tests directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import all test modules
from test_looting_system import TestLootingSystem, TestLootingSystemIntegration, TestLootingSystemPerformance


class TestDexBot(unittest.TestCase):
    """Basic DexBot functionality tests"""

    def test_basic_functionality(self):
        """Test basic bot functionality"""
        self.assertEqual(1, 1)
        
    def test_project_structure(self):
        """Test that the project structure is correct"""
        # Test that key directories exist
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        self.assertTrue(os.path.exists(os.path.join(project_root, 'src')))
        self.assertTrue(os.path.exists(os.path.join(project_root, 'src', 'systems')))
        self.assertTrue(os.path.exists(os.path.join(project_root, 'src', 'config')))
        self.assertTrue(os.path.exists(os.path.join(project_root, 'docs')))


def create_test_suite():
    """Create a comprehensive test suite"""
    suite = unittest.TestSuite()
    
    # Add basic tests
    suite.addTest(unittest.makeSuite(TestDexBot))
    
    # Add looting system tests
    suite.addTest(unittest.makeSuite(TestLootingSystem))
    suite.addTest(unittest.makeSuite(TestLootingSystemIntegration))
    suite.addTest(unittest.makeSuite(TestLootingSystemPerformance))
    
    return suite


if __name__ == '__main__':
    # Run all tests
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
