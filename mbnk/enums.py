from enum import Enum


class MonoPayApiUrls(str, Enum):
    merchant_details = "{base_url}/api/merchant/details"
    merchant_statement = "{base_url}/api/merchant/statement"
    merchant_pubkey = "{base_url}/api/merchant/pubkey"

    invoice_create = "{base_url}/api/merchant/invoice/create"
    invoice_split = "{base_url}/api/merchant/invoice/split-payments"
    invoice_cancel = "{base_url}/api/merchant/invoice/cancel"
    invoice_status = "{base_url}/api/merchant/invoice/status"
    invoice_invalidation = "{base_url}/api/merchant/invoice/remove"
    invoice_info = "{base_url}/api/merchant/invoice/payment-info"
    invoice_finalize = "{base_url}/api/merchant/invoice/finalize"

    qr_list = "{base_url}/api/merchant/qr/list"
    qr_details = "{base_url}/api/merchant/qr/details"
    qr_reset_amount = "{base_url}/api/merchant/qr/reset-amount"

    wallet_cards = "{base_url}/api/merchant/wallet"
    wallet_payment = "{base_url}/api/merchant/wallet/payment"
    wallet_delete_card = "{base_url}/api/merchant/wallet/card"
