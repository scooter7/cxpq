import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random
import pandas as pd
from datetime import datetime
import boto3
from io import StringIO

s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS"]["aws_access_key_id"],
    aws_secret_access_key=st.secrets["AWS"]["aws_secret_access_key"],
)
bucket_name = st.secrets["AWS"]["bucket_name"]
object_key = st.secrets["AWS"]["object_key"]

def download_csv_from_s3():
    try:
        csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        body = csv_obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(body))
    except Exception as e:
        return pd.DataFrame()

def upload_csv_to_s3(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())

if "df" not in st.session_state:
    st.session_state.df = download_csv_from_s3()

def personality_quiz():
    trait_score_map = {
        "Confident": "Blue", "Curious": "Green", "Determined": "Maroon", "Imaginative": "Orange", "Poised": "Pink",
        "Compassionate": "Purple", "Enthusiastic": "Red", "Bold": "Silver", "Innovative": "Yellow", "Influential": "Blue",
        "Adventurous": "Green", "Tough": "Maroon", "Expressive": "Orange", "Polished": "Pink", "Selfless": "Purple",
        "Playful": "Red", "Independent": "Silver", "Analytical": "Yellow", "Achieve With Me": "Blue", "Explore With Me": "Green",
        "Strive With Me": "Maroon", "Create With Me": "Orange", "Refine With Me": "Pink", "Care With Me": "Purple",
        "Enjoy With Me": "Red", "Defy With Me": "Silver", "Invent With Me": "Yellow"
    }
    image_score_map = {
        "OrangeSet.jpg": "Orange", "BrownSet.jpg": "Maroon", "RedSet.jpg": "Red", "YellowSet.jpg": "Yellow",
        "PurpleSet.jpg": "Purple", "BlueSet.jpg": "Blue", "GreenSet.jpg": "Green", "PinkSet.jpg": "Pink", "BlackSet.jpg": "Silver"
    }
    color_priority = ["Pink", "Blue", "Silver", "Yellow", "Maroon", "Red", "Orange", "Green", "Purple"]
    score_counter = Counter({color: 3 for color in color_priority})

    def run_quiz():
        for answer in selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q2]] += 1
        for answer in least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[selected_single_trait_q5]] += 1
        for answer in least_represented_traits_q6:
            score_counter[trait_score_map[answer]] -= 1
        for image in selected_images_q7:
            score_counter[image_score_map[image]] += 1
        score_counter[image_score_map[selected_image_q8]] += 1
        for image in least_represented_images_q9:
            score_counter[image_score_map[image]] -= 1
        for mode in selected_modes_q10:
            score_counter[trait_score_map[mode]] += 1
        sorted_scores = sorted(score_counter.items(), key=lambda item: (-item[1], color_priority.index(item[0])))
        top_two_colors = [color for color, _ in sorted_scores[:2]]
        persona_name = get_persona_name(top_two_colors[0], top_two_colors[1])
        return top_two_colors, persona_name, score_counter

    def get_persona_name(primary_color, secondary_color):
        persona_map = {
            ("Blue", "Maroon"): "Champion", ("Blue", "Green"): "Captain", ("Blue", "Orange"): "Director",
            ("Blue", "Pink"): "Producer", ("Blue", "Purple"): "Mentor", ("Blue", "Red"): "Coach",
            ("Blue", "Silver"): "Maverick", ("Blue", "Yellow"): "Visionary", ("Blue", "Beige"): "Achiever",
            ("Maroon", "Blue"): "Contender", ("Maroon", "Green"): "Need to Find", ("Maroon", "Orange"): "Maker",
            ("Maroon", "Pink"): "Precisionist", ("Maroon", "Purple"): "Protector", ("Maroon", "Red"): "Energizer",
            ("Maroon", "Silver"): "Dark Horse", ("Maroon", "Yellow"): "Challenger", ("Maroon", "Beige"): "Competitor",
            ("Green", "Blue"): "Trailblazer", ("Green", "Maroon"): "Adventurer", ("Green", "Orange"): "Seeker",
            ("Green", "Pink"): "Detective", ("Green", "Purple"): "Ambassador", ("Green", "Red"): "Globetrotter",
            ("Green", "Silver"): "Ranger", ("Green", "Yellow"): "Researcher", ("Green", "Beige"): "Explorer",
            ("Orange", "Blue"): "Architect", ("Orange", "Maroon"): "Artisan", ("Orange", "Green"): "Searcher",
            ("Orange", "Pink"): "Composer", ("Orange", "Purple"): "Curator", ("Orange", "Red"): "Storyteller",
            ("Orange", "Silver"): "Nonconformist", ("Orange", "Yellow"): "Ideator", ("Orange", "Beige"): "Creator",
            ("Pink", "Blue"): "Connoisseur", ("Pink", "Maroon"): "Perfectionist", ("Pink", "Green"): "Philosopher",
            ("Pink", "Orange"): "Virtuoso", ("Pink", "Purple"): "Idealist", ("Pink", "Red"): "Aficionado",
            ("Pink", "Silver"): "Refiner", ("Pink", "Yellow"): "Trendsetter", ("Pink", "Beige"): "Sophisticate",
            ("Purple", "Blue"): "Guide", ("Purple", "Maroon"): "Guardian", ("Purple", "Green"): "Shepherd",
            ("Purple", "Orange"): "Patron", ("Purple", "Pink"): "Confidant", ("Purple", "Red"): "Host",
            ("Purple", "Silver"): "Advocate", ("Purple", "Yellow"): "Advisor", ("Purple", "Beige"): "Provider",
            ("Red", "Blue"): "Motivator", ("Red", "Maroon"): "Dynamo", ("Red", "Green"): "Thrill-seeker",
            ("Red", "Orange"): "Performer", ("Red", "Pink"): "Enthusiast", ("Red", "Purple"): "Emcee",
            ("Red", "Silver"): "DaRedevil", ("Red", "Yellow"): "Magician", ("Red", "Beige"): "Entertainer",
            ("Silver", "Blue"): "Ringleader", ("Silver", "Maroon"): "Instigator", ("Silver", "Green"): "Rogue",
            ("Silver", "Orange"): "Renegade", ("Silver", "Pink"): "Individualist", ("Silver", "Purple"): "Activist",
            ("Silver", "Red"): "Rock Star", ("Silver", "Yellow"): "Free-thinker", ("Silver", "Beige"): "Rebel",
            ("Yellow", "Blue"): "Vanguard", ("Yellow", "Maroon"): "Inventor", ("Yellow", "Green"): "Theorist",
            ("Yellow", "Orange"): "Originator", ("Yellow", "Pink"): "Dreamer", ("Yellow", "Purple"): "Oracle",
            ("Yellow", "Red"): "Futurist", ("Yellow", "Silver"): "Reformer", ("Yellow", "Beige"): "Innovator"
        }
        return persona_map.get((primary_color, secondary_color), "")

    st.title('CollegeXpress Personality Survey')
    traits = ["Confident", "Curious", "Determined", "Imaginative", "Poised", "Compassionate", "Enthusiastic", "Bold", "Innovative"]
    random.seed(st.session_state.get('random_seed', 0))
    random.shuffle(traits)
    st.write("Q1. Here is a list of 9 traits that could make up your personality. Please select exactly 3 traits that best represent who you are.")
    selected_traits_q1 = [trait for trait in traits if st.checkbox(trait, key=f"checkbox_q1_{trait}")]
    if len(selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")
    st.write("---")

    if len(selected_traits_q1) == 3:
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q2 = st.selectbox("", selected_traits_q1, key="radio_q2")
        st.write("---")
        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits if trait not in selected_traits_q1]
        random.seed(st.session_state.get('random_seed', 0))
        random.shuffle(remaining_traits_q3)
        least_represented_traits_q3 = [trait for trait in remaining_traits_q3 if st.checkbox(trait, key=f"checkbox_q3_{trait}")]
        if len(least_represented_traits_q3) != 3:
            st.warning("Please select exactly 3 traits.")
        st.write("---")

        if len(least_represented_traits_q3) == 3:
            st.write("Q4. Here is a new list of 9 traits that could make up your personality. Please select exactly 3 traits that best represent who you are.")
            traits_q4 = ["Influential", "Adventurous", "Tough", "Expressive", "Polished", "Selfless", "Playful", "Independent", "Analytical"]
            random.seed(st.session_state.get('random_seed', 0))
            random.shuffle(traits_q4)
            selected_traits_q4 = [trait for trait in traits_q4 if st.checkbox(trait, key=f"checkbox_q4_{trait}")]
            if len(selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")
            st.write("---")

            if len(selected_traits_q4) == 3:
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                selected_single_trait_q5 = st.selectbox("", selected_traits_q4, key="radio_q5")
                st.write("---")
                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]
                random.seed(st.session_state.get('random_seed', 0))
                random.shuffle(remaining_traits_q6)
                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")
                least_represented_traits_q6 = [trait for trait in remaining_traits_q6 if st.checkbox(trait, key=f"checkbox_q6_{trait}")]
                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")
                st.write("---")

                if len(least_represented_traits_q6) == 3:
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. Please take a moment to view all the groups. Then select the 3 that best represent who you are.")
                    image_files_q7 = ["OrangeSet.jpg", "BrownSet.jpg", "RedSet.jpg", "YellowSet.jpg", "PurpleSet.jpg", "BlueSet.jpg", "GreenSet.jpg", "PinkSet.jpg", "BlackSet.jpg"]
                    selected_images_q7 = []
                    random.seed(st.session_state.get('random_seed', 0))
                    random.shuffle(image_files_q7)

                    for i in range(0, len(image_files_q7), 3):
                        cols = st.columns(3)
                        for j in range(3):
                            if i + j < len(image_files_q7):
                                file = image_files_q7[i + j]
                                image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                                response = requests.get(image_url)
                                image = Image.open(BytesIO(response.content))
                                selected = cols[j].checkbox("", key=f"q7_{i+j}")
                                if selected:
                                    selected_images_q7.append(file)
                                cols[j].image(image, use_column_width=True)

                    if len(selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")
                    st.write("---")

                    if len(selected_images_q7) == 3:
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")
                        selected_image_q8 = None
                        for i, file in enumerate(selected_images_q7):
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            selected = st.checkbox("", key=f"q8_{i}")
                            st.image(image, use_column_width=True)
                            if selected:
                                if selected_image_q8:
                                    st.warning("Please select only one image.")
                                else:
                                    selected_image_q8 = file

                        st.write("Your selected image: ")
                        if selected_image_q8:
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{selected_image_q8}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            st.image(image, use_column_width=True)
                        st.write("---")

                        if selected_image_q8:
                            st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")
                            remaining_images_q9 = [file for file in image_files_q7 if file not in selected_images_q7]
                            random.seed(st.session_state.get('random_seed', 0))
                            random.shuffle(remaining_images_q9)
                            least_represented_images_q9 = []
                            cols_q9 = st.columns(3)

                            for i, file in enumerate(remaining_images_q9):
                                image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                                response = requests.get(image_url)
                                image = Image.open(BytesIO(response.content))
                                selected = cols_q9[i % 3].checkbox("", key=f"q9_{i}")
                                if selected:
                                    least_represented_images_q9.append(file)
                                cols_q9[i % 3].image(image, use_column_width=True)

                            if len(least_represented_images_q9) != 3:
                                st.warning("Please select exactly 3 images.")
                            st.write("---")

                            if len(least_represented_images_q9) == 3:
                                st.write("Q10. Below are 9 things called 'Modes of Connection.' They describe how a person can make an impression, grow friendships, and inspire others. Which two 'Modes of Connection' sound most like what you would use to make an impression, grow friendships, and inspire others?")
                                modes_of_connection = ["Achieve With Me", "Explore With Me", "Strive With Me", "Create With Me", "Refine With Me", "Care With Me", "Enjoy With Me", "Defy With Me", "Invent With Me"]
                                random.seed(st.session_state.get('random_seed', 0))
                                random.shuffle(modes_of_connection)
                                selected_modes_q10 = [mode for mode in modes_of_connection if st.checkbox(mode, key=f"checkbox_q10_{mode}")]
                                if len(selected_modes_q10) != 2:
                                    st.warning("Please select exactly 2 modes.")
                                st.write("---")

                                st.write("Q11. Full Name")
                                full_name = st.text_input("", key="full_name")
                                st.write("Q12. Email Address")
                                email_address = st.text_input("", key="email_address")
                                st.write("Q13. Affiliation")
                                affiliation = st.selectbox("", ["Admitted Student", "Current Student", "Faculty/Staff", "Alum"], key="affiliation")

                                if st.button("Submit"):
                                    if not all([full_name.strip(), email_address.strip(), affiliation]):
                                        st.warning("Please complete all the fields before submitting.")
                                    else:
                                        top_two_colors, persona_name, score_counter = run_quiz()
                                        st.write("Your top two colors are: ", ", ".join(top_two_colors))
                                        st.write("Your persona name is: ", persona_name)
                                        st.write("Total Scores for Each Color:")
                                        for color in color_priority:
                                            st.write(f"{color}: {score_counter[color]}")
                                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        new_data = {
                                            "Timestamp": [timestamp],
                                            "Full Name": [full_name],
                                            "Email Address": [email_address],
                                            "Affiliation": [affiliation],
                                            "Top Two Colors": [", ".join(top_two_colors)],
                                            "Persona Name": [persona_name]
                                        }
                                        new_df = pd.DataFrame(new_data)

                                        if 'df' not in st.session_state:
                                            st.session_state.df = new_df
                                        else:
                                            st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)

                                        upload_csv_to_s3(st.session_state.df)

if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)

personality_quiz()
