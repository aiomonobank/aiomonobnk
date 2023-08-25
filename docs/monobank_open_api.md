## Monobank Open API

### Публічні дані

#### Отримання курсів валют

```python
import os
from aiomonobnk import MonobankOpenAPI

mono = MonobankOpenAPI()

currency_list = mono.public.currency()
```

### Клієнтські персональні дані

#### Інформація про клієнта

```python
import os
from aiomonobnk import MonobankOpenAPI

mono = MonobankOpenAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

client_info = mono.personal.info()
```

#### Встановлення WebHook

```python
import os
from aiomonobnk import MonobankOpenAPI

mono = MonobankOpenAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

web_hook_url = "https://example.com/webHook/endpoint"

mono.personal.set_web_hook(
    web_hook_url=web_hook_url
)
```

#### Виписка

```python
import os
from aiomonobnk import MonobankOpenAPI
from datetime import datetime, timedelta

mono = MonobankOpenAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

from_timestamp = (datetime.now() - timedelta(days=10)).timestamp().as_integer_ratio()
to_timestamp = (datetime.now() - timedelta(days=5)).timestamp().as_integer_ratio()

statement = mono.personal.statement(
    account="<accountId>",
    _from=from_timestamp,
    _to=to_timestamp
)
```

