import os
import pytest

from dotenv import load_dotenv

from aiomonobnk import MonoAcquiringAPI
from aiomonobnk.asyncio import AsyncMonoAcquiringAPI

from aiomonobnk.types import *
from aiomonobnk.responses import *

load_dotenv(dotenv_path=os.path.abspath('.env'))


# Invoices

# Invoice create: synchronous
# def test_invoice_create_sync():
#     mono = MonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = mono.invoice.create(amount=100)
#
#     assert isinstance(invoice, InvoiceCreatedResponse)


# Invoice create: asynchronous
@pytest.mark.asyncio
async def test_invoice_create_async():
    mono = AsyncMonoAcquiringAPI(
        api_token=os.getenv("TEST_MONOBANK_API_TOKEN")
    )

    merchant_paym_info = MerchantPaymInfo(
        reference="1234",
        destination="Призначення",
        basket_order=[
            Product(
                name=f"name_{1}",
                qty=1,
                sum=100
            )
        ]
    )

    invoice = await mono.invoice.create(
        amount=100,
        merchant_paym_info=merchant_paym_info
    )

    print(invoice)
    assert isinstance(invoice, InvoiceCreated)


# Invoice status: synchronous
# def test_invoice_status_sync():
#     mono = MonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = mono.invoice.create(amount=100)
#
#     status = mono.invoice.status(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
#
#
# Invoice status: asynchronous
# @pytest.mark.asyncio
# async def test_invoice_status_async():
#     mono = AsyncMonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = await mono.invoice.create(amount=100)
#
#     status = await mono.invoice.status(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
#
#
# # Invoice cancel: synchronous
# def test_invoice_cancel_sync():
#     mono = MonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = mono.invoice.create(amount=100)
#
#     status = mono.invoice.cancel(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
#
#
# # Invoice cancel: asynchronous
# @pytest.mark.asyncio
# async def test_invoice_cancel_async():
#     mono = AsyncMonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = await mono.invoice.create(amount=100)
#
#     status = await mono.invoice.cancel(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
#
#
# # Invoice info: synchronous
# def test_invoice_info_sync():
#     mono = MonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = mono.invoice.create(amount=100)
#
#     status = mono.invoice.info(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
#
#
# # Invoice info: asynchronous
# @pytest.mark.asyncio
# async def test_invoice_info_async():
#     mono = AsyncMonoAcquiringAPI(
#         api_token=api_token
#     )
#
#     invoice = await mono.invoice.create(amount=100)
#
#     status = await mono.invoice.info(invoice_id=invoice.invoice_id)
#
#     assert isinstance(status, InvoiceStatusResponse)
