import asyncio
from datetime import datetime, timedelta

from mbnk.asyncio import AsyncMonoPay
from mbnk import MonoPay, Monobank


async def main():
    api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"

    async_monopay = AsyncMonoPay(
        api_token=api_token
    )

    response = await async_monopay.merchant.details()

    print("response async:", response)

    sync_version()


def sync_version():
    api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"
    monobank = Monobank(
        api_token=api_token
    )
    currencies = monobank.personal.info()

    print(currencies)


if __name__ == "__main__":
    asyncio.run(main())


