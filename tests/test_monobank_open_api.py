import os
import pytest

from dotenv import load_dotenv

from mbnk import MonobankOpenAPI
from mbnk.asyncio import AsyncMonobankOpenAPI

from mbnk.responses import *
from mbnk.exceptions import *
from mbnk.types import *

load_dotenv(dotenv_path=os.path.abspath('.env'))


def test_public_currency_sync():
    mono = MonobankOpenAPI()

    currency_list = mono.public.currency()

    assert isinstance(currency_list, CurrencyList)


@pytest.mark.asyncio
async def test_public_currency_async():
    mono = AsyncMonobankOpenAPI()

    currency_list = await mono.public.currency()

    assert isinstance(currency_list, CurrencyList)


def test_personal_info_sync():
    mono = MonobankOpenAPI(
        api_token=os.getenv("TEST_MONOBANK_API_TOKEN")
    )

    client_info = mono.personal.info()

    print(client_info)


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
