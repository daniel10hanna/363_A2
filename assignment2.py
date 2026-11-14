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


# Step 2: Remove exact duplicate rows
print("\n--- Equipment: exact duplicates ---")
before = len(equipment_clean)
print("Rows before this step:", before)
equipment_clean = equipment_clean.drop_duplicates(keep="first")
print("Rows removed:", before - len(equipment_clean))
print("Rows remaining:", len(equipment_clean))

print("\n--- Members: exact duplicates ---")
before = len(members_clean)
print("Rows before this step:", before)
members_clean = members_clean.drop_duplicates(keep="first")
print("Rows removed:", before - len(members_clean))
print("Rows remaining:", len(members_clean))

print("\n--- Rentals: exact duplicates ---")
before = len(rentals_clean)
print("Rows before this step:", before)
rentals_clean = rentals_clean.drop_duplicates(keep="first")
print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))


# Step 3: Validate numeric values
# Equipment
print("\n--- Equipment: numeric validation ---")
before = len(equipment_clean)
print("Rows before this step:", before)

for column in ["equipment_id", "daily_rate", "stock_quantity"]:
    equipment_clean[column] = pd.to_numeric(
        equipment_clean[column], errors="coerce"
    )

equipment_clean = equipment_clean[
    (equipment_clean["equipment_id"] > 0)
    & (equipment_clean["equipment_id"] % 1 == 0)
    & (equipment_clean["daily_rate"] >= 1)
    & (equipment_clean["stock_quantity"] >= 0)
    & (equipment_clean["stock_quantity"] % 1 == 0)
].copy()

print("Rows removed:", before - len(equipment_clean))
print("Rows remaining:", len(equipment_clean))

# Members
print("\n--- Members: numeric validation ---")
before = len(members_clean)
print("Rows before this step:", before)

members_clean["member_id"] = pd.to_numeric(
    members_clean["member_id"], errors="coerce"
)

members_clean = members_clean[
    (members_clean["member_id"] > 0)
    & (members_clean["member_id"] % 1 == 0)
].copy()

print("Rows removed:", before - len(members_clean))
print("Rows remaining:", len(members_clean))

# Rentals
print("\n--- Rentals: numeric validation ---")
before = len(rentals_clean)
print("Rows before this step:", before)

for column in [
    "rental_id", "member_id", "equipment_id", "quantity", "rental_days"
]:
    rentals_clean[column] = pd.to_numeric(
        rentals_clean[column], errors="coerce"
    )

rentals_clean = rentals_clean[
    (rentals_clean["rental_id"] > 0)
    & (rentals_clean["rental_id"] % 1 == 0)
    & (rentals_clean["member_id"] > 0)
    & (rentals_clean["member_id"] % 1 == 0)
    & (rentals_clean["equipment_id"] > 0)
    & (rentals_clean["equipment_id"] % 1 == 0)
    & (rentals_clean["quantity"] > 0)
    & (rentals_clean["quantity"] % 1 == 0)
    & (rentals_clean["rental_days"] > 0)
    & (rentals_clean["rental_days"] % 1 == 0)
].copy()

print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))



# Step 4: Validate rental dates
# Equipment and members have no date columns to validate
print("\n--- Equipment: date validation ---")
print("Rows before this step:", len(equipment_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(equipment_clean))

print("\n--- Members: date validation ---")
print("Rows before this step:", len(members_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(members_clean))

# Validate dates in rentals
print("\n--- Rentals: date validation ---")
before = len(rentals_clean)
print("Rows before this step:", before)

rentals_clean["rental_date"] = pd.to_datetime(
    rentals_clean["rental_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

rentals_clean = rentals_clean.dropna(subset=["rental_date"]).copy()

print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))
