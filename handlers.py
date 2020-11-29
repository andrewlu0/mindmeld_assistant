from .root import app

from .config import *

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


# INVENTORY DETAIL HANDLING
@app.handle(intent='open_inventory_detail')
def open_inventory_detail(request, responder):
    view_action, view_mode = get_view_params("read")
    responder.reply('Opening inventory detail.')

@app.handle(intent='edit_inventory_detail')
def edit_inventory_detail(request, responder):
    view_action, view_mode = get_view_params("update")
    responder.reply('Editing inventory detail.')