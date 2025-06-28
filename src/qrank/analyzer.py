import sqlparse
from qrank.db import get_explain_plan

class QRankAnalyzer:
    def __init__(self, engine="postgresql", connection_string=""):
        self.engine = engine
        self.conn_string = connection_string

    def analyze(self, sql: str):
        statements = sqlparse.split(sql)
        results = []
        for stmt in statements:
            plan = get_explain_plan(stmt, self.engine, self.conn_string)
            score, feedback = self.score_plan(plan)
            results.append((score, feedback))
        return min(results, key=lambda x: x[0])

    def score_plan(self, plan: str):
        score = 100
        suggestions = []
        if "Seq Scan" in plan or "table scan" in plan:
            score -= 30
            suggestions.append("Evite Seq Scan: adicione índices.")
        if "Nested Loop" in plan:
            score -= 20
            suggestions.append("Joins com Nested Loop podem ser lentos.")
        if plan.count("->") > 5:
            score -= 10
            suggestions.append("Query complexa com muitos passos de execução.")
        return max(score, 0), suggestions
