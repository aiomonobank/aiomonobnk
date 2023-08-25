## Mono Acquiring API
Офіційна документація: https://api.monobank.ua/docs/acquiring.html

### Вебхук

#### Верифікація підпису WebHook

```python
from aiomonobnk.utils.webhook import webhook_authentication

# example pubkey
pub_key_base64 = "LS0tLS1CRUdJTiBQVUJMSUM...IEtFWS0tLS0tCg=="

# value from X-Sign header in webhook request
x_sign_base64 = "MEUYpm...EaWur7nQXlKDCFxA="

# webhook request body bytes
body_bytes = b'''{
  "invoiceId": "p2_9ZgpZVsl3",
  "status": "created",
  "failureReason": "string",
  "amount": 4200,
  "ccy": 980,
  "finalAmount": 4200,
  "createdDate": "2019-08-24T14:15:22Z",
  "modifiedDate": "2019-08-24T14:15:22Z",
  "reference": "84d0070ee4e44667b31371d8f8813947",
  "cancelList": [
    {
      "status": "processing",
      "amount": 4200,
      "ccy": 980,
      "createdDate": "2019-08-24T14:15:22Z",
      "modifiedDate": "2019-08-24T14:15:22Z",
      "approvalCode": "662476",
      "rrn": "060189181768",
      "extRef": "635ace02599849e981b2cd7a65f417fe"
    }
  ]
}'''

if webhook_authentication(
        pub_key_base64=pub_key_base64,
        x_sign_base64=x_sign_base64,
        body_bytes=body_bytes
):
    print("Authenticated")
else:
    print("Failed to authenticate")

```
### Оплати
#### Створення рахунку

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv('MONOBANK_API_TOKEN')
)

response = mono.invoice.create(amount=100)

```

#### Статус рахунку

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Розширена інформація про успішну оплату

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = monopay.invoice.info(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.invoice.status(invoice_id="<invoiceId>")
```

### Qr-Каси

#### Список QR-кас

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

qr_list = mono.qr.list()
```

#### Інформація про QR-касу

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

qr_details = mono.qr.details(qr_id="qrId")
```

#### Видалення суми оплати

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.qr.reset_amount(qr_id="<qrId>")
```

### Гаманець

#### Список карток у гаманці

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.wallet.cards()
```

#### Оплата по токену

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.wallet.payment()
```

#### Видалення токенізованої картки

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.wallet.delete_card(wallet_id="<walletId>")
```

### Мерчант

#### Дані мерчанта

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

merchant_details = mono.merchant.details()
```

#### Виписка за період

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

merchant_statement = mono.merchant.statement()
```

#### Відкритий ключ для верифікації підписів

```python
import os
from aiomonobnk import MonoAcquiringAPI

mono = MonoAcquiringAPI(
    api_token=os.getenv("MONOBANK_API_TOKEN")
)

response = mono.merchant.pubkey()
pubkey = response.key
```