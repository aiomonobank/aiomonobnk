import asyncio

from aiomonobnk import MonoPay
from aiomonobnk.enums import CurrencyCode, PaymentType
from aiomonobnk.types import SaveCardData
from datetime import datetime, timedelta


async def main():
    async with MonoPay(
            token='uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc'
    ) as client:
        invoice = await client.create_invoice(
            amount=1000,
            ccy=CurrencyCode.USD,
            payment_type=PaymentType.DEBIT,
            save_card_data=SaveCardData(
                save_card=True
            )
        )
        statement = await client.merchant_statement(from_=int((datetime.utcnow() - timedelta(days=29)).timestamp()))

if __name__ == '__main__':
    asyncio.run(main())
