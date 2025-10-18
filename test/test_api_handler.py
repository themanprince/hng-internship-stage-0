import pytest

import sys
from os.path import abspath, join, dirname

sys.path.append(abspath(join(dirname("__file__"), "..")))

from facts_api_handler import facts_api_handler

@pytest.mark.asyncio
async def test_get_fact():
	fact = await facts_api_handler.get_fact()
	
	assert len(fact) > 0