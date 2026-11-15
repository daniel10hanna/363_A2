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


# Step 5: Validate rental references
# Parent tables stay unchanged during this step
print("\n--- Equipment: reference validation ---")
print("Rows before this step:", len(equipment_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(equipment_clean))

print("\n--- Members: reference validation ---")
print("Rows before this step:", len(members_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(members_clean))

# Keep rentals only when both references exist
print("\n--- Rentals: reference validation ---")
before = len(rentals_clean)
print("Rows before this step:", before)

rentals_clean = rentals_clean[
    rentals_clean["member_id"].isin(members_clean["member_id"])
    & rentals_clean["equipment_id"].isin(equipment_clean["equipment_id"])
].copy()

print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))


# Step 6: Final row counts and primary-key uniqueness
print("\n--- Equipment: final checks ---")
print("Final row count:", len(equipment_clean))
print("equipment_id is unique:", equipment_clean["equipment_id"].is_unique)

print("\n--- Members: final checks ---")
print("Final row count:", len(members_clean))
print("member_id is unique:", members_clean["member_id"].is_unique)

print("\n--- Rentals: final checks ---")
print("Final row count:", len(rentals_clean))
print("rental_id is unique:", rentals_clean["rental_id"].is_unique)



# Task 3: Pandas queries

# Q1
print("\n--- Q1 ---")
q1 = equipment_clean.loc[
    equipment_clean["daily_rate"] > 40,
    ["equipment_id", "equipment_name"]
]
q1 = q1.sort_values("equipment_id")
print(q1.to_string(index=False))


# Q2
print("\n--- Q2 ---")
q2 = members_clean.loc[
    members_clean["city"] == "Montreal",
    ["member_id", "member_name"]
]
q2 = q2.sort_values("member_id")
print(q2.to_string(index=False))


# Q3
print("\n--- Q3 ---")
q3 = len(members_clean)
print(q3)