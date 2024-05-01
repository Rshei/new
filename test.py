import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

employee_name = st.selectbox("Enter your name:", options=['Raanan_shein', 'Christina_shein', 'Tomma_shein'])
selected_month = st.selectbox("Select the month:", options=range(1, 13))

# Define function to generate dates
def generate_dates(year, month):
    start_date = datetime(year, month, 1)
    num_days = (datetime(year, month + 1, 1) - start_date).days
    dates_list = [start_date + timedelta(days=i) for i in range(num_days)]
    return [date.strftime('%Y-%m-%d') for date in dates_list]

# Define function to find matches
def find_matches(df):
    matches = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            shift_employee1 = df.iloc[i]
            shift_employee2 = df.iloc[j]
            if shift_employee1['date'] == shift_employee2['date']:
                if shift_employee1['give_away'] in shift_employee2[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                    if shift_employee2['give_away'] in shift_employee1[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                        matches.append((shift_employee1['employee_name'], shift_employee2['employee_name'], shift_employee1['date'], shift_employee1['give_away'],
                                        shift_employee2['give_away']))
    return matches

# Define function to get session state
def get_state():
    if 'submissions' not in st.session_state:
        st.session_state.submissions = []

# Get session state
get_state()

# Define session state variables
session_submissions = st.session_state.submissions



# Display the data editor
st.write("Shift Swap Submission Form")
df = pd.DataFrame(columns=['date','employee_name','give_away','can_take_early','can_take_morning','can_take_evening',
                            'can_take_night','can_take_rest'])
shifts = ['early', 'morning', 'evening', 'night', 'rest', None]
config = {
    'date' : st.column_config.SelectboxColumn('date', width='small',options=generate_dates(2024, 5)),
    'employee_name' : st.column_config.SelectboxColumn('Employee name',options=['Raanan_shein', 'Christina_shein', 'Tomma_shein']),
    'give_away' : st.column_config.SelectboxColumn('Give Away', options=shifts),
    'can_take_early' : st.column_config.SelectboxColumn('Can Take Early', options=['early',None]),
    'can_take_morning' : st.column_config.SelectboxColumn('Can Take Morning', options=['morning',None]),
    'can_take_evening' : st.column_config.SelectboxColumn('Can Take Evening', options=['evening',None]),
    'can_take_night' : st.column_config.SelectboxColumn('Can Take Night', options=['night',None]),
    'can_take_rest' : st.column_config.SelectboxColumn('Can Take Rest', options=['rest',None])
}

result = st.data_editor(df, column_config=config, num_rows='dynamic', hide_index=True)

# Append the submission to the session submissions
session_submissions.append(result)

# Check for submission
if st.button("Submit"):
    st.write("Data submitted!")
# Display matches for the selected employee name
    matches = []
    for submission in session_submissions:
        matches.extend(find_matches(submission))


    if matches:
        st.write("Shift swapping matches for", employee_name + ":")
        for match in matches:
            if match[0] == employee_name or match[1] == employee_name:
                st.write(f"{match[0]} and {match[1]} on {match[2]} can swap shifts.")
                st.write(f"{match[0]} gives away {match[3]} and {match[1]} gives away {match[4]}")
                st.write()
    else:
        st.write("No matches found for", employee_name)
