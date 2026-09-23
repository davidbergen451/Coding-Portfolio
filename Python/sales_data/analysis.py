import csv
from collections import defaultdict

FILE_NAME = "sales_data.csv"


def load_sales():
    sales = []
    with open(FILE_NAME, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Quantity"] = int(row["Quantity"])
            row["UnitPrice"] = float(row["UnitPrice"])
            row["TotalSales"] = row["Quantity"] * row["UnitPrice"]
            sales.append(row)
    return sales


def main():
    sales = load_sales()

    total_revenue = sum(row["TotalSales"] for row in sales)
    total_units = sum(row["Quantity"] for row in sales)
    average_order_value = total_revenue / len(sales)

    product_sales = defaultdict(float)
    region_sales = defaultdict(float)
    monthly_sales = defaultdict(float)

    for row in sales:
        product_sales[row["Product"]] += row["TotalSales"]
        region_sales[row["Region"]] += row["TotalSales"]
        monthly_sales[row["Date"][:7]] += row["TotalSales"]

    best_product = max(product_sales, key=product_sales.get)
    best_region = max(region_sales, key=region_sales.get)
    best_month = max(monthly_sales, key=monthly_sales.get)

    print("=" * 50)
    print("SALES DATA ANALYSIS")
    print("=" * 50)
    print(f"Number of orders: {len(sales)}")
    print(f"Units sold:       {total_units}")
    print(f"Total revenue:    ${total_revenue:,.2f}")
    print(f"Average order:    ${average_order_value:,.2f}")

    print("\nSALES BY PRODUCT")
    for product, amount in sorted(product_sales.items(), key=lambda x: x[1], reverse=True):
        print(f"{product:<12} ${amount:,.2f}")

    print("\nSALES BY REGION")
    for region, amount in sorted(region_sales.items(), key=lambda x: x[1], reverse=True):
        print(f"{region:<12} ${amount:,.2f}")

    print("\nSALES BY MONTH")
    for month, amount in sorted(monthly_sales.items()):
        print(f"{month:<12} ${amount:,.2f}")

    print("\nKEY INSIGHTS")
    print(f"Top product: {best_product}")
    print(f"Top region:  {best_region}")
    print(f"Top month:   {best_month}")


if __name__ == "__main__":
    main()
