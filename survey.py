import streamlit as st
import sqlite3
import pandas as pd
import streamlit.components.v1 as components

# Create a connection to the SQLite database
conn = sqlite3.connect("responses.db")
c = conn.cursor()


# Create a table to store form responses
def create_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS form_responses (id INTEGER PRIMARY KEY AUTOINCREMENT, month TEXT, name TEXT, email TEXT, pre_attend TEXT, attend TEXT, dates TEXT)"
    )
    conn.commit()


# Insert a new response into the table
def insert_response(name, email, pre_attend, attend, dates, month=10):
    c.execute(
        "INSERT OR REPLACE INTO form_responses (id, month, name, email, pre_attend, attend, dates) "
        "VALUES ((SELECT id FROM form_responses WHERE name = ?), ?, ?, ?, ?, ?, ?)",
        (name, month, name, email, pre_attend, attend, dates),
    )
    conn.commit()


# Fetch all responses from the database
def fetch_responses():
    c.execute("SELECT * FROM form_responses")
    data = c.fetchall()
    return data


# Main app function
def main():
    st.title("Survey for Acadamic")

    # Create the form
    st.header("Feedback Form")
    name = st.text_input("Name")
    email = st.text_input("Email")
    # value = streamlit_when2meet(disabled=False)

    # Embed When2Meet using an iframe
    st.markdown("### For the pre-meeting")
    pre_attend = st.radio(
        "是否會參加會議？是則請選擇日期",
        [
            "Yes.",
            "No, but my parner will attend.",
            "No, but I will discuss it with the professor another day.",
        ],
    )
    when2meet_url = "https://www.when2meet.com/?26423062-49Nq8"
    components.html(
        f'<iframe src="{when2meet_url}" width="100%" height="600" frameborder="0"></iframe>',
        height=600,
    )

    st.markdown("### For meeting with Academic Affairs Office")
    attend = st.radio(
        "是否會參加會議？是則請選擇日期",
        [
            "Yes.",
            "No, but my parner will attend.",
        ],
    )
    if attend == "Yes.":
        dates = st.multiselect(
            "請選擇可以參加的日期，時間固定為 14:00 ~ 16:00 之間",
            ["10/1", "10/8", "10/15", "10/22", "10/29"],
        )
    else:
        dates = ["none"]
    if st.button("Submit"):
        if name and email and attend:
            insert_response(name, email, pre_attend, attend, str(dates))
            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill in all fields!")

    # st.write(value)

    # Show the responses if the user is an admin
    if st.checkbox("Show Responses"):
        # pass
        responses = fetch_responses()
        print(responses)
        df = pd.DataFrame(
            responses,
            columns=[
                "ID",
                "Month",
                "Name",
                "Email",
                "Attendence for pre-meeting",
                "Attendence for meeting",
                "Dates",
            ],
        )
        st.write(df)


if __name__ == "__main__":
    create_table()
    main()
