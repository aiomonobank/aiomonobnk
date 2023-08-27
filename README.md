# Aiomonobnk
<hr>

![PyPI](https://img.shields.io/pypi/l/aiomonobnk)
![PyPI](https://img.shields.io/pypi/v/aiomonobnk)
![PyPI](https://img.shields.io/pypi/pyversions/aiomonobnk)

## Async Python3.11 Monobank API

### Introduction

<b>Aiomonobnk</b> - python lib for: 
<br>&bull; MonoPay - Monobank Acquiring
<br>official docs: https://api.monobank.ua/docs/acquiring.html
<br>lib docs: https://github.com/yeghorkikhai/mbnk/blob/master/docs/monopay_api.md

### Github
```
https://github.com/yeghorkikhai/aiomonobnk
```

### Installation
```
pip install aiomonobnk
```

### Get Started with Monobank Open API


```python
import os
import asyncio
from aiomonobnk import MonoPay


async def main():
    async_mono = MonoPay(token=os.getenv("MONOBANK_API_TOKEN"))

    invoice = await async_mono.create_invoice(...)


if __name__ == "__main__":
    asyncio.run(main())
```
