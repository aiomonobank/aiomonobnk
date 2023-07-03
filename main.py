import asyncio
from datetime import datetime, timedelta

from mbnk.asyncio import AsyncMonoPay
from mbnk import MonoPay, Monobank
from mbnk.exceptions import *


async def main():
    api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"

    async_monopay = AsyncMonoPay(
        api_token=api_token
    )

    response = await async_monopay.invoice.create()

    print(response)

    sync_version()


def sync_version():
    api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"
    monobank = Monobank(
        api_token=api_token
    )
    try:
        currencies = monobank.public.currency()
        print(currencies)
    except TooManyRequestsException:
        print(TooManyRequestsException.error_description)

    # monopay = MonoPay(
    #     api_token=api_token
    # )
    #
    # response = monopay.invoice.create(amount=100)

    # print(response)


if __name__ == "__main__":
    asyncio.run(main())


