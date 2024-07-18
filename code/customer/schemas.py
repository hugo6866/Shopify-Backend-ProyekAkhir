from ninja import Schema, ModelSchema, FilterSchema, Field
from datetime import datetime
from typing import Optional, List, Self
from pydantic import model_validator

from customer.models import Customer, Address

from ninja import Schema
from typing import Optional

class ApplicationCharge(Schema):
    name: str
    price: float
    return_url: str
    test: bool

class BillingIn(Schema):
    application_charge: ApplicationCharge
    
class BillingOut(Schema):
    id: int
    name: str
    price: int
    status: str
    return_url: str
    test: bool
    created_at: datetime
    updated_at: datetime
    currency: str
    decoration_return_url: str
    confirmation_url: str

class BillingResp(Schema):
    application_charge: List[BillingOut]
    
    
class GiftCardIn(Schema):
    note: Optional[str] = None
    initial_value: float
    code: str
    template_suffix: Optional[str] = None

class GiftCardOut(Schema):
    id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    currency: str
    initial_value: float
    disabled_at: Optional[datetime] = None
    line_item_id: Optional[int] = None
    customer_id: Optional[int] = None
    note: Optional[str] = None
    expires_on: Optional[datetime] = None
    template_suffix: Optional[str] = None
    last_characters: str
    order_id: Optional[int] = None
    #code: str
    
class GiftCardDetailOut(GiftCardOut):
    code: str


class GiftCardResp(Schema):
    gift_card: List[GiftCardOut ]
    

class ProductIn(Schema):
    title: str
    body_html: Optional[str] = ""
    vendor: str
    product_type: str
    published_at: Optional[datetime] = None
    status: str = 'active'
    tags: Optional[str] = ""
    image_url: Optional[str] = ""
    price: Optional[float] = None
    inventory_quantity: int = 0
    weight: Optional[float] = 0
    weight_unit: Optional[str] = "kg"
    requires_shipping: bool = True
    taxable: bool = True


class ProductOut(Schema):
    id: int
    title: str
    body_html: Optional[str]
    vendor: str
    product_type: str
    created_at: datetime
    updated_at: datetime
    handle: str
    published_at: Optional[datetime]
    status: str
    tags: Optional[str]
    image_url: Optional[str]
    price: Optional[float]
    inventory_quantity: int
    weight: Optional[float]
    weight_unit: Optional[str]
    requires_shipping: bool
    taxable: bool

class ProductResp(Schema):
    products: List[ProductOut]
    
class UserCreateIn(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    state: str
    verified_email: bool
    send_email_welcome: bool
    currency: str
    phone: str
    
class AddressIn(Schema):
    customer_id: int
    address1: str
    address2: Optional[str] = ''
    city: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    phone: Optional[str] = ''
    province: str
    country: str
    zip: str
    company: str
    name: Optional[str] = ''
    
class AddressOut(Schema):
    id: int
    customer_id: int
    first_name: str =  Field(alias='customer.user.first_name')
    last_name: str = Field(alias='customer.user.last_name')
    company: str
    address1: str
    address2: str
    city: str
    province: str
    country: str
    zip: str
    phone: Optional[str] = ''
    name: str
    default: bool
       
class CustomerOut(Schema):
    id: int
    email: str = Field(alias='user.email')
    created_at: datetime
    updated_at: datetime
    first_name: str = Field(alias='user.first_name')
    last_name: str = Field(alias='user.last_name')
    order_counts: int
    state: str
    verified_email: bool
    currency : str
    phone: str
    addresses: Optional[List[AddressOut]] = Field(alias='address_set')
    
class CustomerResp(Schema):
    customers: List[CustomerOut]

class AddressResp(Schema):
    customer_address: List[AddressOut]
    
class DiscountCodeIn(Schema):
    code: str

class DiscountBatchIn(Schema):
    discount_codes: List[DiscountCodeIn]

class DiscountCodeCreation(Schema):
    id: int
    price_rule_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    status: str
    codes_count: int
    imported_count: int
    failed_count: int
    logs: List[str] = []

class DiscountBatchOut(Schema):
    discount_code_creation: DiscountCodeCreation
    
class SingleDiscountCodeOut(Schema):
    id: int
    price_rule_id: int
    code: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

class DiscountCodeData(Schema):
    code: str

class SingleDiscountCodeIn(Schema):
    discount_code: DiscountCodeData

class SingleDiscountCodeOut(Schema):
    id: int
    price_rule_id: int
    code: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

class SingleDiscountCodeResp(Schema):
    discount_code: SingleDiscountCodeOut
class SingleDiscountCodeIn(Schema):
    discount_code: DiscountCodeData

class DiscountCodeCreationOut(Schema):
    id: int
    price_rule_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    status: str
    codes_count: int
    imported_count: int
    failed_count: int
    logs: List[str] = []

class DiscountCodeCreationResp(Schema):
    discount_code_creation: DiscountCodeCreationOut
    
class TaxLine(Schema):
    price: float
    rate: float
    title: str

class LineItem(Schema):
    title: str
    price: float
    grams: int
    quantity: int
    tax_lines: List[TaxLine]

class Transaction(Schema):
    kind: str
    status: str
    amount: float

class OrderData(Schema):
    line_items: List[LineItem]
    transactions: List[Transaction]
    total_tax: float
    currency: str

class OrderIn(Schema):
    order: OrderData

class OrderOut(Schema):
    id: int
    order_number: str
    email: str
    phone: Optional[str] = None
    financial_status: str
    fulfillment_status: str
    total_price: float
    subtotal_price: float
    total_tax: float
    total_discounts: float
    currency: str
    created_at: datetime
    updated_at: datetime
    note: Optional[str] = None
    tags: Optional[str] = None
    discount_code: Optional[str] = None
    discount_amount: Optional[float] = None
    cancel_reason: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

class OrdersResp(Schema):
    orders: List[OrderOut]
class OrderResp(Schema):
    order: OrderOut

class CancelOrderIn(Schema):
    cancel_reason: Optional[str] = "other"

class CancelOrderResp(Schema):
    order: OrderOut
    notice: str

