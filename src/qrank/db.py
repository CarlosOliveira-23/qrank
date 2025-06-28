def get_explain_plan(sql: str, engine: str, conn_str: str) -> str:
    if engine == "postgresql":
        import psycopg2
        conn = psycopg2.connect(conn_str)
        with conn.cursor() as cur:
            cur.execute("EXPLAIN " + sql)
            return "\n".join(row[0] for row in cur.fetchall())
    elif engine == "mysql":
        import mysql.connector
        conn = mysql.connector.connect(option_files=conn_str)
        cursor = conn.cursor()
        cursor.execute("EXPLAIN " + sql)
        return str(cursor.fetchall())
    else:
        raise ValueError("Unsupported engine: " + engine)