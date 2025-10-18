from fastapi import HTTPException
from httpx import AsyncClient, TimeoutException, RequestError
from dotenv import dotenv_values

handler_instance_created = False

class FactsAPIHandler(object):
	def __init__(self):
		if handler_instance_created: #singleton
			raise HTTPException(500, detail="instance of FactsAPIHandler already exists")
		
		handler_instance_created = True
		
	
	async def get_fact(self):
		timeout = (dotenv_values(".env"))["API_QUERY_TIMEOUT"]
		timeout = int(timeout)
		
		async with AsyncClient(timeout=timeout) as client:
			try:
				response = await client.get("https://catfact.ninja/fact")
				return response.json()
			
			except TimeoutException as timeout_exception:
				return {
					"error": "Sorry. The Request Timed Out! Please try again"
				}
				
			except RequestError as request_error:
				return {
					"error": request_error
				}


facts_api_handler = FactsAPIHandler()