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


#Task 2: Data cleaning
# Make separate copies for cleaning
equipment_clean = equipment_df.copy()
members_clean = members_df.copy()
rentals_clean = rentals_df.copy()

# Step 1: Remove rows with any missing value
print("\n--- Equipment: missing values ---")
before = len(equipment_clean)
print("Initial row count:", before)
equipment_clean = equipment_clean.dropna()
print("Rows removed:", before - len(equipment_clean))
print("Rows remaining:", len(equipment_clean))

print("\n--- Members: missing values ---")
before = len(members_clean)
print("Initial row count:", before)
members_clean = members_clean.dropna()
print("Rows removed:", before - len(members_clean))
print("Rows remaining:", len(members_clean))

print("\n--- Rentals: missing values ---")
before = len(rentals_clean)
print("Initial row count:", before)
rentals_clean = rentals_clean.dropna()
print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))