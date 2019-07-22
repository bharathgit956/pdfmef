import unittest
import src.extraction.runnables as runnables
import src.extraction.test.filters as filters
import src.extraction.test.extractors as extractors
import xmltodict


class TestRunnables(unittest.TestCase):
   def setUp(self):
      pass

   def test_defining_dependencies(self):
      self.assertTrue(hasattr(filters.FilterWithoutDeps, 'dependencies'))
      self.assertEqual(len(filters.FilterWithoutDeps.dependencies), 0)
      self.assertEqual(len(filters.FilterWithDeps.dependencies), 1)
      self.assertTrue(filters.FilterWithoutDeps in filters.FilterWithDeps.dependencies)

      

      
