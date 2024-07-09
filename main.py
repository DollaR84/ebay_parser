import asyncio
import json

from client import EbayClient


def file_output(product_id: str, data: dict):
    with open(f"product_{product_id}.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=3)


async def main():
    product_id: str = "315453956000"
    params: dict[str, str] = {
        "itmmeta": "01J2CC51XXQ4B15AT2RTKBF9K6",
        "hash": "item4972855fa0:g:QLcAAOSweKlmc5jT",
        "var": "613950082992",
    }

    ebay = EbayClient(product_id, params)
    data = await ebay.get_data()
    file_output(product_id, data)


if "__main__" == __name__:
    asyncio.run(main())
