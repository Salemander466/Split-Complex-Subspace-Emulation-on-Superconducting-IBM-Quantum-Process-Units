import json
from pathlib import Path


def test_validation_catalog_has_17_formal_tests():
    data = json.loads(Path('results/validation_results.json').read_text())
    assert len(data) == 17
    assert {item['id'] for item in data} == set(range(1, 18))
