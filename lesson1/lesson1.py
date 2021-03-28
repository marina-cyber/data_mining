# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }

from pathlib import Path
import requests

class Parse5kaProducts:
    def __init__(self, cat_url: str, category: str):
        self.cat_url = cat_url
        self.params = {
            'store': None,
            'records_per_page': 30,
            'page': 1,
            'categories': category,
            'ordering': None,
            'price_promo__gte': None,
            'price_promo__lte': None,
            'search': None
             }

    def parse(self) -> dict:
        products = requests.get(self.cat_url, params=self.params).json()
        return products['results']


class Parse5kaCategories:
    def __init__(self, cat_url, prod_url, result_path: Path):
        self.cat_url = cat_url
        self.prod_url = prod_url
        self.result_path = result_path
        self.categories = None

    def _run(self):
        req = requests.get(self.cat_url)
        self.categories = req.json()
        self._save()

    def _save(self):
        if not self.result_path.exists():
            self.result_path.mkdir()

        for cat in self.categories:
            seq = [f"name: {cat['parent_group_name']}\n", f"code: {cat['parent_group_code']}\n"]
            products = Parse5kaProducts(self.prod_url,cat['parent_group_code']).parse()
            with open(self.result_path.joinpath(f"{cat['parent_group_name']}.json"), 'w+', encoding='utf8') as file:
                file.writelines(seq)
                file.write('Products:\n')
                for product in products:
                    file.write(product.__str__() +'\n')


cat_url = 'https://5ka.ru/api/v2/categories/'
prod_url='https://5ka.ru/api/v2/special_offers'

cat = Parse5kaCategories(cat_url, prod_url, Path(__file__).parent.joinpath('categories/'))
cat._run()
