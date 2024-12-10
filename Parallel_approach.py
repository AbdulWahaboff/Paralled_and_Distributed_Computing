import pandas as pd
from concurrent.futures import ProcessPoolExecutor

students_df = pd.read_csv('C:\\Users\\abcd\\Downloads\\21b-156-cs_PDC_Assignment\\students.csv')
fees_df = pd.read_csv('C:\\Users\\abcd\\Downloads\\21b-156-cs_PDC_Assignment\\fees.csv')

students_df["student_id"] = students_df["student_id"].astype(str).str.strip().astype(int)
fees_df["student_id"] = fees_df["student_id"].astype(str).str.strip().astype(int)

print("Unique Student IDs in students_df:", students_df["student_id"].unique())
print("Unique Student IDs in fees_df:", fees_df["student_id"].unique())

def find_most_relevant_fee_date(group):
    return group["fee_submission_date"].mode().iloc[0]  

relevant_dates_mapping = fees_df.groupby("student_id").apply(find_most_relevant_fee_date).reset_index()
relevant_dates_mapping.columns = ["student_id", "most_relevant_date"]

def process_student(student):
    student_id = student["student_id"]
    relevant_date = relevant_dates_mapping.loc[relevant_dates_mapping["student_id"] == student_id, "most_relevant_date"]
    if not relevant_date.empty:
        return f"Student ID {student_id}: Most relevant fee submission date: {relevant_date.iloc[0]}"
    return f"Student ID {student_id}: No fee records found."

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_student, students_df.to_dict("records"))
    print("\n".join(results))
