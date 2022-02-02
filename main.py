from aiogram import executor
from create_bot import dp


# class ApiParameters:
#     def init(self, username, password, api_url):
#         self.username = username
#         self.password = password
#         self.api_url = api_url
#         self.token = self.auth()
#
#     def auth(self):
#         response = requests.post(
#             f'{self.api_url}/auth',
#             data=f'''{{ "username": "{self.username}", "password": "{self.password}" }}''')
#         print(f'Username": {self.username}; \nAuth token - {response.json()["result"]["token"]};')
#         return response.json()["result"]["token"]
#
#
# open_api = ApiParameters("oleg", "1488", "https://api.meest.com/v3.0/openAPI")
#
#
# def api_call(api_parameters, func_name, function_type, body=None, params=None):
#     if params is None:
#         params = {}
#     response = {
#         "post": (requests.post(f'{api_parameters.api_url}/{func_name}',
#                              headers={'token': f'{api_parameters.token}'},
#                              params=params,
#                              data=body)),
#         "get": (requests.get(f'{api_parameters.api_url}/{func_name}',
#                              headers={'token': f'{api_parameters.token}'},
#                              params=params,
#                              data=body)),
#         "put": (requests.put(f'{api_parameters.api_url}/{func_name}',
#                              headers={'token': f'{api_parameters.token}'},
#                              params=params,
#                              data=body)),
#         "delete": (requests.delete(f'{api_parameters.api_url}/{func_name}',
#                              headers={'token': f'{api_parameters.token}'},
#                              params=params,
#                              data=body))
#     }
#     response = response[function_type]
#     print(f"\nfunction Name:\n{func_name}\nResponse:\n{response.json()}\n")
#     return response.status_code, response.elapsed.total_seconds(), response.json()


async def on_startup(_):
    print("bot is running")


from handlers import api_handlers, other_handlers, users_handlers

api_handlers.register_handlers_api(dp)
other_handlers.register_handlers_others(dp)
users_handlers.register_handlers_users(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
