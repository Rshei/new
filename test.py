import streamlit as st
import pandas as pd

# Function to find matches for shift swapping
def find_matches(submissions):
    matches = []
    user_ids = list(submissions.keys())
    
    # Iterate through each pair of users
    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
            user1_id = user_ids[i]
            user2_id = user_ids[j]
            
            user1_shifts = submissions[user1_id]
            user2_shifts = submissions[user2_id]
            
            # Compare shifts between the current pair of users
            for _, shift1 in user1_shifts.iterrows():
                for _, shift2 in user2_shifts.iterrows():
                    # Check if shifts match and the date is the same
                    if (shift1['give_away'] in shift2.dropna().values and
                        shift2['give_away'] in shift1.dropna().values and
                        shift1['date'] == shift2['date']):
                        # If there is a match, store the information
                        matches.append((user1_id, user2_id, shift1['date'], shift1['give_away']))
    return matches

# Initialize an empty dictionary to store submitted data
submissions = {}

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
    
    # Extract employee ID from the submitted data
    employee_id = result['employee_id'].iloc[0]  
    
    # Store the submitted data in the submissions dictionary
    submissions[employee_id] = result
    
    # Check for matches among all users
    matches = find_matches(submissions)
    if matches:
        st.write("Shift swapping matches:")
        for match in matches:
            st.write(match)
    else:
        st.write("No matches found.")
