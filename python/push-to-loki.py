# example of usage grafana/loki api when you need push any log/message from your python scipt
import requests
import json
import datetime
import pytz

host = 'somehost'
curr_datetime = datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))
curr_datetime = curr_datetime.isoformat('T')
msg = 'On server {host} detected error'.format(host=host)

# push msg log into grafana-loki
url = 'http://host-where-loki-run:3100/loki/api/v1/push'
headers = {
    'Content-type': 'application/json'
}
payload = {
    'streams': [
        {
            'labels': '{source=\"Name-of-your-source\",job=\"name-of-your-job\", host=\"' + host + '\"}',
            'entries': [
                {
                    'ts': curr_datetime,
                    'line': '[WARN] ' + msg
                }
            ]
        }
    ]
}
payload = json.dumps(payload)
answer = requests.post(url, data=payload, headers=headers)
print(answer)
response = answer
print(response)
# end pushing
