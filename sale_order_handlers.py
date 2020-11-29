from .root import app

from .config import * 

@app.handle(intent='create_sale_order')
def create_sale_order(request, responder):
    view_action, view_mode = get_view_params("create")
    meta_uri = 'sales.salesOrders'
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map = {
        'sold-to': '&autoFill=soldToCustomerCode%3d',
        'ship-to': '&autoFill=shipToCustomerCode%3d',
        'bill-to': '&autoFill=billToCustomerCode%3d'
    }
    for e in request.entities:
        if e['type'] == 'field' and 'children' in e:
            customer_id = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname in param_map:
                params.append(param_map[cname] + customer_id)
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Creating a sales order. Here is the URL: ' + url)

@app.handle(intent='open_sale_order')
def open_sale_order(request, responder):
    view_action, view_mode = get_view_params("read")
    meta_uri = "sales.salesOrders"
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map = {
        'sold-to': '&filter=so_mstr.so_cust,eq,',
        'ship-to': '&filter=so_mstr.so_ship,eq,',
        'bill-to': '&filter=so_mstr.so_bill,eq,'
    }
    sale_order_id = next((e for e in request.entities if e['type'] == 'sale_order_id'), None)
    if sale_order_id:
        params.append('&filter=so_mstr.so_nbr,eq,' + sale_order_id['text'] + ',literal')
    for e in request.entities:
        if e['type'] == 'field' and 'children' in e:
            customer_id = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname in param_map:
                params.append(param_map[cname] + customer_id + ',literal')
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Opening a sales order. Here is the URL: ' + url)

@app.handle(intent='edit_sale_order')
def edit_sale_order(request, responder):
    view_action, view_mode = get_view_params("update")
    meta_uri = "sales.salesOrders"
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map = {
        'sold-to': '&autoFill=soldToCustomerCode%3d',
        'ship-to': '&autoFill=shipToCustomerCode%3d',
        'bill-to': '&autoFill=billToCustomerCode%3d'
    }
    sale_order_id = next((e for e in request.entities if e['type'] == 'sale_order_id'), None)
    if sale_order_id:
        params.append('&filter=so_mstr.so_nbr,eq,' + sale_order_id['text'] + ',literal')
    else:
        responder.reply('Please specify a sales order.')
        return
    for e in request.entities:
        if e['type'] == 'field' and 'children' in e:
            customer_id = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname in param_map:
                params.append(param_map[cname] + customer_id)
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Editing a sales order. Here is the URL: ' + url)

@app.handle(intent='delete_sale_order')
def delete_sale_order(request, responder):
    open_sale_order(request, responder)