from django.test import SimpleTestCase, TestCase

class NodbTests(SimpleTestCase):

    def test_no_args(self):
        response = self.client.get('/item-price-service/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": 404, "content": {"message": "Not found"}})

    def test_no_item(self):
        response = self.client.get('/item-price-service/?city=Philadelphia')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": 404, "content": {"message": "Not found"}})


class UsingDbTests(TestCase):

    fixtures = ['test_data.json', ]

    def test_item_not_found(self):
        response = self.client.get('/item-price-service/?item=brandonsshoes')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": 404, "content": {"message": "Not found"}})

    def test_city_not_specified(self):
        response = self.client.get('/item-price-service/?item=ps4')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
            {"status": 200,
             "content":
                 {"item": "ps4", "city": "Not specified", "price_suggestion": 43, "item_count": 861}}
            )
    def test_unique(self):
        response = self.client.get('/item-price-service/?item=Furniture&city=Philadelphia')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
            {"status": 200,
             "content":
                 {"item": "Furniture", "city": "Philadelphia", "price_suggestion": 24, "item_count": 53}})
