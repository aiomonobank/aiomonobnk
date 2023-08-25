import os
import pytest

from dotenv import load_dotenv

from aiomonobnk import MonobankOpenAPI
from aiomonobnk.asyncio import AsyncMonobankOpenAPI

from aiomonobnk.types import *
from aiomonobnk.enums import *

load_dotenv(dotenv_path=os.path.abspath('.env'))


def test_public_currency_sync():
    mono = MonobankOpenAPI()

    currencies = mono.public.currency()

    print(currencies)

    assert isinstance(currencies, CurrencyList)


@pytest.mark.asyncio
async def test_public_currency_async():
    mono = AsyncMonobankOpenAPI()

    currencies = await mono.public.currency()

    assert isinstance(currencies, CurrencyList)


def test_personal_info_sync():
    mono = MonobankOpenAPI(
        api_token=os.getenv("TEST_MONOBANK_API_TOKEN")
    )

    client_info = mono.personal.info()

    print(client_info)

    assert isinstance(client_info, ClientInfo)


@pytest.mark.asyncio
async def test_personal_info_async():
    pass


def test_personal_set_webhook_sync():
    pass


@pytest.mark.asyncio
async def test_personal_set_webhook_async():
    pass


def test_personal_statement_sync():
    pass


@pytest.mark.asyncio
async def test_personal_statement_async():
    pass
