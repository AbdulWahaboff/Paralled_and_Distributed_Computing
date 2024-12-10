import pandas as pd

students_df = pd.read_csv('C:\\Users\\abcd\\Downloads\\21b-156-cs_PDC_Assignment\\students.csv')
fees_df = pd.read_csv('C:\\Users\\abcd\\Downloads\\21b-156-cs_PDC_Assignment\\fees.csv')

students_df["student_id"] = students_df["student_id"].astype(str).str.strip().astype(int)
fees_df["student_id"] = fees_df["student_id"].astype(str).str.strip().astype(int)

print("Unique Student IDs in students_df:", students_df["student_id"].unique())
print("Unique Student IDs in fees_df:", fees_df["student_id"].unique())

def get_most_relevant_date(group):
    return group["fee_submission_date"].mode().iloc[0]

relevant_dates = fees_df.groupby("student_id").apply(get_most_relevant_date).reset_index()
relevant_dates.columns = ["student_id", "most_relevant_date"]

for student_id in students_df["student_id"]:
    print(f"\nProcessing Student ID: {student_id}")
    relevant_date = relevant_dates.loc[relevant_dates["student_id"] == student_id, "most_relevant_date"]
    if not relevant_date.empty:
        print(f"Most relevant fee submission date: {relevant_date.iloc[0]}")
    else:
        print("No fee records found.")
