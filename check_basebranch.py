import json
import os
import sys

event_name = os.environ['GITHUB_EVENT_NAME']
if event_name not in ('pull_request_target', 'pull_request'):
    print(f'No-op for {event_name}')
    sys.exit(0)

event_jsonfile = os.environ['GITHUB_EVENT_PATH']

with open(event_jsonfile, encoding='utf-8') as fin:
    event = json.load(fin)

skip_label = os.environ.get('SKIP_BASEBRANCH_CHECK_LABEL')
pr_labels = [e['name'] for e in event['pull_request']['labels']]
if skip_label and skip_label in pr_labels:
    print('Base branch check is skipped due to the presence of '
          f'{skip_label} label.')
    sys.exit(0)

allowed_basebranch = os.environ.get('BASEBRANCH_NAME', 'main')
pr_base_branch = event['pull_request']['base']['ref']
if pr_base_branch != allowed_basebranch:
    print(f'PR opened against {pr_base_branch}, not {allowed_basebranch}')
    sys.exit(1)

print(f'PR opened correctly against {allowed_basebranch}')
