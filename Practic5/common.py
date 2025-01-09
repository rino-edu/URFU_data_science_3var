import json

def save_in_json(data, filepath):
  
  for doc in data:
    for key, value in doc.items():
        if isinstance(value, object):
            doc[key] = str(value)
            
  with open(filepath, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)