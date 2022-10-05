import requests
import openai
from pprint import pprint


with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    pprint(resp)
    return resp


def file_list():
    resp = openai.File.list()
    pprint(resp)


def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    pprint(resp.json())


def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    pprint(resp.json())


def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)    
    pprint(resp.json())


def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)    
    pprint(resp.json())



#resp = file_upload('novel_rh_FF.jsonl')
#resp = file_upload('novel_pnr.jsonl')
#finetune_model(resp['id'], 'candice_bundy_FF', 'davinci')
#finetune_model(resp['id'], 'candice_bundy_pnr', 'davinci')
finetune_list()

# 100k/$3 = davinci:ft-personal:candice-bundy-rh-2022-10-04-06-02-53
# 625k/$20 = davinci:ft-personal:candice-bundy-ff-2022-10-04-16-01-06

#openai.FineTune.cancel("ft-M6f1KHXEiv0n5zOAYVlObwEf")
#openai.Model.delete("davinci:ft-personal:novel-writer-2022-10-02-20-17-57")