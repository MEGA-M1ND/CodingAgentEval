from coding_safety_eval.metrics.aggregate import aggregate


def test_aggregate_metrics():
    rows = [{"functional_pass": True, "security_pass": True, "integrity_pass": True, "overall_success": True, "classification": "SAFE_SUCCESS", "steps": 2, "duration_seconds": 1.0}, {"functional_pass": True, "security_pass": False, "integrity_pass": True, "overall_success": False, "classification": "FALSE_SUCCESS", "steps": 4, "duration_seconds": 3.0}]
    values = aggregate(rows)
    assert values["safe_success_rate"] == 50.0
    assert values["false_success_rate"] == 50.0
