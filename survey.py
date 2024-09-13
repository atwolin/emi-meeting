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
    st.title("Survey for Meeting Attendence")

    # # Create the form
    # st.header("Feedback Form")
    # name = st.text_input("Name")
    # email = st.text_input("Email")
    # # value = streamlit_when2meet(disabled=False)

    # # Embed When2Meet using an iframe
    # st.markdown("### For the pre-meeting")
    # pre_attend = st.radio(
    #     "是否會參加會議？是則請選擇日期",
    #     [
    #         "Yes, and I will attend in person.",
    #         "Yes, and I will participate online.",
    #         "No, but my parner will attend.",
    #         "No, but I will discuss it with the professor another day.",
    #         "Others.",
    #     ],
    # )
    # if pre_attend == "Others.":
    #     pre_attend = st.text_input("Please write your answer.")

    st.markdown("### Google form")
    googleform_url = "https://forms.gle/8rjzen5DXuPRBiaY9"
    if st.checkbox("Show Google form"):
        components.html(
            f'<iframe src="{googleform_url}" width="100%" height="600" frameborder="0"></iframe>',
            height=600,
        )

    st.markdown("### when2meet")
    when2meet_url = "https://www.when2meet.com/?26426058-grwZy"
    if st.checkbox("Show when2meet"):
        components.html(
            f'<iframe src="{when2meet_url}" width="100%" height="600" frameborder="0"></iframe>',
            height=600,
        )

    st.markdown("### Google form responses")
    response = "https://docs.google.com/forms/d/e/1FAIpQLSdfRjNdGFgHj_oSDtql5i0AQazatB5tMNfaN6FMw1IR-zQhxw/viewform?usp=sharing"
    st.markdown(f"Link: [response]({response})")
    exel_url = "https://docs.google.com/spreadsheets/d/1ALgNQ7L6t5N0OUz02m-g2Ym2fneMkVwSXZmJ07ff6f4/edit?usp=sharing"
    if st.checkbox("Show response table"):
        components.html(
            f'<iframe src="{exel_url}" width="100%" height="600" frameborder="0"></iframe>',
            height=600,
        )

    # st.markdown("### For meeting with Academic Affairs Office")
    # attend = st.radio(
    #     "是否會參加會議？是則請選擇日期",
    #     [
    #         "Yes, and I will attend in person.",
    #         "Yes, and I will participate online.",
    #         "No, but my parner will attend.",
    #         "No, but I will check the meeting minutes.",
    #         "Others.",
    #     ],
    # )
    # if attend.startswith("Yes"):
    #     dates = st.multiselect(
    #         "請選擇可以參加的日期，時間固定為 16:00 ~ 17:00 之間",
    #         ["10/14"],
    #     )
    # elif attend == "Others.":
    #     ans = st.text_input("")
    #     dates = [ans]
    # else:
    #     dates = ["none"]
    # if st.button("Submit"):
    #     if name and email and attend:
    #         insert_response(name, email, pre_attend, attend, str(dates))
    #         st.success("Thank you for your feedback!")
    #     else:
    #         st.error("Please fill in all fields!")

    # # Show the responses if the user is an admin
    # if st.checkbox("Show Responses"):
    #     # pass
    #     responses = fetch_responses()
    #     df = pd.DataFrame(
    #         responses,
    #         columns=[
    #             "ID",
    #             "Month",
    #             "Name",
    #             "Email",
    #             "Attendence for pre-meeting",
    #             "Attendence for meeting",
    #             "Dates",
    #         ],
    #     )
    #     st.write(df)


if __name__ == "__main__":
    # create_table()
    main()
