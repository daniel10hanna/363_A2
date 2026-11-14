#Task 1: Data loading
import pandas as pd

equipment_df = pd.read_csv("Tables/equipment.csv")
members_df = pd.read_excel("Tables/members.xlsx", engine="openpyxl")
rentals_df = pd.read_csv("Tables/rentals.txt")

print("\n--- Equipment: first five rows ---")
print(equipment_df.head().to_string(index=False))
print("\n--- Equipment: structure ---")
equipment_df.info()

print("\n--- Members: first five rows ---")
print(members_df.head().to_string(index=False))
print("\n--- Members: structure ---")
members_df.info()

print("\n--- Rentals: first five rows ---")
print(rentals_df.head().to_string(index=False))
print("\n--- Rentals: structure ---")
rentals_df.info()