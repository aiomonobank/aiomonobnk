from mbnk import MonoAcquiringAPI
from mbnk.types import *

api_token = "uAvDe23DVr7MUJpnOTV7rUz_cFyCGlL2bvM74pU05ejc"

mono = MonoAcquiringAPI(
    api_token=api_token
)

merchant_paym_info = MerchantPaymInfo(
    reference="1234",
    destination="Призначення",
    basket_order=[
        Product(
            name='Товар',
            qty=1,
            sum=100
        )
    ]
)

invoice = mono.invoice.create(
    amount=100,
    merchant_paym_info=merchant_paym_info
)

print(invoice)
