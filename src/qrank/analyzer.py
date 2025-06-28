import re
import sqlparse
from qrank.db import get_explain_plan


class QRankAnalyzer:
    def __init__(self, engine="postgresql", connection_string=""):
        self.engine = engine
        self.connection_string = connection_string

    def analyze(self, sql: str):
        """
        Analyzes one or more SQL statements and returns the lowest score found,
        along with suggestions to improve the query.
        """
        statements = sqlparse.split(sql)
        results = []
        for stmt in statements:
            plan = get_explain_plan(stmt, self.engine, self.connection_string)
            score, feedback = self._score_plan(plan, stmt)
            results.append((score, feedback))
        return min(results, key=lambda x: x[0])

    def _score_plan(self, plan: str, raw_sql: str):
        """
        Scores a query based on its execution plan and raw SQL structure.
        Returns a score (0-100) and a list of suggestions.
        """
        score = 100
        suggestions = []

        # Heuristics based on EXPLAIN plan
        if "Seq Scan" in plan or "table scan" in plan.lower():
            score -= 30
            suggestions.append("Avoid sequential scans: consider adding indexes.")

        if "Nested Loop" in plan:
            score -= 20
            suggestions.append("Nested Loop joins can be slow on large datasets.")

        if plan.count("->") > 5:
            score -= 10
            suggestions.append("Query has a complex execution plan with many steps.")

        # Heuristics based on raw SQL content
        sql_lower = raw_sql.lower()

        if "select *" in sql_lower:
            score -= 10
            suggestions.append("Avoid SELECT *: specify only the required columns.")

        if "limit" not in sql_lower:
            score -= 15
            suggestions.append("Consider using LIMIT to reduce scanned rows.")

        if sql_lower.count(" join ") >= 3:
            score -= 10
            suggestions.append("Too many JOINs can hurt performance. Consider refactoring.")

        if re.search(r"\bor\b\s+\w+\s*=", sql_lower):
            score -= 10
            suggestions.append("Avoid OR in filters: use IN or split queries when possible.")

        if re.search(r"\(.*select", sql_lower, re.DOTALL):
            score -= 5
            suggestions.append("Subqueries detected. Prefer JOINs or CTEs when possible.")

        return max(score, 0), suggestions
