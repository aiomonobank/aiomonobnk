## Sync/Async Python3 Monobank API

### Installation
```python
pip install mbnk
```

### Getting Started

```python
import os
from mbnk import Monobank

# Your Monobank API token 
TOKEN = os.getenv('<X-Token>')

mbnk = Monobank(api_token=TOKEN)

#Get currencies rates list
currencies_list = mbnk.public.currency_rates()
print(currencies_list)
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