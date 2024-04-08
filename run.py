import pandas as pd
from staffsignup.models import StudentDetails, Branch
import re
def extract_phone_number(raw_number):
    if pd.notnull(raw_number):
        raw_number_str = str(raw_number)
        if '.' in raw_number_str:
            # If raw number is a floating-point number, remove the decimal part
            raw_number_str = raw_number_str.split('.')[0]
        digits_only = re.sub(r'\D', '', raw_number_str)
        if len(digits_only) >= 10:
            last_10_digits = digits_only[-10:]
            return last_10_digits
    return None

def process_excel_file(excel_file_path):
    try:
        df = pd.read_excel(excel_file_path)
        success_count = 0
        update_count = 0
        error_count = 0
        batch_size = 1000  # Set your preferred batch size
        processed_count = 0  # Counter for the number of processed students

        for start_index in range(0, len(df), batch_size):
            batch_df = df[start_index:start_index+batch_size]
            for index, row in batch_df.iterrows():
                # Check if we have processed 1000 students
                if processed_count >= 1000:
                    break

                pincode = row["PIN Code"]
                if pd.notnull(pincode):
                    pincode = int(pincode) if isinstance(pincode, float) else pincode
                dob = row["Date Of Birth"]
                if pd.notnull(dob) and not pd.isna(dob):
                    dob = row["Date Of Birth"]
                else:
                    dob = None
                branch_name = row["Branch_id"]
                try:
                    branch = Branch.objects.get(Name=branch_name)
                    branch_id = branch.id
                except Branch.DoesNotExist:
                    branch_id = None
                missing_fields = ["Registration Number", "Roll number", "Primary Mobile Number", 
                                  "Student's Name", "Primary Mobile Number", "Course", 
                                  "Course ID", "Batch", "Exam", "Branch_id"]
                if any(pd.isnull(row[field]) for field in missing_fields):
                    error_count += 1
                    continue

                roll_number = row["Roll number"]
                existing_student = StudentDetails.objects.filter(CoachingRoll=roll_number).first()

                if existing_student:
                    # Update the existing student record
                    try:
                        existing_student.CoachingRegisteration = row["Registration Number"]
                        existing_student.Name = row["Student's Name"]
                        existing_student.FatherName = row["Father's Name"]
                        existing_student.MotherName = row["Mother's Name"]
                        existing_student.PrimaryNumber = extract_phone_number(row["Primary Mobile Number"])
                        existing_student.SecondaryNumber = extract_phone_number(row["Secondary Mobile Number"])
                        existing_student.AdditionalNumber = extract_phone_number(row["Addition Mobile Number"])
                        existing_student.WhatsappNumber = extract_phone_number(row["WhatsApp Number"])
                        existing_student.Course = row["Course"]
                        existing_student.CourseId = row["Course ID"]
                        existing_student.Batch = row["Batch"]
                        existing_student.Medium = row["Medium"]
                        existing_student.DOB = dob
                        existing_student.Gender = row["Gender"]
                        existing_student.Category = row["Category"]
                        existing_student.Address = row["Permanent Address"]
                        existing_student.Tehsil = row["Tehsil"]
                        existing_student.District = row["District"]
                        existing_student.State = row["State"]
                        existing_student.Pincode = pincode
                        existing_student.PreviousRoll = row["Previous GCI Roll Number"]
                        existing_student.Exam = row["Exam"]
                        existing_student.Branch_id = branch_id
                        existing_student.save()
                        update_count += 1
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"Error updating row {index + 1}: {str(e)}")
                else:
                    # Create a new student record
                    try:
                        student = StudentDetails.objects.create(
                            CoachingRegisteration=row["Registration Number"],
                            CoachingRoll=roll_number,
                            Name=row["Student's Name"],
                            FatherName=row["Father's Name"],
                            MotherName=row["Mother's Name"],
                            PrimaryNumber=extract_phone_number(row["Primary Mobile Number"]),
                            SecondaryNumber=extract_phone_number(row["Secondary Mobile Number"]),
                            AdditionalNumber=extract_phone_number(row["Addition Mobile Number"]),
                            WhatsappNumber=extract_phone_number(row["WhatsApp Number"]),
                            Course=row["Course"],
                            CourseId=row["Course ID"],
                            Batch=row["Batch"],
                            Medium=row["Medium"],
                            DOB=dob,
                            Gender=row["Gender"],
                            Category=row["Category"],
                            Address=row["Permanent Address"],
                            Tehsil=row["Tehsil"],
                            District=row["District"],
                            State=row["State"],
                            Pincode=pincode,
                            PreviousRoll=row["Previous GCI Roll Number"],
                            Exam=row["Exam"],
                            Branch_id=branch_id,
                        )
                        success_count += 1
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"Error processing row {index + 1}: {str(e)}")

        print(f"Processed {processed_count} rows.")
        print(f"{success_count} student(s) added successfully.")
        print(f"{update_count} student(s) updated successfully.")
        print(f"{error_count} student(s) encountered errors.")

    except Exception as e:
        error_count += 1
        print(f"Error processing row {index + 1}: {str(e)}")



# Provide the path to your Excel file on the server
excel_file_path = "neet & JEE - all data (1).xlsx"

# Call the function to process the Excel file
process_excel_file(excel_file_path)
