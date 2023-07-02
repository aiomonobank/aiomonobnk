from enum import Enum


class APIPaths(str, Enum):

    # MonoPay

    merchant_details = "merchant/details"
    merchant_statement = "merchant/statement"
    merchant_pubkey = "merchant/pubkey"

    invoice_create = "merchant/invoice/create"
    invoice_split = "merchant/invoice/split-payments"
    invoice_cancel = "merchant/invoice/cancel"
    invoice_status = "merchant/invoice/status"
    invoice_invalidation = "merchant/invoice/remove"
    invoice_info = "merchant/invoice/payment-info"
    invoice_finalize = "merchant/invoice/finalize"

    qr_list = "merchant/qr/list"
    qr_details = "merchant/qr/details"
    qr_reset_amount = "merchant/qr/reset-amount"

    wallet_cards = "merchant/wallet"
    wallet_payment = "merchant/wallet/payment"
    wallet_delete_card = "merchant/wallet/card"

    # Monobank Open API

    currencies_list = "bank/currency"

    personal_info = "personal/client-info"
    personal_webhook = "personal/webhook"
    personal_statement = "personal/statement/{account}/{from}/{to}"

    # Monobank Open API for providers

    auth_registration = "personal/auth/registration"
    auth_status = "personal/auth/registration/status"

    corporate_webhook = "personal/corp/webhook"
    corporate_info = "personal/corp/settings"

    init_access = "personal/auth/request"
    check_access = "personal/auth/request"
