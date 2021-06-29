import json
from tornado.web import RequestHandler



class MainHandler(RequestHandler):

    def post(self):
        payload = json.loads(self.request.body)
        return self.write(payload)
