"""Analyze one month's retail sales and current inventory from a CSV file."""

import csv
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "products.csv"
REPORT_FILE = BASE_DIR / "output" / "analysis_report.csv"


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_cost: float
    unit_price: float
    units_sold: int
    stock_on_hand: int
    reorder_point: int
    target_stock: int

    @property
    def revenue(self) -> float:
        return self.unit_price * self.units_sold

    @property
    def gross_profit(self) -> float:
        return (self.unit_price - self.unit_cost) * self.units_sold

    @property
    def inventory_value(self) -> float:
        return self.unit_cost * self.stock_on_hand

    @property
    def reorder_quantity(self) -> int:
        # Refill to the target only when stock reaches the reorder point.
        return max(0, self.target_stock - self.stock_on_hand) if self.stock_on_hand <= self.reorder_point else 0

    @property
    def stock_status(self) -> str:
        if self.stock_on_hand <= self.reorder_point:
            return "Reorder"
        if self.stock_on_hand > self.target_stock:
            return "Overstocked"
        return "Healthy"


def load_products(path: Path) -> list[Product]:
    """Read products and give a useful error for invalid input rows."""
    products = []
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = set(Product.__dataclass_fields__)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain these columns: {', '.join(sorted(required))}")

        for row_number, row in enumerate(reader, start=2):
            try:
                product = Product(
                    sku=row["sku"].strip(),
                    name=row["name"].strip(),
                    category=row["category"].strip(),
                    unit_cost=float(row["unit_cost"]),
                    unit_price=float(row["unit_price"]),
                    units_sold=int(row["units_sold"]),
                    stock_on_hand=int(row["stock_on_hand"]),
                    reorder_point=int(row["reorder_point"]),
                    target_stock=int(row["target_stock"]),
                )
                if not all((product.sku, product.name, product.category)):
                    raise ValueError("sku, name, and category cannot be blank")
                if min(product.unit_cost, product.unit_price, product.units_sold,
                       product.stock_on_hand, product.reorder_point, product.target_stock) < 0:
                    raise ValueError("numeric values cannot be negative")
                if product.target_stock <= product.reorder_point:
                    raise ValueError("target_stock must exceed reorder_point")
                products.append(product)
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(f"Invalid data on CSV row {row_number}: {error}") from error
    if not products:
        raise ValueError("The products CSV has no data rows")
    return products


def write_report(products: list[Product], path: Path) -> None:
    """Save one row per product, ordered by gross profit (highest first)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sku", "name", "category", "units_sold", "stock_on_hand",
                  "revenue", "gross_profit", "inventory_value", "stock_status", "reorder_quantity"]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in sorted(products, key=lambda item: item.gross_profit, reverse=True):
            writer.writerow({
                "sku": product.sku,
                "name": product.name,
                "category": product.category,
                "units_sold": product.units_sold,
                "stock_on_hand": product.stock_on_hand,
                "revenue": f"{product.revenue:.2f}",
                "gross_profit": f"{product.gross_profit:.2f}",
                "inventory_value": f"{product.inventory_value:.2f}",
                "stock_status": product.stock_status,
                "reorder_quantity": product.reorder_quantity,
            })


def print_summary(products: list[Product]) -> None:
    total_revenue = sum(product.revenue for product in products)
    total_profit = sum(product.gross_profit for product in products)
    inventory_value = sum(product.inventory_value for product in products)
    reorder = [product for product in products if product.reorder_quantity > 0]
    overstocked = [product for product in products if product.stock_status == "Overstocked"]

    category_profit: dict[str, float] = {}
    for product in products:
        category_profit[product.category] = category_profit.get(product.category, 0) + product.gross_profit

    print("RETAIL INVENTORY ANALYSIS (sample month)")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Total gross profit: ${total_profit:,.2f}")
    print(f"Current inventory value (at cost): ${inventory_value:,.2f}")
    print("\nCategories by gross profit:")
    for category, profit in sorted(category_profit.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: ${profit:,.2f}")
    print("\nTop 3 products by gross profit:")
    for product in sorted(products, key=lambda item: item.gross_profit, reverse=True)[:3]:
        print(f"  {product.name}: ${product.gross_profit:,.2f}")
    print("\nReorder recommendations (stock at or below reorder point):")
    for product in reorder:
        print(f"  {product.name}: order {product.reorder_quantity} units")
    if not reorder:
        print("  None")
    print("\nOverstocked products (stock above target):")
    for product in overstocked:
        print(f"  {product.name}: {product.stock_on_hand} units on hand")
    if not overstocked:
        print("  None")


def main() -> None:
    try:
        products = load_products(INPUT_FILE)
        write_report(products, REPORT_FILE)
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error
    print_summary(products)
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
