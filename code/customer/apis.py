from datetime import datetime
from typing import List, Optional
from ninja import NinjaAPI, Query

from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from .models import Order, User, Customer, Address, Product, GiftCard, Billing, DiscountCode,DiscountCodeCreationJob
from .schemas import OrdersResp, CancelOrderResp, OrderOut, CancelOrderIn, OrderIn, OrderResp, CustomerOut, CustomerResp, AddressIn, AddressResp, UserCreateIn, ProductIn, ProductResp, GiftCardResp, GiftCardIn, GiftCardResp, BillingIn, GiftCardDetailOut, BillingResp, DiscountBatchIn, DiscountBatchOut, SingleDiscountCodeResp, SingleDiscountCodeIn, DiscountCodeCreationResp
api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.post('/auth/register', response=CustomerOut)
def register(request, data: UserCreateIn):
    user = User.objects.create_user(
        username=data.email,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    customer = Customer.objects.create(
        user=user,
        state=data.state,
        verified_email=data.verified_email,
        send_email_welcome=data.send_email_welcome,
        currency=data.currency,
        phone=data.phone
    )
    return customer

@api.get("/")
def index(request):
    return {'NIM' : 'A11.2021.13937',
            'Nama' : 'Hafizh Hugo Harman'}

@api.get("hello")
def helloWorld(request):
    return {'hello' : 'hello from A11.2021.13937'}

@api.get("customers.json",auth=apiAuth,response=CustomerResp)
def get_all_customers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers' : customers }

@api.post('customers/{id_cust}/addresses.json',auth=apiAuth, response=AddressResp)
def add_customer(request, id_cust: int, data: AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    customer_address = Address.objects.create(
        customer=cust,
        address1=data.address1,
        address2=data.address2,
        city=data.city,
        province=data.province,
        company=data.company,
        zip=data.zip
    )
    return {'customer_address': [customer_address]}

@api.put('customers/{id_cust}/addresses/{id_addr}/default.json',response=AddressResp)
def set_default_address(request,id_cust:int,id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default = True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()
        
    return {'customer_address': [addr]}

@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def delete_address(request,id_cust:int,id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

@api.get('products.json', response=ProductResp)
def get_all_products(request):
    products = Product.objects.all()
    return {'products': products}

@api.post("products.json", response=ProductResp)
def add_product(request, data: ProductIn):
    products = Product.objects.create(
        title=data.title,
        body_html=data.body_html,
        vendor=data.vendor,
        product_type=data.product_type,
        status=data.status,
        handle=data.title.lower().replace(' ', '-'), 
        price=0.00, 
        inventory_quantity=0,
        weight=0,
        weight_unit='kg',
        requires_shipping=True,
        taxable=True
    )
    
    return {"products": [products]} 

@api.delete('/products/{id_product}.json')
def delete_product(request,id_product:int):
    Product.objects.get(pk=id_product).delete()
    return {}

@api.post("gift_cards.json", response=GiftCardDetailOut)
def add_gift_card(request, data: GiftCardIn):
    gift_card = GiftCard.objects.create(
        balance=data.initial_value,
        code=data.code,
        currency="USD",
        initial_value=data.initial_value,
        note=data.note,
        template_suffix=data.template_suffix
    )
    return gift_card

@api.get("gift_cards.json", response=GiftCardResp)
def get_all_gift_cards(request):
    gift_card = GiftCard.objects.all()
    return {"gift_card": gift_card}

@api.post("gift_cards/{id_gift_card}/disable.json", response=GiftCardResp)
def disable_gift_card(request, id_gift_card: int):
    gift_card = GiftCard.objects.get(pk=id_gift_card)
    gift_card.disabled_at = datetime.now()
    gift_card.save()
    return {"gift_card": [gift_card]}

@api.post("application_charges.json", response=BillingResp)
def create_application_charge(request, data: BillingIn):
    charge_data = data.application_charge
    application_charge = Billing.objects.create(
        name=charge_data.name,
        price=charge_data.price,
        return_url=charge_data.return_url,
        test=charge_data.test,
        status='pending',
        currency='USD'
    )
    charge_id = application_charge.pk
    application_charge.decoration_return_url = f"{charge_data.return_url}?charge_id={charge_id}"
    application_charge.confirmation_url = f"{charge_data.return_url}/admin/charges/{charge_id}/ApplicationCharge/confirm_application_charge"
    application_charge.save()  
    
    billings = Billing.objects.get(pk=charge_id)

    return {"application_charge": [billings]}

@api.get("application_charges.json", response=BillingResp)
def get_application_charges(request):
    billings = Billing.objects.all()
    return {"application_charge": billings}

@api.post('/price_rules/{price_rule_id}/batch.json', response=DiscountBatchOut)
def create_discount_batch(request, price_rule_id: int, data: DiscountBatchIn):
    created_at = datetime.now()
    discount_code_creation = DiscountCodeCreationJob.objects.create(
        price_rule_id=price_rule_id,
        created_at=created_at,
        updated_at=created_at,
        status="queued",
        codes_count=len(data.discount_codes)
    )
    
    discount_codes = []

    for code_data in data.discount_codes:
        discount_code = DiscountCode.objects.create(
            code=code_data.code,
            creation_job=discount_code_creation,
            created_at=created_at,
            updated_at=created_at
        )
        discount_codes.append(discount_code)

    discount_code_creation_data = {
        "id": discount_code_creation.id,
        "price_rule_id": price_rule_id,
        "started_at": None,
        "completed_at": None,
        "created_at": created_at,
        "updated_at": created_at,
        "status": "queued",
        "codes_count": len(discount_codes),
        "imported_count": 0,
        "failed_count": 0,
        "logs": []
    }

    return {"discount_code_creation": discount_code_creation_data}

@api.post('/price_rules/{price_rule_id}/discount_codes.json', response=SingleDiscountCodeResp)
def create_single_discount_code(request, price_rule_id: int, data: SingleDiscountCodeIn):
    created_at = datetime.now()
    code = data.discount_code.code

    discount_code_creation, created = DiscountCodeCreationJob.objects.get_or_create(
        price_rule_id=price_rule_id,
        defaults={'created_at': created_at, 'updated_at': created_at, 'status': 'queued'}
    )

    discount_code = DiscountCode.objects.create(
        code=code,
        creation_job=discount_code_creation,
        created_at=created_at,
        updated_at=created_at,
        usage_count=0
    )

    discount_code_creation.codes_count = discount_code_creation.discount_codes.count()
    discount_code_creation.save()

    discount_code_response = {
        "id": discount_code.id,
        "price_rule_id": price_rule_id,
        "code": discount_code.code,
        "usage_count": discount_code.usage_count,
        "created_at": created_at,
        "updated_at": created_at
    }

    return {"discount_code": discount_code_response}

@api.get('/discount_codes/count.json')
def get_discount_code_count(request):
    count = DiscountCode.objects.count()
    return {"count": count}

@api.get('/price_rules/{price_rule_id}/batch/{batch_id}.json', response=DiscountCodeCreationResp)
def get_discount_code_creation(request, price_rule_id: int, batch_id: int):
    discount_code_creation = DiscountCodeCreationJob.objects.filter(price_rule_id=price_rule_id, id=batch_id).first()
    discount_code_creation_data = {
        "id": discount_code_creation.id,
        "price_rule_id": discount_code_creation.price_rule_id,
        "started_at": discount_code_creation.started_at,
        "completed_at": discount_code_creation.completed_at,
        "created_at": discount_code_creation.created_at,
        "updated_at": discount_code_creation.updated_at,
        "status": discount_code_creation.status,
        "codes_count": discount_code_creation.discount_codes.count(),
        "imported_count": discount_code_creation.imported_count,
        "failed_count": discount_code_creation.failed_count,
        "logs": discount_code_creation.logs
    }
    
    return {"discount_code_creation": discount_code_creation_data}


@api.delete('/price_rules/{price_rule_id}/discount_codes/{discount_code_id}.json', response={204: None})
def delete_discount_code(request, price_rule_id: int, discount_code_id: int):
    discount_code = DiscountCode.objects.get(id=discount_code_id, creation_job__price_rule_id=price_rule_id)
    discount_code.delete()
    return api.create_response(request, None, status=204)

@api.post('/orders.json', response=OrderResp)
def create_order(request, data: OrderIn):
    order_data = data.order
    order = Order.objects.create(
        order_number=str(Order.objects.count() + 1), 
        email=request.user.email if request.user.is_authenticated else "",
        phone="",
        financial_status="paid",
        fulfillment_status="unfulfilled",
        total_price=sum(item.price * item.quantity for item in order_data.line_items),
        subtotal_price=sum(item.price * item.quantity for item in order_data.line_items),
        total_tax=order_data.total_tax,
        total_discounts=0,
        currency=order_data.currency,
        note="",
        tags=""
    )

    for item in order_data.line_items:
        order.add_item(
            product_id=1,  
            quantity=item.quantity,
            price=item.price,
            variant_title=item.title
        )

    return {"order": order}

@api.post('/orders/{order_id}/cancel.json', response=CancelOrderResp)
def cancel_order(request, order_id: int, data: CancelOrderIn):
    try:
        order = Order.objects.get(pk=order_id)
        order.cancel_reason = data.cancel_reason
        order.cancelled_at = datetime.now()
        order.save()
        return {"order": OrderOut.from_orm(order), "notice": "Order has been canceled"}
    except Order.DoesNotExist:
        return {"detail": "Order not found"}, 404

@api.get('/orders.json', response=OrdersResp)
def list_orders(request, status: Optional[str] = Query(None)):
    if status == 'any':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(financial_status=status)
    
    return {"orders": [OrderOut.from_orm(order) for order in orders]}

@api.get('/orders/count.json')
def get_orders_count(request, status: Optional[str] = Query(None)):
    if status == 'any':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(financial_status=status)
    count = orders.count()
    return {"count": count}

@api.delete('/orders/{order_id}.json')
def delete_order(request, order_id: int):
    try:
        order = Order.objects.get(pk=order_id)
        order.delete()
        return {}
    except Order.DoesNotExist:
        return {"detail": "Order not found"}, 404


@api.post('/orders/{order_id}/close.json', response=OrderResp)
def close_order(request, order_id: int):
    try:
        order = Order.objects.get(pk=order_id)
        order.closed_at = datetime.now()
        order.save()
        return {"order": OrderOut.from_orm(order)}
    except Order.DoesNotExist:
        return {"detail": "Order not found"}, 404
    
@api.post('/orders/{order_id}/open.json', response=OrderResp)
def open_order(request, order_id: int):
    try:
        order = Order.objects.get(pk=order_id)
        order.closed_at = None
        order.save()
        return {"order": OrderOut.from_orm(order)}
    except Order.DoesNotExist:
        return {"detail": "Order not found"}, 404
