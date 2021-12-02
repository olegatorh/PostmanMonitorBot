import json
from datetime import datetime
import requests
from requests.structures import CaseInsensitiveDict

X_API_Key = "PMAK-61631c0813c1f600469840e2-8d247191c8233a0186aca827592c5de44a"  # postman login id
uid = "12824584-1ec25c6a-f11b-4b90-b36e-b6b229cf216c"  # postman monitor uid
url = "https://api.getpostman.com/monitors" + f"/{uid}/run"  # postman monitor run

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json,"
headers["X-API-Key"] = X_API_Key
headers["Authorization"] = "Bearer {token}"
headers["Content-Type"] = ""
headers["Content-Length"] = "0"


def run_monitor():
    try:
        json_data = (requests.post(url, headers=headers, timeout=220)).json()
        print(json_data)
        return json_data
    except Exception as e:
        print(e)
        return None


class ShortInfo:
    def __init__(self, name, status, total_func, failed_func, total_test, failed_test, started, finished, failures):
        self.name = name
        self.status = status
        self.total_func = total_func
        self.failed_func = failed_func
        self.failed_func = failed_func
        self.total_test = total_test
        self.failed_test = failed_test
        self.monitor_executingTime = datetime.strptime(finished[:19], "%Y-%m-%dT%H:%M:%S") - datetime.strptime(
            started[:19], "%Y-%m-%dT%H:%M:%S")
        self.failures = failures

    def answer(self, full_info, errors):
        if errors == 0:
            if full_info == 0:
                if self.status == "success":
                    return f"\n Monitor name: {self.name}. " \
                           f"\n Monitor status: {self.status}." \
                           f"\n Total functions: {self.total_func}." \
                           f"\n Failed functions: {self.failed_func}." \
                           f"\n Total tests: {self.total_test}." \
                           f"\n Failed tests: {self.failed_test}." \
                           f"\n Monitor status: {self.status}." \
                           f"\n Time: {self.monitor_executingTime} sec."

                else:
                    return (f"\n Monitor name: {self.name}. "
                            f"\n Monitor status: {self.status}."
                            f"\n Total functions: {self.total_func}."
                            f"\n Failed functions: {self.failed_func}."
                            f"\n Total tests: {self.total_test}."
                            f"\n Failed tests: {self.failed_test}."
                            f"\n Time: {self.monitor_executingTime} sec."
                            f"\n \n Houston we have a problem!"
                            f"\n failures {self.failures}" if len(self.failures) > 0 else "")

            else:
                return "ше не дороблено!"
        else:
            if full_info == 0:
                return (f"\n Monitor name: {self.name}. "
                        f"\n Monitor status: {self.status}."
                        f"\n Total functions: {self.total_func}."
                        f"\n Failed functions: {self.failed_func}."
                        f"\n Total tests: {self.total_test}."
                        f"\n Failed tests: {self.failed_test}."
                        f"\n Time: {self.monitor_executingTime} sec."
                        f"\n \n Houston we have a problem!"
                        f"\n failures {self.failures}" if len(self.failures) > 0 else "")
            else:
                print("ше не дороблено!")


def return_data(json_data, user):
    return (ShortInfo(json_data['run']["info"]["name"],
                      json_data['run']["info"]["status"],
                      json_data['run']["stats"]["requests"]["total"],
                      json_data['run']["stats"]["requests"]["failed"],
                      json_data['run']["stats"]["assertions"]["total"],
                      json_data['run']["stats"]["assertions"]["failed"],
                      json_data['run']["info"]["startedAt"],
                      json_data['run']["info"]["finishedAt"],
                      json_data['run']["failures"]).answer(user[6], user[5]))
