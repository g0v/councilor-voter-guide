def append_contact(item, contact_type, label, value):
    item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})


def append_contact_list(item, contact_type, label, value_list):
    for value in value_list:
        item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})
