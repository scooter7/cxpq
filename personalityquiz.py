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
    
    # Convert the responses dictionary to DataFrame
    df = pd.DataFrame([responses])
    
    # Write DataFrame to StringIO object
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Upload CSV to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())

def personality_quiz():
    # (existing trait_score_map, image_score_map, color_priority, and score_counter initialization)
    
    # (existing run_quiz and get_persona_name functions)
    
    st.title('CollegeXpress Personality Survey')
    
    # (existing traits initialization and shuffling)
    
    # (existing UI elements for Q1 to Q10)
    
    # New Input Fields and Submit Button
    full_name = st.text_input("Full Name")
    email_address = st.text_input("Email Address")
    association = st.selectbox("Your Association", ["", "Current Student", "Admitted Student", "Faculty/Staff", "Alum"])
    
    if st.button("Submit"):
        if not full_name or not email_address or not association or association == "":
            st.warning("Please fill in your Full Name, Email Address, and Your Association.")
        # Add other validations for Q1 to Q10 here
        else:
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

# Set the random seed for each user session
if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)

personality_quiz()
