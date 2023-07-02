# Mbnk
<hr>

![PyPI](https://img.shields.io/pypi/v/mbnk)

## Sync/Async Python3 Monobank API

### Introduction

<b>mbnk</b> - python lib for: 
<br>
<br>&bull; Monobank Open API 
<br>official docs: https://api.monobank.ua/docs/ 
<br>lib docs: https://github.com/yeghorkikhai/mbnk/blob/master/docs/monobank_open_api.md
<br>&bull; Monobank Open API for providers 
<br> official docs: https://api.monobank.ua/docs/corporate.html
<br>lib docs: https://github.com/yeghorkikhai/mbnk/blob/master/docs/monobank_corp_open_api.md
<br>&bull; MonoPay - Monobank Acquiring
<br>official docs: https://api.monobank.ua/docs/acquiring.html
<br>lib docs: https://github.com/yeghorkikhai/mbnk/blob/master/docs/monopay_api.md

### Github
```
https://github.com/yeghorkikhai/mbnk
```

### Installation
```python
pip install mbnk
```

### Getting Started Monobank Open API

```python
# Sync Version Monobank API
import os
from mbnk import Monobank

# Your Monobank API token 
api_token = os.getenv('<X-Token>')

mbnk = Monobank(api_token=api_token)

#Get currencies rates list
currencies_list = mbnk.public.currency_rates()

# Async Version Monobank API
import os
import asyncio
from mbnk.asyncio import AsyncMonobank

# Your Monobank API token 
api_token = os.getenv('<X-Token>')


async def main():
    async_mbnk = AsyncMonobank(api_token=api_token)
    
    currencies_list = await mbnk.public.currency_rates()

    
if __name__ == "__main__":
    asyncio.run(main())

```

```python

#Get Client Info
client_info = mbnk.personal.info()

#Setup webhook url
WEB_HOOK_URL = 'https://example.com/webhook/endpoint'
mbnk.personal.set_webhook(web_hook_url=WEB_HOOK_URL)

#Get statement
from_timestamp = (datetime.now() + timedelta(days=-31)).timestamp()
statement = mbnk.personal.statement(from_date=int(from_timestamp))
```