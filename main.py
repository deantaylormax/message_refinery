import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os
import dotenv
dotenv.load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")

template = """
    This message is not properly written.
    Your goal is to:
    - Properly format the email
    - Convert the text to a specified tone
    - Convert the text to a specified dialect

    Here are some examples different Tones:
    - Excited: I'm so excited to tell you about my trip to Barcelona! It was so much fun. I can't wait to tell you all about it.
    - Formal: I am writing to inform you of my recent trip to Barcelona. It was a very enjoyable experience. I would like to share my thoughts with you.
    - Casual: Hey! I just got back from Barcelona. It was awesome! I had a great time. I'll tell you all about it when I see you.
    - Robotic: Went to Barcelona. It was fun. Bye.

    Here are some examples of words in different dialects:
    - Midwest American English: pop, tennis shoes, gym shoes, shopping cart, bag, bag lunch, drinking fountain
    - Southern American English: coke, tennis shoes, gym shoes, buggy, sack, sack lunch
    - New England American English: sneakers, carriage, bag, bag lunch, bubbler
    - English as spoken by a native of the United Kingdom: trainers, pram, trolley, packed lunch, water fountain
    - English as spoken by a native of Australia: runners, pram, trolley, packed lunch, bubbler
    
    Example Sentences from each dialect:
    - Midwest American English: Could you please pass the ranch dressing? I think it goes great with this salad.
    - Southern American English: Y'all come back now, ya hear? We'll have sweet tea waitin' for you.
    - New England American English: I'm wicked excited to go to the beach this weekend. I hope the weather is nice.  I'm gonna pack my car and head to the Cape for the weekend. Wanna grab some chowdah before we go?
    - English as spoken by a native of the United Kingdom: I'm going to the loo. I'll be back in a minute.
    - English as spoken by a native of Australia: I'm going to the dunny. I'll be back in a tick.

    Please start the email with a pleasant introduction. Add the introduction if you think it is necessary.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

# Define your username and password
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Basic login section
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Authentication check
if st.sidebar.button("Login"):
    if username == USERNAME and password == PASSWORD:
        st.success(f"Logged in as {username}")
        st.header("Message Refinery")
        st.markdown("Refine your messages with new tones and dialects.")
        st.markdown("## Enter Your Text - Make Your Selections")
        col1, col2 = st.columns(2)
        with col1:
            option_tone = st.selectbox(
                'Choose your tone for the message',
                ('Excited', 'Formal', 'Casual', 'Robotic'))
            
        with col2:
            option_dialect = st.selectbox(
                'Choose your dailect for the message',
                ('Midwest American English', 'Southern American English', 'New England American English', 'English as spoken by a native of the United Kingdom', 'English as spoken by a native of Australia'))

        def get_text():
            input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
            return input_text

        email_input = get_text()

        if len(email_input.split(" ")) > 500:
            st.write("Try again, the max length for your message is 500 words.")
            st.stop()

        def update_text_with_example():
            # print ("in updated")
            st.session_state.email_input = "I has to get to your house by when again?  I wanna not be to late you know.  Thanks for so much responding."

        st.button("*Click to see an example*", type='secondary', help="Check out the example.", on_click=update_text_with_example)

        st.markdown("### Your New Message:")

        if email_input:

            llm = load_LLM(openai_api_key=openai_api_key)

            prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

            formatted_email = llm(prompt_with_email)

            st.write(formatted_email)
    else:
        st.error("Incorrect username or password")