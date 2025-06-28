import click
from qrank.analyzer import QRankAnalyzer

@click.command()
@click.argument("file", required=False)
@click.option("-c", "--command", help="SQL command to analyze")
@click.option("--engine", default="postgresql", help="Database engine: postgresql or mysql")
@click.option("--conn", default="", help="Database connection string")
def main(file, command, engine, conn):
    analyzer = QRankAnalyzer(engine=engine, connection_string=conn)
    sql = command
    if file:
        with open(file, "r") as f:
            sql = f.read()
    if not sql:
        print("Provide either a file or a SQL command.")
        return
    score, suggestions = analyzer.analyze(sql)
    print(f"Score: {score}/100")
    for s in suggestions:
        print(f"- {s}")

if __name__ == "__main__":
    main()