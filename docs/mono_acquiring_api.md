## Вебхук

#### Верифікація підпису WebHook
```python
from mbnk.utils.webhook import webhook_authentication

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
from mbnk import MonoPay

monopay = MonoPay(api_token=os.getenv('MONOPAY_API_TOKEN'))

response = monopay.invoice.create(amount=100)

```

#### Статус рахунку

```python
response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Розширена інформація про успішну оплату

```python
response = monopay.invoice.info(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
response = monopay.invoice.status(invoice_id="<invoiceId>")
```

#### Invoice Status

```python
response = monopay.invoice.status(invoice_id="<invoiceId>")
```

### Qr-Каси

#### Список QR-кас
```python

```

#### Інформація про QR-касу
```python

```

#### Видалення суми оплати
```python

```

### Гаманець

#### Список карток у гаманці
```python

```

#### Оплата по токену
```python

```

#### Видалення токенізованої картки
```python

```

### Мерчант

#### Дані мерчанта
```python

```

#### Виписка за період
```python

```

#### Відкритий ключ для верифікації підписів
```python

```