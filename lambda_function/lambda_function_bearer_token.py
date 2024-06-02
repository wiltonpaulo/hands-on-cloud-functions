import json
import requests

def lambda_handler(event, context):
    url = "https://api.pipedream.com/v1/sources/dc_BVuJZL8/event_summaries"
    headers = {
        "Authorization": "Bearer 2f0042ebb922139b5b7d3cda4539b5ae"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'error': 'Failed to retrieve data'})
        }