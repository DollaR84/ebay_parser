import json
import logging

from aiohttp import ClientSession

from bs4 import BeautifulSoup

from schemas import Product


class EbayClient:

    def __init__(self, item_id: str, params: dict[str, str]):
        self.base_url: str = "https://www.ebay.com"

        self.item_id: str = item_id
        self.params: dict[str, str] = params

    def make_url(self, item_id: str, params: dict[str, str]) -> str:
        url = "/".join([self.base_url, "itm", item_id])
        return "?".join([
            url, "&".join([
                f"{key}={value}"
                for key, value in params.items()
            ])
        ])

    async def get_data(self) -> dict:
        async with ClientSession() as session:
            try:
                return await self.get(session, self.make_url(self.item_id, self.params))

            except Exception as error:
                logging.error(error, exc_info=True)

    async def get(self, session: ClientSession, url: str) -> dict:
        async with session.get(url) as response:
            content = await response.text()
            return self.parse(url, content)

    def parse(self, url: str, content: str) -> dict:
        result = {}
        product = None

        bs = BeautifulSoup(content, "html.parser")
        seller_tag = bs.find("div", class_="x-sellercard-atf__info__about-seller")
        delivery_tag = bs.find("div", class_="ux-labels-values--deliverto")
        for span_tag in delivery_tag.find_all("span", class_="ux-textspans"):
            if "delivery" in span_tag.text.lower():
                continue
            delivery = span_tag.text

        json_tags = bs.find_all("script", type="application/ld+json")
        for json_tag in json_tags:
            data = json.loads(json_tag.text)

            data_type = data.get("@type")
            if not data_type or data_type != "Product":
                continue

            offers = data.get("offers")
            if not offers:
                continue

            brand = data.get("brand")
            product = Product(
                name=data.get("name"),
                image=data.get("image"),
                url=url,
                delivery=delivery,
                seller=seller_tag.get("title"),
                currency=offers.get("priceCurrency"),
                price=offers.get("price"),
                model=data.get("model"),
                brand=brand.get("name") if brand else None,
            )

        if product:
            result = product.dict(exclude_unset=True)
        return result
