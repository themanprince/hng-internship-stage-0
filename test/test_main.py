import pytest

import sys
from os.path import abspath, join, dirname

sys.path.append(abspath(join(dirname("__file__"), "..")))


from fastapi.testclient import TestClient
from main import app
import re

client = TestClient(app)


def all_in(dictObj, **list_of_keys):
	for key in list_of_keys:
		if (key not in dictObj) or (not dictObj[key]):
			return False
	return True


def test_main():
	response = client.get("/me")
	assert response.status_code == 200
	assert response.headers["Content-Type"] == "application/json"
	
	body = response.json()
	assert all_in(body, "status", "user", "timestamp", "fact")
	
	assert body["status"] == "success"
	assert all_in(body["user"], "email", "name", "stack")
	EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
	assert EMAIL_RE.fullmatch(body["user"]["email"])
	
	timestamp1 = body["timestamp"]
	
	response2 = client.get("/me")
	timestamp2 = response2.json()["timestamp"]
	assert timestamp1 != timestamp2