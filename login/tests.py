from FunDoo.fundoo.fundoo.settings import BASE_URL
import json
import requests

with open("Test.json") as f:
    data = json.load(f)


class TestReg:
    def test_reg1(self):
        url = BASE_URL + '/registration/'
        file = data[0]['Test_case1']
        response = requests.post(url=url, data=file)
        assert response.status_code == 400


class Testlogin:
    def test_log1(self):
        url = BASE_URL + '/login/'
        file = data[0]['Test_case2']

        response = requests.post(url=url, data=file)
        assert response.status_code == 400


if __name__ == '__main__':
    TestReg()
    Testlogin()
