import streamlit as st
import pandas as pd

# Function to find matches for shift swapping
def find_matches(shift_tables):
    matches = []
    
    # Iterate through each pair of employees
    for employee_id, shifts in shift_tables.items():
        for other_id, other_shifts in shift_tables.items():
            if employee_id != other_id:
                # Compare shifts between the current pair of employees
                for _, shift in shifts.iterrows():
                    for _, other_shift in other_shifts.iterrows():
                        # Check if shifts match and the date is the same
                        if (shift['give_away'] in other_shift.dropna().values and
                            other_shift['give_away'] in shift.dropna().values and
                            shift['date'] == other_shift['date']):
                            # If there is a match, store the information
                            matches.append((employee_id, other_id, shift['date'], shift['give_away']))
    return matches

# Initialize an empty dictionary to store submitted data
submissions = {}

# Display the data editor
st.write("Shift Swap Submission Form")
df = pd.DataFrame(columns=['date','employee_id','give_away','can_take_early','can_take_morning','can_take_evening',
                           'can_take_night','can_take_rest'])
shifts = ['early', 'morning', 'evening', 'night', 'rest', None]
config = {
    'date' : st.column_config.TextColumn('choose date for swap', width='small'),
    'employee_id' : st.column_config.NumberColumn('employee_id', min_value=1, max_value=50),
    'give_away' : st.column_config.SelectboxColumn('give_away', options=shifts),
    'can_take_early' : st.column_config.SelectboxColumn('can_take_early', options=shifts),
    'can_take_morning' : st.column_config.SelectboxColumn('can_take_morning', options=shifts),
    'can_take_evening' : st.column_config.SelectboxColumn('can_take_evening', options=shifts),
    'can_take_night' : st.column_config.SelectboxColumn('can_take_night', options=shifts),
    'can_take_rest' : st.column_config.SelectboxColumn('can_take_rest', options=shifts)
}

result = st.data_editor(df, column_config=config, num_rows='dynamic', hide_index=True)

# Check for submission
if st.button("Submit"):
    st.write("Data submitted!")
    
    # Extract employee ID from the submitted data
    employee_id = result['employee_id'].iloc[0]  
    
    # Store the submitted data in the submissions dictionary
    submissions[employee_id] = result
    
    # Check for matches
    matches = find_matches(submissions)
    if matches:
        st.write("Shift swapping matches:")
        for match in matches:
            st.write(match)
    else:
        st.write("No matches found.")
st.write(submissions)