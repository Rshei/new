import streamlit as st
import pandas as pd

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
                # Check if any of the shifts of employee1 match with any of the shifts of employee2
                if shift_employee1['give_away'] in shift_employee2[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                    if shift_employee2['give_away'] in shift_employee1[['can_take_early', 'can_take_morning', 'can_take_evening', 'can_take_night', 'can_take_rest']].values:
                        # If there's a match, store the information
                        matches.append((shift_employee1['employee_id'], shift_employee2['employee_id'], shift_employee1['date'], shift_employee1['give_away'],
                                        shift_employee2['give_away']))
    return matches

# Display the data editor
st.write("Shift Swap Submission Form")
df = pd.DataFrame(columns=['date','employee_id','give_away','can_take_early','can_take_morning','can_take_evening',
                           'can_take_night','can_take_rest'])
shifts = ['early', 'morning', 'evening', 'night', 'rest', None]
config = {
    'date' : st.column_config.TextColumn('Choose date for swap', width='small'),
    'employee_id' : st.column_config.NumberColumn('Employee ID', min_value=1, max_value=50),
    'give_away' : st.column_config.SelectboxColumn('Give Away', options=shifts),
    'can_take_early' : st.column_config.SelectboxColumn('Can Take Early', options=shifts),
    'can_take_morning' : st.column_config.SelectboxColumn('Can Take Morning', options=shifts),
    'can_take_evening' : st.column_config.SelectboxColumn('Can Take Evening', options=shifts),
    'can_take_night' : st.column_config.SelectboxColumn('Can Take Night', options=shifts),
    'can_take_rest' : st.column_config.SelectboxColumn('Can Take Rest', options=shifts)
}

result = st.data_editor(df, column_config=config, num_rows='dynamic', hide_index=True)

# Check for submission
if st.button("Submit"):
    st.write("Data submitted!")

    # Find matches among all users
    matches = find_matches(result)

    
    if matches:
        st.write("Shift swapping matches:")
        for match in matches:
            st.write(f"Employee {match[0]} and Employee {match[1]} on {match[2]} can swap shifts.")
            st.write(f"Employee {match[0]} gives away {match[3]} and Employee {match[1]} gives away {match[4]}")
            st.write()
    else:
        st.write("No matches found.")
