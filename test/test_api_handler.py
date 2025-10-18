import pytest

import sys
from os.path import abspath, join, dirname

sys.path.append(abspath(join(dirname("__file__"), "..")))

from facts_api_handler import facts_api_handler

async def test_get_fact():
	fact = await facts_api_handler.getFact()
	
	assert len(fact) > 0