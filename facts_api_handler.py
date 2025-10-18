from fastapi import HTTPException
from httpx import AsyncClient, TimeoutException, RequestError
from dotenv import dotenv_values

handler_instance_created = False

class FactsAPIHandler(object):
	def __init__(self):
		global handler_instance_created
		
		if handler_instance_created: #singleton
			raise HTTPException(500, detail="instance of FactsAPIHandler already exists")
		
		handler_instance_created = True
		
	
	async def get_fact(self):
		timeout = (dotenv_values(".env"))["API_QUERY_TIMEOUT"]
		timeout = float(timeout) or 3
		
		async with AsyncClient(timeout=timeout) as client:
			try:
				response = await client.get("https://catfact.ninja/fact")
				response.raise_for_status()
				response = response.json()
				return response["fact"]
			
			except TimeoutException:
				raise HTTPException(500, detail="Sorry. The Request Timed Out!")
				
			except RequestError:
				raise HTTPException(500, detail="unable to reach API")


facts_api_handler = FactsAPIHandler()