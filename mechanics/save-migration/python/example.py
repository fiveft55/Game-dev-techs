"""Versioned JSON save migration. Original MIT-licensed educational implementation."""

import json

def load_save(text):
    if not isinstance(text,str) or len(text)>65536: raise ValueError("save too large or not text")
    try:
        data=json.loads(text)
    except (ValueError,RecursionError) as error:
        raise ValueError("invalid JSON") from error
    if not isinstance(data,dict) or type(data.get('version')) is not int:
        raise ValueError("invalid save header")
    if data['version']==1:
        data={'version':2,'inventory':{'gold':data.get('gold',0)}}
    if data['version']!=2 or not isinstance(data.get('inventory'),dict):
        raise ValueError("unsupported save schema")
    inventory=data['inventory']
    if any(not isinstance(k,str) or type(v) is not int or v<0 for k,v in inventory.items()):
        raise ValueError("invalid inventory")
    return {'version':2,'inventory':dict(inventory)}
