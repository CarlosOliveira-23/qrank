# QRank

**QRank** é uma ferramenta de linha de comando e biblioteca Python para analisar e ranquear queries SQL com base em eficiência, uso de índices, joins excessivos e sugestões de melhoria.

## Instalação

```bash
pip install .
```

## Uso via CLI

```bash
qrank -c "SELECT * FROM usuarios WHERE ativo = true"
qrank arquivo.sql
```

## Uso como biblioteca

```python
from qrank.analyzer import QRankAnalyzer

analyzer = QRankAnalyzer(engine="postgresql", connection_string="dbname=meubanco user=postgres")
score, feedback = analyzer.analyze("SELECT * FROM usuarios")
print(score, feedback)
```