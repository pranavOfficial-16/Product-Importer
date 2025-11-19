import csv

with open("big_products.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sku", "name", "description", "price"])

    for i in range(500_000):
        sku = f"SKU{i}"
        name = f"Product {i}"
        desc = f"Description {i}"
        price = round(10 + (i % 100) * 0.5, 2)

        writer.writerow([sku, name, desc, price])

print("Generated 500k CSV!")
