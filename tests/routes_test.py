from nestor import create_app
import json


class TestRoutes():

    def setUp(self):
        app = create_app(testing=True)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_ping(self):
        r = self.app.get('/ping')
        payload = json.loads(r.get_data(as_text=True))
        assert(payload['ping'])
