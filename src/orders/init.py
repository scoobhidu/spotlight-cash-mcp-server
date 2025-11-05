import json

import requests

from config import master
from headers_util import add_vensec_auth_to_headers
from fastapi import Request, APIRouter

orderRouter = APIRouter()

class UserOrders:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization


    async def PlaceOrder(request: Request):
        # Get request body
        body = await request.json()

        # Extract parameters from request body
        client_id = body.get('client_id', 'AA0793')  # Default client_id
        security_id = body.get('security_id')
        exchange = body.get('exchange')
        segment = body.get('segment', 'E')  # Default segment, D -> derivatives
        txn_type = body.get('txn_type')  # B for Buy, S for Sell
        order_type = body.get('order_type', 'MKT')  # MKT, LMT, etc.
        quantity = body.get('quantity')
        price = body.get('price', 0)
        trigger_price = body.get('trigger_price', 0)
        product = body.get('product', 'C')  # Default product
        validity = body.get('validity', 'DAY')  # Default validity, EOS for BFO
        disc_quantity = body.get('disc_quantity', 0)
        off_mkt_flag = body.get('off_mkt_flag', 0)
        remarks = body.get('remarks', '')
        source = body.get('source', 'W')  # Default source

        url = f"{DATA_API_HOST}/orders/v1/delivery"
        headers = add_vensec_auth_to_headers(
            request.headers.get('session_id'),
            request.headers.get('x-client-id'),
            request.headers.get('Authorization')
        )

        payload = json.dumps({
            "client_id": client_id,
            "security_id": security_id,
            "exchange": exchange,
            "segment": segment,
            "txn_type": txn_type,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
            "trigger_price": trigger_price,
            "product": product,
            "validity": validity,
            "disc_quantity": disc_quantity,
            "off_mkt_flag": off_mkt_flag,
            "remarks": remarks,
            "source": source
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        restemp = response.json()

        return restemp


    async def ModifyOrder(request: Request):
        # Get request body
        if request.method == "POST":
            body = await request.json()
        else:
            # For GET requests, you might want to get parameters from query params
            body = dict(request.query_params)

        # Extract parameters from request body
        client_id = body.get('client_id', 'AA0793')
        order_no = body.get('order_no')
        order_type = body.get('order_type')
        quantity = body.get('quantity')
        price = body.get('price', 0)
        trigger_price = body.get('trigger_price', 0)
        disc_quantity = body.get('disc_quantity', 0)
        remarks = body.get('remarks', '')
        validity = body.get('validity', 'DAY')
        off_mkt_flag = body.get('off_mkt_flag', 0)
        source = body.get('source', 'W')

        # Validate required fields
        if not order_no:
            return {
                "status": "error",
                "message": "order_no is required for order modification"
            }

        url = f"{DATA_API_HOST}/orders/v1/modify"
        headers = add_vensec_auth_to_headers(
            request.headers.get('session_id'),
            request.headers.get('x-client-id'),
            request.headers.get('Authorization')
        )

        payload = json.dumps({
            "client_id": client_id,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
            "trigger_price": trigger_price,
            "disc_quantity": disc_quantity,
            "remarks": remarks,
            "order_no": order_no,
            "validity": validity,
            "off_mkt_flag": off_mkt_flag,
            "source": source
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        restemp = response.json()

        return restemp


    async def CancelOrder(request: Request):
        # Get request body
        if request.method == "POST":
            body = await request.json()
        else:
            # For GET requests, get parameters from query params
            body = dict(request.query_params)

        # Extract parameters
        client_id = body.get('client_id', 'AA0793')
        order_no = body.get('order_no')
        source = body.get('source', 'W')

        # Validate required fields
        if not order_no:
            return {
                "status": "error",
                "message": "order_no is required for order cancellation"
            }

        url = f"{DATA_API_HOST}/orders/v1/cancel"
        headers = add_vensec_auth_to_headers(
            request.headers.get('session_id'),
            request.headers.get('x-client-id'),
            request.headers.get('Authorization')
        )

        payload = json.dumps({
            "client_id": client_id,
            "order_no": order_no,
            "source": source
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        restemp = response.json()

        return restemp


@orderRouter.get("/place_order")
@orderRouter.post("/place_order")
async def PlaceOrder(request: Request):
    # Get request body
    body = await request.json()

    # Extract parameters from request body
    client_id = body.get('client_id', 'AA0793')  # Default client_id
    security_id = int(master[str(body.get('symbol'))])
    exchange = body.get('exchange')
    segment = body.get('segment', 'E')  # Default segment, D -> derivatives
    txn_type = body.get('txn_type')  # B for Buy, S for Sell
    order_type = body.get('order_type', 'MKT')  # MKT, LMT, etc.
    quantity = body.get('quantity')
    price = body.get('price', 0)
    trigger_price = body.get('trigger_price', 0)
    product = body.get('product', 'C')  # Default product
    validity = body.get('validity', 'DAY')  # Default validity, EOS for BFO
    disc_quantity = body.get('disc_quantity', 0)
    off_mkt_flag = body.get('off_mkt_flag', 0)
    remarks = body.get('remarks', '')
    source = body.get('source', 'W')  # Default source

    url = f"{DATA_API_HOST}/orders/v1/delivery"
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    payload = json.dumps({
        "client_id": client_id,
        "security_id": security_id,
        "exchange": exchange,
        "segment": segment,
        "txn_type": txn_type,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
        "trigger_price": trigger_price,
        "product": product,
        "validity": validity,
        "disc_quantity": disc_quantity,
        "off_mkt_flag": off_mkt_flag,
        "remarks": remarks,
        "source": source
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    restemp = response.json()

    return restemp


@orderRouter.get("/modify_order")
@orderRouter.post("/modify_order")
async def ModifyOrder(request: Request):
    # Get request body
    if request.method == "POST":
        body = await request.json()
    else:
        # For GET requests, you might want to get parameters from query params
        body = dict(request.query_params)

    # Extract parameters from request body
    client_id = body.get('client_id', 'AA0793')
    order_no = body.get('order_no')
    order_type = body.get('order_type')
    quantity = body.get('quantity')
    price = body.get('price', 0)
    trigger_price = body.get('trigger_price', 0)
    disc_quantity = body.get('disc_quantity', 0)
    remarks = body.get('remarks', '')
    validity = body.get('validity', 'DAY')
    off_mkt_flag = body.get('off_mkt_flag', 0)
    source = body.get('source', 'W')

    # Validate required fields
    if not order_no:
        return {
            "status": "error",
            "message": "order_no is required for order modification"
        }

    url = f"{DATA_API_HOST}/orders/v1/modify"
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    payload = json.dumps({
        "client_id": client_id,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
        "trigger_price": trigger_price,
        "disc_quantity": disc_quantity,
        "remarks": remarks,
        "order_no": order_no,
        "validity": validity,
        "off_mkt_flag": off_mkt_flag,
        "source": source
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    restemp = response.json()

    return restemp


@orderRouter.get("/cancel_order")
@orderRouter.post("/cancel_order")
async def CancelOrder(request: Request):
    # Get request body
    if request.method == "POST":
        body = await request.json()
    else:
        # For GET requests, get parameters from query params
        body = dict(request.query_params)

    # Extract parameters
    client_id = body.get('client_id', 'AA0793')
    order_no = body.get('order_no')
    source = body.get('source', 'W')

    # Validate required fields
    if not order_no:
        return {
            "status": "error",
            "message": "order_no is required for order cancellation"
        }

    url = f"{DATA_API_HOST}/orders/v1/cancel"
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    payload = json.dumps({
        "client_id": client_id,
        "order_no": order_no,
        "source": source
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    restemp = response.json()

    return restemp