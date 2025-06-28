from qrank.analyzer import QRankAnalyzer


def test_scoring_mock():
    analyzer = QRankAnalyzer()
    score, feedback = analyzer._score_plan("Seq Scan on tabela -> Nested Loop", "SELECT * FROM tabela")
    assert score < 100
    assert any("índices" in s.lower() or "nested" in s.lower() for s in feedback)
