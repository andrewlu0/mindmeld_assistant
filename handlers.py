from .root import app

action_map = {
  "create": {
    "viewActionParam": "&viewAction=CREATE",
    "viewModeParam": "&hybridMode=maint",
  },
  "read": {
    "viewActionParam": "",
    "viewModeParam": "&hybridMode=browse",
  },
  "update": {
    "viewActionParam": "&viewAction=UPDATE",
    "viewModeParam": "&hybridMode=hybrid",
  },
  "delete": {
    "viewActionParam": "&viewAction=DELETE",
    "viewModeParam": "&hybridMode=hybrid",
  }
}

base_url = "https://qvarfrdlwb01.qad.com/clouderp/#/view/qraview/hybridbrowse?viewMetaUri=urn:view:meta:com.qad.erp."

def get_view_params(action):
    return action_map[action]["viewActionParam"], action_map[action]["viewModeParam"]

# GENERAL INTENTS
@app.handle(intent='greet')
def welcome(request, responder):
    try:
        responder.slots['name'] = request.context['name']
        prefix = 'Hello, {name}. '
    except KeyError:
        prefix = 'Hello. '
    responder.reply(prefix + 'How can I help?')
    responder.listen()

@app.handle(intent='exit')
def say_goodbye(request, responder):
    responder.reply(['Bye', 'Goodbye', 'Have a nice day.'])

@app.handle(default=True)
def default(request, responder):
    responder.reply('Sorry, not sure what you meant there.')
    responder.listen()

# SALES ORDERS HANDLING
@app.handle(intent='create_sale_order')
def create_sale_order(request, responder):
    viewAction, viewMode = get_view_params("create")
    meta_uri = 'sales.salesOrders'
    params = []
    params.append(viewAction)
    params.append(viewMode)
    fields = []
    for e in request.entities:
        if e['type'] == 'field' and e['children']:
            customer_id = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname == 'sold-to':
                prefix = '&autoFill=soldToCustomerCode%3d'
            elif cname == 'ship-to':
                prefix = '&autoFill=shipToCustomerCode%3d'
            elif cname == 'bill-to':
                prefix = '&autoFill=billToCustomerCode%3d'
            else:
                continue
            params.append(prefix + customer_id)
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Creating a sales order. Here is the URL:' + url)

@app.handle(intent='open_sale_order')
def open_sale_order(request, responder):
    viewAction, viewMode = get_view_params("read")
    meta_uri = "sales.salesOrders"
    responder.reply('Opening a sales order. Here are the params:' + meta_uri + ',' + viewAction + ',' + viewMode)

@app.handle(intent='edit_sale_order')
def edit_sale_order(request, responder):
    viewAction, viewMode = get_view_params("update")
    meta_uri = "sales.salesOrders"
    responder.reply('Editing a sales order. Here are the params:' + meta_uri + ',' + viewAction + ',' + viewMode)

@app.handle(intent='delete_sale_order')
def delete_sale_order(request, responder):
    viewAction, viewMode = get_view_params("delete")
    meta_uri = "sales.salesOrders"
    responder.reply('Deleting a sales order. Here are the params:' + meta_uri + ',' + viewAction + ',' + viewMode)


# ACTION REQUEST HANDLING
@app.handle(intent='create_action_request')
def create_action_request(request, responder):
    viewAction, viewMode = get_view_params("create")
    responder.reply('Creating a action request.')

@app.handle(intent='open_action_request')
def open_action_request(request, responder):
    viewAction, viewMode = get_view_params("read")
    responder.reply('Opening a action request.')

@app.handle(intent='edit_action_request')
def edit_action_request(request, responder):
    viewAction, viewMode = get_view_params("update")
    responder.reply('Editing a action request.')

@app.handle(intent='delete_action_request')
def delete_action_request(request, responder):
    viewAction, viewMode = get_view_params("delete")
    responder.reply('Deleting a action request.')


# INVENTORY DETAIL HANDLING
@app.handle(intent='open_inventory_detail')
def open_inventory_detail(request, responder):
    viewAction, viewMode = get_view_params("read")
    responder.reply('Opening inventory detail.')

@app.handle(intent='edit_inventory_detail')
def edit_inventory_detail(request, responder):
    viewAction, viewMode = get_view_params("update")
    responder.reply('Editing inventory detail.')