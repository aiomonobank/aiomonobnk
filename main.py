import asyncio
from datetime import datetime, timedelta

from mbnk.asyncio import AsyncMonoPay


async def main():
    api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"

    async_monopay = AsyncMonoPay(
        api_token=api_token
    )

    response = await async_monopay.wallet.delete_card(card_token="sad")

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
