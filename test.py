import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

employees_name = ['Raanan_shein', 'Christina_shein', 'Tomma_shein']
# Dropdown for selecting user name
employee_name = st.selectbox("Enter your name:", options=employees_name)
selected_month = st.selectbox("Select the month:", options=range(1, 13))

# Define filename for data storage
data_file = "may_swap_1.csv"

# Function to load data from CSV
def load_data():
    try:
        df_base = pd.read_csv(data_file)
    except FileNotFoundError:
        df_base = pd.DataFrame(columns=['date','employee_name','give_away','can_take_early','can_take_morning','can_take_evening',
                                   'can_take_night','can_take_rest'])
    return df_base

# Function to save data to CSV
def save_data(df_base):
    df_base.to_csv(data_file, index=False)

def generate_dates(year, month):
    # Define the start date for the given month and year
    start_date = datetime(year, month, 1)

    # Calculate the number of days in the given month
    if month == 12:
        num_days = (datetime(year + 1, 1, 1) - start_date).days
    else:
        num_days = (datetime(year, month + 1, 1) - start_date).days

    # Generate a list of dates for the given month and year
    dates_list = [start_date + timedelta(days=i) for i in range(num_days)]

    # Convert the dates to strings
    dates_list = [date.strftime('%Y-%m-%d') for date in dates_list]

    return dates_list

# Function to find matches for shift swapping
def find_matches(df):
    matches = []

    # Iterate through each pair of employees
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            # Get the shifts for each pair of employees
            shift_employee1 = df.iloc[i]
            shift_employee2 = df.iloc[j]

            # Check if the shifts are on the same date
            if shift_employee1['date'] == shift_employee2['date']:
                if shift_employee1['employee_name'] != shift_employee2['employee_name']:
                # Check if any of the shifts of employee1 match with any of the shifts of employee2
                    if shift_employee1['give_away'] in shift_employee2[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                        if shift_employee2['give_away'] in shift_employee1[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                            # If there's a match, store the information
                            matches.append((shift_employee1['employee_name'], shift_employee2['employee_name'], shift_employee1['date'], shift_employee1['give_away'],
                                            shift_employee2['give_away']))
    return matches

# Load data before displaying the app
df_base = load_data()

# Display the data editor
st.write("Shift Swap Submission Form")
df = pd.DataFrame(columns=['date','employee_name','give_away','can_take_early','can_take_morning','can_take_evening',
                            'can_take_night','can_take_rest'])
shifts = ['early', 'morning', 'evening', 'night', 'rest', None]
config = {
    'date' : st.column_config.SelectboxColumn('date', width='small',options=generate_dates(2024, selected_month)),
    'employee_name' : st.column_config.SelectboxColumn('Employee name',options=employees_name),
    'give_away' : st.column_config.SelectboxColumn('Give Away', options=shifts),
    'can_take_early' : st.column_config.SelectboxColumn('Can Take Early', options=['early',None]),
    'can_take_morning' : st.column_config.SelectboxColumn('Can Take Morning', options=['morning',None]),
    'can_take_evening' : st.column_config.SelectboxColumn('Can Take Evening', options=['evening',None]),
    'can_take_night' : st.column_config.SelectboxColumn('Can Take Night', options=['night',None]),
    'can_take_rest' : st.column_config.SelectboxColumn('Can Take Rest', options=['rest',None])
}

result = st.data_editor(df, column_config=config, num_rows='dynamic', hide_index=True)

# Initialize matches variable as an empty list
matches = []

# Check for submission
# Save data after submission
if st.button("Submit"):
    st.write("Data submitted!")
    save_data(result)
    st.write(df_base)        
    # Find matches among all users
    matches = find_matches(result)
    

# Display matches for the selected employee name
if matches:
    st.write("Shift swapping matches for", employee_name + ":")
    for match in matches:
        if match[0] == employee_name or match[1] == employee_name:
            st.write(f"{match[0]} and {match[1]} on {match[2]} can swap shifts.")
            st.write(f"{match[0]} gives away {match[3]} and {match[1]} gives away {match[4]}")
            
else:
    st.write("No matches found for", employee_name)

