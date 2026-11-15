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
# Make copies for cleaning
equipment_clean = equipment_df.copy()
members_clean = members_df.copy()
rentals_clean = rentals_df.copy()

# Step 1: Remove rows with missing value
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


# Step 2: Remove duplicate rows
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
# Equipment and members no dates
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
# Parent tables unchanged
print("\n--- Equipment: reference validation ---")
print("Rows before this step:", len(equipment_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(equipment_clean))

print("\n--- Members: reference validation ---")
print("Rows before this step:", len(members_clean))
print("Rows removed:", 0)
print("Rows remaining:", len(members_clean))

# Keep rentals with existing references
print("\n--- Rentals: reference validation ---")
before = len(rentals_clean)
print("Rows before this step:", before)

rentals_clean = rentals_clean[
    rentals_clean["member_id"].isin(members_clean["member_id"])
    & rentals_clean["equipment_id"].isin(equipment_clean["equipment_id"])
].copy()

print("Rows removed:", before - len(rentals_clean))
print("Rows remaining:", len(rentals_clean))


# Step 6: Final row counts
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

# Q4
print("\n--- Q4 ---")
q4 = rentals_clean.loc[rentals_clean["quantity"] > 5, "rental_id"].count()
print(q4)


# Q5
print("\n--- Q5 ---")
q5 = equipment_clean["daily_rate"].mean()
print(f"{q5:.2f}")


# Q6
print("\n--- Q6 ---")
q6 = equipment_clean.loc[
    equipment_clean["daily_rate"] == equipment_clean["daily_rate"].max(),
    ["equipment_id", "equipment_name", "daily_rate"]
]
q6 = q6.sort_values("equipment_id")
print(q6.to_string(
    index=False,
    formatters={"daily_rate": "{:.2f}".format}
))


# Q7
print("\n--- Q7 ---")
q7 = equipment_clean.groupby("category").size().reset_index(
    name="equipment_count"
)
q7 = q7.sort_values("category")
print(q7.to_string(index=False))


# Q8
print("\n--- Q8 ---")
q8 = rentals_clean.loc[
    rentals_clean["rental_date"] > pd.Timestamp("2026-09-15"),
    "rental_id"
].count()
print(q8)


# Q9
print("\n--- Q9 ---")
rentals_equipment = rentals_clean.merge(
    equipment_clean,
    on="equipment_id",
    how="inner"
)
rentals_equipment["revenue"] = (
    rentals_equipment["quantity"]
    * rentals_equipment["rental_days"]
    * rentals_equipment["daily_rate"]
)

q9 = rentals_equipment.loc[
    rentals_equipment["rental_days"] > 3,
    "revenue"
].sum()
print(f"{q9:.2f}")


# Q10
print("\n--- Q10 ---")
rentals_members = rentals_clean.merge(
    members_clean,
    on="member_id",
    how="inner"
)
q10 = rentals_members.loc[
    (rentals_members["city"] == "Halifax")
    & (rentals_members["quantity"] >= 4),
    ["member_id", "member_name"]
]
q10 = q10.drop_duplicates().sort_values("member_id")
print(q10.to_string(index=False))


# Q11
print("\n--- Q11 ---")
q11 = rentals_members.loc[
    (rentals_members["city"] == "Montreal")
    & (rentals_members["rental_date"] >= pd.Timestamp("2026-09-01"))
    & (rentals_members["rental_date"] < pd.Timestamp("2026-10-01")),
    ["member_id", "member_name"]
]
q11 = q11.drop_duplicates().sort_values("member_id")
print(q11.to_string(index=False))


# Q12
print("\n--- Q12 ---")
q12 = (
    rentals_members.loc[rentals_members["city"] == "Ottawa"]
    .groupby(["member_id", "member_name"])["rental_id"]
    .count()
    .reset_index(name="rental_count")
)
q12 = q12.loc[q12["rental_count"] > 2]
q12 = q12.sort_values(
    ["rental_count", "member_id"],
    ascending=[False, True]
)
print(q12.to_string(index=False))


# Q13
print("\n--- Q13 ---")
q13 = (
    rentals_equipment
    .groupby(["equipment_id", "equipment_name"])["quantity"]
    .sum()
    .reset_index(name="total_units")
)
q13 = q13.sort_values(
    ["total_units", "equipment_id"],
    ascending=[False, True]
).head(3)
print(q13.to_string(index=False))


# Q14
print("\n--- Q14 ---")
rentals_details = rentals_equipment.merge(
    members_clean,
    on="member_id",
    how="inner"
)
q14 = (
    rentals_details
    .groupby(["member_id", "member_name"])["revenue"]
    .sum()
    .reset_index(name="total_spending")
)
q14 = q14.loc[
    q14["total_spending"] == q14["total_spending"].max()
]
q14 = q14.sort_values("member_id")
print(q14.to_string(
    index=False,
    formatters={"total_spending": "{:.2f}".format}
))


# Q15
print("\n--- Q15 ---")
q15 = (
    rentals_members
    .groupby("city")["rental_id"]
    .count()
    .reset_index(name="rental_count")
)
q15 = q15.loc[
    q15["rental_count"] == q15["rental_count"].max()
]
q15 = q15.sort_values("city")
print(q15.to_string(index=False))


# Q16
print("\n--- Q16 ---")
q16 = equipment_clean.loc[
    (equipment_clean["category"] == "Camping")
    & (~equipment_clean["equipment_id"].isin(
        rentals_clean["equipment_id"]
    )),
    ["equipment_id", "equipment_name"]
]
q16 = q16.sort_values("equipment_id")
print(q16.to_string(index=False))


# Q17
print("\n--- Q17 ---")
q17 = (
    rentals_clean
    .groupby(rentals_clean["rental_date"].dt.to_period("M"))["rental_id"]
    .count()
    .reset_index(name="rental_count")
    .rename(columns={"rental_date": "year_month"})
)
q17 = q17.sort_values("year_month")
print(q17.to_string(index=False))


# Q18
print("\n--- Q18 ---")
rentals_details["rental_label"] = "Standard"
rentals_details.loc[
    (rentals_details["revenue"] > 500)
    | (
        (rentals_details["quantity"] >= 4)
        & (rentals_details["city"] == "Montreal")
    ),
    "rental_label"
] = "High Value"
q18 = rentals_details.loc[
    rentals_details["rental_label"] == "High Value",
    ["member_id", "member_name"]
]
q18 = q18.drop_duplicates().sort_values("member_id")
print(q18.to_string(index=False))


# Q19
print("\n--- Q19 ---")
q19 = (
    rentals_details
    .groupby(["city", "member_id", "member_name"])["revenue"]
    .sum()
    .reset_index(name="total_spending")
)
q19 = q19.loc[
    q19["total_spending"]
    == q19.groupby("city")["total_spending"].transform("max")
]
q19 = q19.sort_values(["city", "member_id"])
print(q19.to_string(
    index=False,
    formatters={"total_spending": "{:.2f}".format}
))
