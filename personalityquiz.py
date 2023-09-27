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

# Initialize S3 client
s3 = boto3.client(
    "s3", 
    aws_access_key_id=st.secrets["AWS"]["aws_access_key_id"], 
    aws_secret_access_key=st.secrets["AWS"]["aws_secret_access_key"]
)
bucket_name = st.secrets["AWS"]["bucket_name"]

# Function to upload responses to S3
def upload_responses_to_s3(responses):
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    unique_id_str = str(uuid.uuid4())
    object_key = f"responses/{timestamp_str}_{unique_id_str}.csv"
    
    df = pd.DataFrame([responses])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())

def personality_quiz():
    # (existing trait_score_map, image_score_map, color_priority, and score_counter initialization)
    
    # (existing run_quiz and get_persona_name functions)
    
    st.title('CollegeXpress Personality Survey')
    
    # (existing traits initialization and shuffling)
    
    # (existing UI elements for Q1 to Q10)
    
    # New Input Fields
    full_name = st.text_input("Full Name")
    email_address = st.text_input("Email Address")
    association = st.selectbox("Your Association", ["", "Current Student", "Admitted Student", "Faculty/Staff", "Alum"])
    
    # Validation: Check if all questions have been answered and required fields are filled
    if (full_name and email_address and association and association != ""):
        # If all validations pass, render the 'Submit' button
        if st.button("Submit"):
            # Run the quiz and gather the results
            top_two_colors, persona_name, score_counter = run_quiz()
            
            # Prepare the responses
            responses = {
                "full_name": full_name,
                "email_address": email_address,
                "association": association,
                "top_two_colors": top_two_colors,
                "persona_name": persona_name,
                # Include other responses and analysis results
            }
            
            # Upload the responses to S3
            upload_responses_to_s3(responses)
            
            # Display the results to the user
            st.write("Your top two colors are: ", ", ".join(top_two_colors))
            st.write("Your persona name is: ", persona_name)
            st.write("Total Scores for Each Color:")
            for color in color_priority:
                st.write(f"{color}: {score_counter[color]}")
    else:
        st.warning("Please answer all questions and fill in your Full Name, Email Address, and Your Association before submitting.")

# Set the random seed for each user session
if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)

personality_quiz()
