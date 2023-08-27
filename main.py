import asyncio

from aiomonobnk import MonoPay
from aiomonobnk.enums import CurrencyCode, PaymentType
from aiomonobnk.types import SaveCardData, MerchantPaymInfo, Product
from datetime import datetime, timedelta


async def main():
    async with MonoPay(
            token='mGjKtE5GZHyGt7YxfRlAeaw'
    ) as client:
        invoice = await client.create_invoice(
            amount=1000,
            ccy=CurrencyCode.USD,
            payment_type=PaymentType.DEBIT,
            merchant_paym_info=MerchantPaymInfo(
                reference='1',
                destination='distination of payment',
                comment='this is comment',
                basket_order=[
                    Product(
                        name='Product',
                        qty=1,
                        sum=100,
                        code='1'
                    )
                ]
            )
        )
        print(invoice)
        statement = await client.merchant_statement(from_=int((datetime.utcnow() - timedelta(days=29)).timestamp()))

if __name__ == '__main__':
    asyncio.run(main())
