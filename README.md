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

### Get Started with Monobank Open API

<b>Async example:</b>
```python
import os
import asyncio
from mbnk.asyncio import AsyncMonobankOpenAPI

async def main():
    async_mono = AsyncMonobankOpenAPI(api_token=os.getenv("MONOBANK_API_TOKEN"))
    
    currency_list = await async_mono.public.currency()
    
if __name__ == "__main__":
    asyncio.run(main())
```

<b>Sync example:</b>
```python
import os
from mbnk import MonobankOpenAPI

mono = MonobankOpenAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

#Get currencies rates list
currency_list = mono.public.currency()
```
