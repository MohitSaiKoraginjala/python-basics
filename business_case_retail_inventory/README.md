# Retail inventory business case

## Business problem

A small retail company has one month of product sales and a snapshot of current stock. Managers need a quick way to see sales performance, the cost value of stock on shelves, and which products need attention.

## Project objective

Read `data/products.csv`, calculate revenue and gross profit, rank categories and products by gross profit, identify low stock and overstock, recommend replenishment quantities, and write a product-level CSV report. The sample data is illustrative, not actual company data.

**Rules:** Revenue = unit price × units sold. Gross profit = (unit price − unit cost) × units sold; it excludes rent, labor, taxes, and other operating expenses. Inventory value = unit cost × current stock on hand. A product is marked **Reorder** when stock on hand is at or below its reorder point; its recommended quantity is `target_stock - stock_on_hand`. A product is **Overstocked** when stock exceeds target stock. All other products are **Healthy**. Reorder takes priority over other statuses.

## Python concepts used

Variables, `if`/`else` conditions, loops, lists, dictionaries, functions, CSV reading and writing, exception handling, list comprehensions, sorting with `lambda`, a `dataclass`, and type hints.

## Run

Requires Python 3.9 or newer. No third-party packages are needed. From this directory:

```bash
python main.py
```

On Windows, `py main.py` also works. The script resolves file paths relative to `main.py`, so it can also be run from another directory.

## Expected output

The console shows total revenue, total gross profit, current inventory value at cost, categories ranked by gross profit, the top three products by gross profit, reorder recommendations, and overstocked products. It also writes `output/analysis_report.csv` with one row per product, sorted by gross profit. The report includes sales figures, inventory value, stock status, and reorder quantity. Rerunning the script replaces the report with results from the current input CSV.

Try the exercises in [CHALLENGE.md](CHALLENGE.md) before studying the solution in `main.py`.
