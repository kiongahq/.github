#!/usr/bin/env python3
"""Preview or reconcile Kionga repository rules without bypass permissions."""
import argparse
import json
import subprocess

CHECKS = {
    '.github': [],
    'platform': ['console', 'core-contracts', 'go', 'security'],
    'contracts': ['python / python'],
    'sdk-python': ['python / python', 'package', 'pgvector'],
    'agent-runtime': ['python / python', 'image / image', 'langflow-image / image'],
    'pipeline-runner': ['python / python', 'image / image'],
    'serving': ['go / go', 'image / image'],
    'trace-proxy': ['go / go', 'image / image'],
    'workspace': ['python / python', 'jupyter / image', 'ide / image', 'langflow / image', 'langflow-sidecar / image'],
    'deploy': ['deploy', 'langflow-kind'],
    'docs': ['build', 'prose', 'diagrams', 'references'],
}
GUARDRAILS = ['guardrails / workflow-policy', 'guardrails / secrets', 'guardrails / dependency-review']


def api(method, path, body=None):
    command = ['gh', 'api', '--method', method, path]
    if body is not None:
        command += ['--input', '-']
    result = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                            text=True, capture_output=True, check=True)
    return json.loads(result.stdout) if result.stdout.strip() else None


def desired_rules(repo):
    return [{
        'name': 'Reviewed and verified default branch',
        'target': 'branch',
        'enforcement': 'active',
        'bypass_actors': [],
        'conditions': {'ref_name': {'include': ['~DEFAULT_BRANCH', 'refs/heads/main', 'refs/heads/master'], 'exclude': []}},
        'rules': [
            {'type': 'deletion'}, {'type': 'non_fast_forward'},
            {'type': 'pull_request', 'parameters': {
                'required_approving_review_count': 1,
                'dismiss_stale_reviews_on_push': True,
                'require_code_owner_review': True,
                'require_last_push_approval': True,
                'required_review_thread_resolution': True,
            }},
            {'type': 'required_status_checks', 'parameters': {
                'strict_required_status_checks_policy': True,
                'do_not_enforce_on_create': False,
                'required_status_checks': [{'context': name, 'integration_id': 15368}
                                           for name in GUARDRAILS + CHECKS[repo]],
            }},
            {'type': 'code_scanning', 'parameters': {'code_scanning_tools': [{
                'tool': 'CodeQL', 'security_alerts_threshold': 'medium_or_higher',
                'alerts_threshold': 'errors',
            }]}},
        ],
    }, {
        'name': 'Immutable release tags', 'target': 'tag', 'enforcement': 'active',
        'bypass_actors': [],
        'conditions': {'ref_name': {'include': ['refs/tags/v*'], 'exclude': []}},
        'rules': [{'type': 'deletion'}, {'type': 'non_fast_forward'}],
    }]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', choices=sorted(CHECKS))
    parser.add_argument('--apply', action='store_true', help='Write the managed rulesets to GitHub')
    args = parser.parse_args()
    rulesets = desired_rules(args.repository)
    if not args.apply:
        print(json.dumps(rulesets, indent=2))
        return
    path = f'repos/kiongahq/{args.repository}/rulesets'
    existing = api('GET', path + '?per_page=100')
    for desired in rulesets:
        matches = [item for item in existing if item['name'] == desired['name']]
        if len(matches) > 1:
            raise RuntimeError('Duplicate managed ruleset names; reconcile manually before applying')
        endpoint = path + '/' + str(matches[0]['id']) if matches else path
        actual = api('PUT' if matches else 'POST', endpoint, desired)
        verified = api('GET', path + '/' + str(actual['id']))
        for key in ('name', 'target', 'enforcement', 'conditions', 'bypass_actors'):
            if verified.get(key) != desired[key]:
                raise RuntimeError(f'Ruleset verification failed for {key}')
        for rule in desired['rules']:
            saved = next((item for item in verified['rules'] if item['type'] == rule['type']), None)
            if saved is None or any(saved.get('parameters', {}).get(key) != value
                                    for key, value in rule.get('parameters', {}).items()):
                raise RuntimeError(f'Ruleset verification failed for {rule["type"]}')
        print(f'{args.repository}: verified {actual["name"]} ({actual["id"]})')


if __name__ == '__main__':
    main()
