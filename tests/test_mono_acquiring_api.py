import pytest

from mbnk import MonoAcquiring
from mbnk.asyncio import AsyncMonoPay

from mbnk.responses import *

api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"


# Invoices

# Invoice create: synchronous
def test_invoice_create_sync():
    mono = MonoAcquiring(
        api_token=api_token
    )

    invoice = mono.invoice.create(amount=100)

    assert isinstance(invoice, InvoiceCreatedResponse)


# Invoice create: asynchronous
@pytest.mark.asyncio
async def test_invoice_create_async():
    mono = AsyncMonoPay(
        api_token=api_token
    )

    invoice = await mono.invoice.create(amount=100)

    assert isinstance(invoice, InvoiceCreatedResponse)


# Invoice status: synchronous
def test_invoice_status_sync():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = mono.invoice.create(amount=100)

    status = mono.invoice.status(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)


# Invoice status: asynchronous
@pytest.mark.asyncio
async def test_invoice_status_async():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = await mono.invoice.create(amount=100)

    status = await mono.invoice.status(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)


# Invoice cancel: synchronous
def test_invoice_cancel_sync():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = mono.invoice.create(amount=100)

    status = mono.invoice.cancel(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)


# Invoice cancel: asynchronous
async def test_invoice_cancel_async():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = await mono.invoice.create(amount=100)

    status = await mono.invoice.cancel(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)


# Invoice info: synchronous
def test_invoice_info_sync():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = mono.invoice.create(amount=100)

    status = mono.invoice.info(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)


# Invoice info: asynchronous
async def test_invoice_info_async():
    mono = MonoPay(
        api_token=api_token
    )

    invoice = mono.invoice.create(amount=100)

    status = mono.invoice.info(invoice_id=invoice.invoice_id)

    assert isinstance(status, InvoiceStatusResponse)
