import uuid
from datetime import datetime
import boto3
import pandas as pd
from io import StringIO
import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random

def personality_quiz():
    trait_score_map = {
        "Confident": "Blue",
        "Curious": "Green",
        "Determined": "Maroon",
        "Imaginative": "Orange",
        "Poised": "Pink",
        "Compassionate": "Purple",
        "Enthusiastic": "Red",
        "Bold": "Silver",
        "Innovative": "Yellow",
        "Influential": "Blue",
        "Adventurous": "Green",
        "Tough": "Maroon",
        "Expressive": "Orange",
        "Polished": "Pink",
        "Selfless": "Purple",
        "Playful": "Red",
        "Independent": "Silver",
        "Analytical": "Yellow",
        "Achieve With Me": "Blue",
        "Explore With Me": "Green",
        "Strive With Me": "Maroon",
        "Create With Me": "Orange",
        "Refine With Me": "Pink",
        "Care With Me": "Purple",
        "Enjoy With Me": "Red",
        "Defy With Me": "Silver",
        "Invent With Me": "Yellow",
    }

    image_score_map = {
        "OrangeSet.jpg": "Orange",
        "BrownSet.jpg": "Maroon",
        "RedSet.jpg": "Red",
        "YellowSet.jpg": "Yellow",
        "PurpleSet.jpg": "Purple",
        "BlueSet.jpg": "Blue",
        "GreenSet.jpg": "Green",
        "PinkSet.jpg": "Pink",
        "BlackSet.jpg": "Silver",
    }

    color_priority = ["Pink", "Blue", "Silver", "Yellow", "Maroon", "Red", "Orange", "Green", "Purple"]

    score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    
    def run_quiz():
        # Ensure that selected_single_trait_q2 and similar variables are assigned values properly within the function
        # For example:
        # selected_single_trait_q2 = some_value  # Replace 'some_value' with the actual value or expression intended to be assigned to selected_single_trait_q2
        
        # Place the surrounding lines of code in the proper scope within the function
            score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1
 Set the random seed for each user session
if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)

personality_quiz()


s3 = boto3.client(
    "s3", 
    aws_access_key_id=st.secrets["AWS"]["aws_access_key_id"], 
    aws_secret_access_key=st.secrets["AWS"]["aws_secret_access_key"]
)
bucket_name = st.secrets["AWS"]["bucket_name"]
object_key = st.secrets["AWS"]["object_key"]


def upload_responses_to_s3(responses):
    # Generate a DataFrame from the responses dictionary
    new_response_df = pd.DataFrame([responses])
    
    # Try to read the existing CSV file from the S3 bucket
    try:
        csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        existing_responses_df = pd.read_csv(csv_obj['Body'])
        # Append the new response to the existing responses
        all_responses_df = existing_responses_df.append(new_response_df, ignore_index=True)
    except Exception as e:
        # If the file does not exist, use the new response DataFrame
        all_responses_df = new_response_df
    
    # Write DataFrame to StringIO object
    csv_buffer = StringIO()
    all_responses_df.to_csv(csv_buffer, index=False)
    
    # Upload the updated CSV to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())


# Create a form

    def run_quiz():
        # Ensure that selected_single_trait_q2 and similar variables are assigned values properly within the function
        # For example:
        # selected_single_trait_q2 = some_value  # Replace 'some_value' with the actual value or expression intended to be assigned to selected_single_trait_q2
        
        # Place the surrounding lines of code in the proper scope within the function
            score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1

    with st.form(key='response_form'):
    # Add the new input fields inside the form
    full_name = 
    email_address = 
    association = 
    
    # Add a submit button to the form
    submitted = st.form_submit_button("Submit")
    
    # Check if the form is submitted and if all the mandatory fields are filled
    if submitted:
        if full_name and email_address and association != "Select":
            responses = {
                "full_name": full_name,
                "email_address": email_address,
                "association": association,
                # Add other responses and analysis results
            }
            upload_responses_to_s3(responses)
        else:
            st.error("Please fill in all the mandatory fields before submitting.")


# Generate a unique object key for each response
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
unique_id_str = str(uuid.uuid4())
object_key = f"responses/{timestamp_str}_{unique_id_str}.csv"

    def run_quiz():
        # Ensure that selected_single_trait_q2 and similar variables are assigned values properly within the function
        # For example:
        # selected_single_trait_q2 = some_value  # Replace 'some_value' with the actual value or expression intended to be assigned to selected_single_trait_q2
        
        # Place the surrounding lines of code in the proper scope within the function
            score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1

    with st.form(key='response_form'):
    st.selectbox("", selected_traits_q1, key="radio_q2")
    st.selectbox("", selected_traits_q4, key="radio_q5")
    st.text_input("Full Name")
    st.text_input("Email Address")
    st.selectbox("Your Association", ["Select", "Current Student", "Admitted Student", "Faculty/Staff", "Alum"])
    # Add the new input fields inside the form
    full_name = st.text_input("Full Name")
    email_address = st.text_input("Email Address")
    association = st.selectbox("Your Association", ["Select", "Current Student", "Admitted Student", "Faculty/Staff", "Alum"])
    
    # Add a submit button to the form
    submitted = st.form_submit_button("Submit")
    
    # Check if the form is submitted and if all the mandatory fields are filled
    if submitted:
        if full_name and email_address and association != "Select":
            responses = {
                "full_name": full_name,
                "email_address": email_address,
                "association": association,
                # Add other responses and analysis results
            }
            upload_responses_to_s3(responses)
        else:
            st.error("Please fill in all the mandatory fields before submitting.")
 boto3
