import click
from qrank.analyzer import QRankAnalyzer


@click.command()
@click.argument("file", required=False)
@click.option("-c", "--command", help="SQL command to analyze")
@click.option("--engine", default="postgresql", help="Database engine: postgresql or mysql")
@click.option("--conn", default="", help="Database connection string")
@click.option("--verbose", is_flag=True, help="Show detailed feedback")
def main(file, command, engine, conn, verbose):
    """
    Analyze SQL performance and return a score and recommendations.
    """
    analyzer = QRankAnalyzer(engine=engine, connection_string=conn)

    sql = command
    if file:
        with open(file, "r") as f:
            sql = f.read()

    if not sql:
        print("Please provide either a SQL file or use the -c option.")
        return

    score, suggestions = analyzer.analyze(sql)
    print(f"Query Score: {score}/100")

    if verbose:
        print("\nRecommendations:")
        for suggestion in suggestions:
            print(f" - {suggestion}")


if __name__ == "__main__":
    main()
