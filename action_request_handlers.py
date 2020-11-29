from .root import app

from .config import * 

@app.handle(intent='create_action_request')
def create_action_request(request, responder):
    view_action, view_mode = get_view_params("create")
    meta_uri = "service.actionRequests"
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map = {
        'crm_acct': '&autoFill=contactType%3d8&autoFill=contactCode%3d',
        'customer': '&autoFill=contactType%3d1&autoFill=contactCode%3d',
        'employee': '&autoFill=contactType%3d4&autoFill=contactCode%3d',
        'end_user': '&autoFill=contactType%3d2&autoFill=contactCode%3d',
        'engineer': '&autoFill=contactType%3d6&autoFill=contactCode%3d',
        'other': '&autoFill=contactType%3d7&autoFill=contactCode%3d',
        'salespsn': '&autoFill=contactType%3d5&autoFill=contactCode%3d',
        'supplier': '&autoFill=contactType%3d3&autoFill=contactCode%3d'
    }
    for e in request.entities:
        if e['type'] == 'contact_type' and 'children' in e:
            customer_id = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname in param_map:
                params.append(param_map[cname] + customer_id)
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Creating an action request. Here is the URL: ' + url)

@app.handle(intent='open_action_request')
def open_action_request(request, responder):
    view_action, view_mode = get_view_params("read")
    meta_uri = "service.actionRequests"
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map = {
        'crm_acct': '&filter=local_variables.local-var02,eq,CrmAcct,literal',
        'customer': '&filter=local_variables.local-var02,eq,Customer,literal',
        'employee': '&filter=local_variables.local-var02,eq,Employee,literal',
        'end_user': '&filter=local_variables.local-var02,eq,End%20User,literal',
        'engineer': '&filter=local_variables.local-var02,eq,Engineer,literal',
        'other': '&filter=local_variables.local-var02,eq,Other,literal',
        'salespsn': '&filter=local_variables.local-var02,eq,Salespsn,literal',
        'supplier': '&filter=local_variables.local-var02,eq,Supplier,literal'
    }
    action_request_id = next((e for e in request.entities if e['type'] == 'action_request_id'), None)
    if action_request_id:
        params.append('&filter=acr_mstr.acr_nbr,eq,' + action_request_id['text'] + ',literal')
    for e in request.entities:
        if e['type'] == 'contact_type':
            cname = e['value'][0]['cname']
            if cname in param_map:
                params.append(param_map[cname])
                if 'children' in e:
                    customer_id = e['children'][0]['text']
                    params.append('&filter=acr_mstr.acr_con_code,eq,' + customer_id + ',literal')
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Opening an action request. Here is the URL: ' + url)

@app.handle(intent='edit_action_request')
def edit_action_request(request, responder):
    view_action, view_mode = get_view_params("update")
    meta_uri = "service.actionRequests"
    params = []
    params.append(view_action)
    params.append(view_mode)
    param_map_contact_name = {
        'sold-to': '&autoFill=contactName%3d',
        'contact_name': '&autoFill=contactName%3d',
    }
    param_map_contact_type = {
        'crm_acct': '&autoFill=contactType%3d8',
        'customer': '&autoFill=contactType%3d1',
        'employee': '&autoFill=contactType%3d4',
        'end_user': '&autoFill=contactType%3d2',
        'engineer': '&autoFill=contactType%3d6',
        'other': '&autoFill=contactType%3d7',
        'salespsn': '&autoFill=contactType%3d5',
        'supplier': '&autoFill=contactType%3d3'
    }
    action_request_id = next((e for e in request.entities if e['type'] == 'action_request_id'), None)
    if action_request_id:
        params.append('&filter=acr_mstr.acr_nbr,eq,' + action_request_id['text'] + ',literal')
    else:
        responder.reply('Please specify an action request.')
        return
    for e in request.entities:
        if e['type'] == 'field' and len(e['value']) > 0 and 'children' in e:
            child = e['children'][0]['text']
            cname = e['value'][0]['cname']
            if cname == 'sold-to' or cname == 'contact_name':
                params.append(param_map_contact_name[cname] + child)
            elif cname == 'contact_type':
                try:
                    contact_type = e['children'][0]['value'][0]['cname']
                    params.append(param_map_contact_type[contact_type])
                except IndexError:
                    pass
    url = base_url + meta_uri
    for p in params:
        url += p
    responder.reply('Editing an action request. Here is the URL: ' + url)

@app.handle(intent='delete_action_request')
def delete_action_request(request, responder):
    open_action_request(request, responder)