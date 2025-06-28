from qrank.analyzer import QRankAnalyzer


def test_scoring_mock():
    analyzer = QRankAnalyzer()
    score, feedback = analyzer.score_plan("Seq Scan on tabela -> Nested Loop")
    assert score < 100
    assert any("índices" in s.lower() or "nested" in s.lower() for s in feedback)
    