import csv

with open ("problems.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows([[i, "_"] for i in range(100)])