import pandas as pd
from io import StringIO

import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random

def personality_quiz():
    trait_score_map = {
        "Confident": "Blue",
        "Curious": "Green",
        "Determined": "Maroon",
        "Imaginative": "Orange",
        "Poised": "Pink",
        "Compassionate": "Purple",
        "Enthusiastic": "Red",
        "Bold": "Silver",
        "Innovative": "Yellow",
        "Influential": "Blue",
        "Adventurous": "Green",
        "Tough": "Maroon",
        "Expressive": "Orange",
        "Polished": "Pink",
        "Selfless": "Purple",
        "Playful": "Red",
        "Independent": "Silver",
        "Analytical": "Yellow",
        "Achieve With Me": "Blue",
        "Explore With Me": "Green",
        "Strive With Me": "Maroon",
        "Create With Me": "Orange",
        "Refine With Me": "Pink",
        "Care With Me": "Purple",
        "Enjoy With Me": "Red",
        "Defy With Me": "Silver",
        "Invent With Me": "Yellow",
    }

    image_score_map = {
        "OrangeSet.jpg": "Orange",
        "BrownSet.jpg": "Maroon",
        "RedSet.jpg": "Red",
        "YellowSet.jpg": "Yellow",
        "PurpleSet.jpg": "Purple",
        "BlueSet.jpg": "Blue",
        "GreenSet.jpg": "Green",
        "PinkSet.jpg": "Pink",
        "BlackSet.jpg": "Silver",
    }

    color_priority = ["Pink", "Blue", "Silver", "Yellow", "Maroon", "Red", "Orange", "Green", "Purple"]

    score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    
    def run_quiz():
        # Ensure that selected_single_trait_q2 and similar variables are assigned values properly within the function
        # For example:
        # selected_single_trait_q2 = some_value  # Replace 'some_value' with the actual value or expression intended to be assigned to selected_single_trait_q2
        
        # Place the surrounding lines of code in the proper scope within the function
            score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1
 Set the random seed for each user session
if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)

personality_quiz()


s3 = boto3.client(
    "s3", 
    aws_access_key_id=st.secrets["AWS"]["aws_access_key_id"], 
    aws_secret_access_key=st.secrets["AWS"]["aws_secret_access_key"]
)
bucket_name = st.secrets["AWS"]["bucket_name"]
object_key = st.secrets["AWS"]["object_key"]


def upload_responses_to_s3(responses):
    # Generate a DataFrame from the responses dictionary
    new_response_df = pd.DataFrame([responses])
    
    # Try to read the existing CSV file from the S3 bucket
    try:
        csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        existing_responses_df = pd.read_csv(csv_obj['Body'])
        # Append the new response to the existing responses
        all_responses_df = existing_responses_df.append(new_response_df, ignore_index=True)
    except Exception as e:
        # If the file does not exist, use the new response DataFrame
        all_responses_df = new_response_df
    
    # Write DataFrame to StringIO object
    csv_buffer = StringIO()
    all_responses_df.to_csv(csv_buffer, index=False)
    
    # Upload the updated CSV to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())


# Create a form

    def run_quiz():
        # Ensure that selected_single_trait_q2 and similar variables are assigned values properly within the function
        # For example:
        # selected_single_trait_q2 = some_value  # Replace 'some_value' with the actual value or expression intended to be assigned to selected_single_trait_q2
        
        # Place the surrounding lines of code in the proper scope within the function
            score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1

    with st.form(key='response_form'):
    # Add the new input fields inside the form
    full_name = 
    email_address = 
    association = 
    
    # Add a submit button to the form
    submitted = st.form_submit_button("Submit")
    
    # Check if the form is submitted and if all the mandatory fields are filled
    if submitted:
        if full_name and email_address and association != "Select":
            responses = {
                "full_name": full_name,
                "email_address": email_address,
                "association": association,
                # Add other responses and analysis results
            }
            upload_responses_to_s3(responses)
        else:
            st.error("Please fill in all the mandatory fields before submitting.")


# Generate a unique object key for each response
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
unique_id_str = str(uuid.uuid4())
object_key = f"responses/{timestamp_str}_{unique_id_str}.csv"
