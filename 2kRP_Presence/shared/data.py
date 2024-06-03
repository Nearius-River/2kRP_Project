data_store = {
    'location': None,
}

def update_data(location):
    global data_store
    data_store['location'] = location

def get_data():
    global data_store
    return data_store