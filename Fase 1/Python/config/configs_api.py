import requests

class Api(object):
    def getDataAPI(self, url):
        send_url = url
        response = requests.request("GET", send_url)
        result = response.json()
        return result
