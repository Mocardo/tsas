from datetime import datetime
import json

CACHE_FOLDER = 'caches'

def cache_json(obj, fname_beg):
  obj_str = json.dumps(obj, indent=2, default=lambda o: o.__dict__)
  path = CACHE_FOLDER + f'/{fname_beg}_{datetime.now()}.json'
  cax = open(path, 'w')
  cax.write(obj_str)
  cax.close()

def list_to_list_of_dicts(ll):
  return [ll[i].to_dict() for i in range(len(ll))]
