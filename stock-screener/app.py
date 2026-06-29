import os
import json
import pandas as pd

from screener import check_stock
from config import STOCKS

signals = []

for stock in STOCKS:

    result = check_stock(stock)

    if result:
        signals.append(result)

os.makedirs("output", exist_ok=True)

with open(
    "output/signals.json",
    "w"
) as f:
    json.dump(
        signals,
        f,
        indent=4
    )

pd.DataFrame(signals).to_csv(
    "output/signals.csv",
    index=False
)

print("Signals Generated")
print(signals)
