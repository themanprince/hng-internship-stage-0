import pytest

import sys
from os.path import abspath, join, dirname

sys.path.append(abspath(join(dirname("__file__"), "..")))

from facts_api_adapter import FactsAPIAdapter

def test_get_fact():
	fact = (FactsAPIAdapter()).getFact()
	
	assert len(fact) > 0