from src.extraction.runnables import Extractor, RunnableError, ExtractorResult
import src.extraction.utils
import src.extractor.csxextract.interfaces as interfaces
import src.extractor.csxextract.config as config
import src.extractor.csxextract.filters as filters
import src.extractor.csxextract.utils as utils
import subprocess32 as subprocess
import subprocess
import defusedxml.ElementTree as safeET
import xml.etree.ElementTree as ET
import os
import tempfile
import requests
import re
import shutil
import glob


# Returns a plain text version of a PDF file
class PDFFigures2Extractor(Extractor):
   dependencies = frozenset([filters.AcademicPaperFilter])
   result_file_name = '.figures'

   def extract(self, data, dependency_results):
      file_path = src.extraction.utils.temp_file(data, suffix='.pdf')
      results_dir = tempfile.mkdtemp() + '/'

      try:
         command_args = ['java', '-jar', config.PDFFIGURES2_JAR, file_path, '-m', results_dir, '-d', results_dir]
         status, stdout, stderr = src.extraction.utils.external_process(command_args, timeout=30)
      except subprocess.TimeoutExpired:
	 shutil.rmtree(results_dir)
         raise RunnableError('PDFFigures2 timed out while processing document')
      finally:
         os.remove(file_path)

      if status != 0:
         raise RunnableError('PDFFigures22 Failure. Possible error:\n' + stderr)

      # Handle png results
      files = {}
      for path in glob.glob(results_dir + '*.png'):
         # basename looks something like this: -Figure-X.png
         # remove the hyphen and replace with a '.', because framework will add filename prefix later
         filename = '.' + os.path.basename(path)[1:]
         with open(path, 'rb') as f:
            files[filename] = f.read()

      # Handle json results
      for path in glob.glob(results_dir + '*.json'):
         filename = '.' + os.path.basename(path)[1:]
         with open(path, 'r') as f:
            files[filename] = f.read()

      shutil.rmtree(results_dir)

      return ExtractorResult(xml_result=None, files=files)
