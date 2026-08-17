from app import read_report


def test_reads_report():
    assert read_report("reports/q1.txt") == "Q1 financial report\n"
