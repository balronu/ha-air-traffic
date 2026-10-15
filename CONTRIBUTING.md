# Contributing to Air Traffic

Thank you for helping improve Air Traffic. Contributions should preserve the
technical Home Assistant domain `air_traffic_merge` unless a separately tested
migration plan is approved.

## Before opening a pull request

- Read the README and the latest phase reports in `docs/`.
- Keep production Home Assistant, dashboards and user data out of the change.
- Do not commit API keys, tokens, private endpoints or personal location data.
- Add or update backend and frontend tests for behavior changes.
- Run the checks available locally:

```text
PYTHONPATH=custom_components/air_traffic_merge python3 -m unittest discover -s tests
cd frontend && npm ci && npm test && npm run build
python3 -m compileall -q custom_components tests
git diff --check -- . ':(exclude)custom_components/air_traffic_merge/frontend/air-traffic-card.js'
```

The generated frontend bundle must be committed after a source change. Hassfest,
HACS validation and secret scanning run in GitHub Actions and are release gates.

## Pull requests

Describe the user-visible change, compatibility impact, test results and any
blocked checks. Keep public branding as **Air Traffic** while retaining legacy
technical identifiers where required for existing installations.

## License

By contributing, you agree that your contribution is provided under the MIT
License in this repository.
