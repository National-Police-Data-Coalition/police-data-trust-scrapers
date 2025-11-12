import pandas as pd
from officers import AddEmployment, CreateOfficer

# Define file paths for the CSV files
texas_file_path = "path_to_texas_data.csv"
california_file_path = "path_to_california_data.csv"

# Load data from CSV files
texas_data = pd.read_csv(texas_file_path)
california_data = pd.read_csv(california_file_path)


# Function to transform Texas data to Officer and Employment models
def process_texas_data(data):
    officers = {}
    employments = []

    for _, row in data.iterrows():
        person_uid = row["person_nbr"]
        if person_uid not in officers:
            officers[person_uid] = CreateOfficer(
                first_name=row["first_name"],
                middle_name=row["middle_name"],
                last_name=row["last_name"],
                suffix=row.get("suffix"),
                date_of_birth=f"{row['year_of_birth']}-01-01",
            )

        employment = AddEmployment(
            officer_uid=person_uid,
            agency_uid=None,  # Assuming agency_uid needs to be resolved separately
            start_date=row["start_date"],
            end_date=row["end_date"],
            highest_rank=row["rank"],
        )
        employments.append(employment)

    return officers, employments


# Function to transform California data to Officer and Employment models
def process_california_data(data):
    officers = {}
    employments = []

    for _, row in data.iterrows():
        person_uid = row["person_nbr"]
        if person_uid not in officers:
            officers[person_uid] = CreateOfficer(
                first_name=row["first_name"],
                middle_name=row["middle_name"],
                last_name=row["last_name"],
                suffix=row.get("suffix"),
            )

        employment = AddEmployment(
            officer_uid=person_uid,
            agency_uid=None,  # Assuming agency_uid needs to be resolved separately
            start_date=row["start_date"],
            end_date=row["end_date"],
            highest_rank=row["rank"],
        )
        employments.append(employment)

    return officers, employments


# Process the data
texas_officers, texas_employments = process_texas_data(texas_data)
california_officers, california_employments = process_california_data(california_data)

# Combine results
all_officers = {**texas_officers, **california_officers}
all_employments = texas_employments + california_employments

# Print results for verification
print(f"Total officers processed: {len(all_officers)}")
print(f"Total employment records processed: {len(all_employments)}")

# Example: Accessing a specific officer
example_officer_id = next(iter(all_officers))
print(all_officers[example_officer_id])

# Example: Accessing a specific employment record
print(all_employments[0])
