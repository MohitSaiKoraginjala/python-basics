# Retail inventory challenge

Try building your own `main.py` before reading the provided solution. Use only Python's standard library and the sample CSV in `data/products.csv`.

1. Read the CSV with `csv.DictReader`. Convert the numeric columns to `int` or `float`. What should happen if a file is missing or a number is invalid?
2. Store each product as a dictionary or a simple dataclass. Write functions to calculate its revenue, gross profit, and current inventory value at cost.
3. Use a loop to total revenue and gross profit across all products. Check your calculations by hand for one row.
4. Use `if`/`else` to label a product **Reorder**, **Overstocked**, or **Healthy**. Set the reorder quantity to the number needed to reach target stock, but only when stock is at or below the reorder point.
5. Make a list of products that need reordering and a separate list of overstocked products. Print their names and relevant quantities.
6. Accumulate gross profit by category in a dictionary. Which category ranks first? Sort it with `sorted()` and a `lambda` key.
7. Sort products by gross profit and print the top three. Then write a product-level CSV report in `output/`.

**Stretch ideas:** Add gross margin percentage, identify the product with the slowest sales, or compare inventory value by category. Decide how your program should handle duplicate SKUs and test that rule.
