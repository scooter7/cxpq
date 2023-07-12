import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import random

def run_quiz():
    top_two_colors = []
    persona_name = ""
    score_counter = {}
    return top_two_colors, persona_name, score_counter

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
        "Innovative": "Yellow"
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
        "BlackSet.jpg": "Silver"
    }

    color_priority = ["Pink", "Blue", "Silver", "Yellow", "Maroon", "Red", "Orange", "Green", "Purple"]

    score_counter = {color: 3 for color in color_priority}

    def get_persona_name(primary_color, secondary_color):
        pass

    st.title('CollegeXpress Personality Survey')

    traits = ["Confident", "Curious", "Determined", "Imaginative", "Poised", "Compassionate", "Enthusiastic", "Bold", "Innovative"]

    st.write("Q1. Here is a list of 9 traits that could make up your personality. Please select exactly 3 traits that best represent who you are.")
    if "randomized_traits_q1" not in st.session_state:
        st.session_state.randomized_traits_q1 = random.sample(traits, len(traits))
    selected_traits_q1 = []
    for trait in st.session_state.randomized_traits_q1:
        selected = st.checkbox(trait, key=f"checkbox_q1_{trait}")
        if selected:
            selected_traits_q1.append(trait)

    if len(selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")

    st.write("---")

    if len(selected_traits_q1) == 3:
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        if "selected_single_trait_q2" not in st.session_state:
            st.session_state.selected_single_trait_q2 = None
        selected_single_trait_q2 = st.radio("", selected_traits_q1, key="radio_q2")

        st.write("---")

        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits if trait not in selected_traits_q1]
        if "randomized_remaining_traits_q3" not in st.session_state:
            st.session_state.randomized_remaining_traits_q3 = random.sample(remaining_traits_q3, len(remaining_traits_q3))
        least_represented_traits_q3 = []
        for trait in st.session_state.randomized_remaining_traits_q3:
            selected = st.checkbox(trait, key=f"checkbox_q3_{trait}")
            if selected:
                least_represented_traits_q3.append(trait)

        if len(least_represented_traits_q3) != 3:
            st.warning("Please select exactly 3 traits.")

        st.write("---")

        if len(least_represented_traits_q3) == 3:
            st.write("Q4. Here is a new list of 9 traits that could make up your personality. Please select exactly 3 traits that best represent who you are.")
            traits_q4 = ["Influential", "Adventurous", "Tough", "Expressive", "Polished", "Selfless", "Playful", "Independent", "Analytical"]

            if "randomized_traits_q4" not in st.session_state:
                st.session_state.randomized_traits_q4 = random.sample(traits_q4, len(traits_q4))
            selected_traits_q4 = []
            for trait in st.session_state.randomized_traits_q4:
                selected = st.checkbox(trait, key=f"checkbox_q4_{trait}")
                if selected:
                    selected_traits_q4.append(trait)

            if len(selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")

            st.write("---")

            if len(selected_traits_q4) == 3:
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                if "selected_single_trait_q5" not in st.session_state:
                    st.session_state.selected_single_trait_q5 = None
                selected_single_trait_q5 = st.radio("", selected_traits_q4, key="radio_q5")

                st.write("---")

                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]
                if "randomized_remaining_traits_q6" not in st.session_state:
                    st.session_state.randomized_remaining_traits_q6 = random.sample(remaining_traits_q6, len(remaining_traits_q6))

                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")

                least_represented_traits_q6 = []
                for trait in st.session_state.randomized_remaining_traits_q6:
                    selected = st.checkbox(trait, key=f"checkbox_q6_{trait}")
                    if selected:
                        least_represented_traits_q6.append(trait)

                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")

                st.write("---")

                if len(least_represented_traits_q6) == 3:
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. Please take a moment to view all the groups. Then select the 3 that best represent who you are.")

                    image_files_q7 = ["OrangeSet.jpg", "BrownSet.jpg", "RedSet.jpg", "YellowSet.jpg", "PurpleSet.jpg", "BlueSet.jpg", "GreenSet.jpg", "PinkSet.jpg", "BlackSet.jpg"]

                    if "randomized_image_files_q7" not in st.session_state:
                        st.session_state.randomized_image_files_q7 = random.sample(image_files_q7, len(image_files_q7))
                    selected_images_q7 = []

                    for i, file in enumerate(st.session_state.randomized_image_files_q7):
                        image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                        response = requests.get(image_url)
                        image = Image.open(BytesIO(response.content))
                        selected = st.checkbox("", key=f"q7_{i}")
                        if selected:
                            selected_images_q7.append(file)
                        st.image(image, use_column_width=True)

                    if len(selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")

                    st.write("---")

                    if len(selected_images_q7) == 3:
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")

                        if "selected_image_q8" not in st.session_state:
                            st.session_state.selected_image_q8 = None

                        for i, file in enumerate(selected_images_q7):
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            selected = st.checkbox("", key=f"q8_{i}")
                            st.image(image, use_column_width=True)
                            if selected:
                                if st.session_state.selected_image_q8:
                                    st.warning("Please select only one image.")
                                else:
                                    st.session_state.selected_image_q8 = file

                        st.write("Your selected image: ")
                        if st.session_state.selected_image_q8:
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{st.session_state.selected_image_q8}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            st.image(image, use_column_width=True)

                        st.write("---")

                        if st.session_state.selected_image_q8:
                            st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")
                            remaining_images_q9 = [file for file in image_files_q7 if file not in selected_images_q7]

                            if "randomized_remaining_images_q9" not in st.session_state:
                                st.session_state.randomized_remaining_images_q9 = random.sample(remaining_images_q9, len(remaining_images_q9))

                            least_represented_images_q9 = []

                            for i, file in enumerate(st.session_state.randomized_remaining_images_q9):
                                image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                                response = requests.get(image_url)
                                image = Image.open(BytesIO(response.content))
                                selected = st.checkbox("", key=f"q9_{i}")
                                if selected:
                                    least_represented_images_q9.append(file)
                                st.image(image, use_column_width=True)

                            if len(least_represented_images_q9) != 3:
                                st.warning("Please select exactly 3 images.")

                            st.write("---")

                            if len(least_represented_images_q9) == 3:
                                st.write("Q10. Below are 9 things called 'Modes of Connection.' They describe how a person can make an impression, grow friendships, and inspire others. Which two 'Modes of Connection' sound most like what you would use to make an impression, grow friendships, and inspire others?")

                                modes_of_connection = ["Achieve With Me", "Explore With Me", "Strive With Me", "Create With Me", "Refine With Me", "Care With Me", "Enjoy With Me", "Defy With Me", "Invent With Me"]

                                if "randomized_modes_of_connection" not in st.session_state:
                                    st.session_state.randomized_modes_of_connection = random.sample(modes_of_connection, len(modes_of_connection))

                                selected_modes_q10 = []
                                for mode in st.session_state.randomized_modes_of_connection:
                                    selected = st.checkbox(mode, key=f"checkbox_q10_{mode}")
                                    if selected:
                                        selected_modes_q10.append(mode)

                                if len(selected_modes_q10) != 2:
                                    st.warning("Please select exactly 2 modes.")

                                st.write("---")

                                st.write("Please click 'Submit' once you have completed the quiz.")
                                if st.button("Submit"):
                                    if len(selected_traits_q1) != 3:
                                        st.warning("Please select exactly 3 traits for Q1.")
                                    elif not selected_single_trait_q2:
                                        st.warning("Please select a single trait for Q2.")
                                    elif len(least_represented_traits_q3) != 3:
                                        st.warning("Please select exactly 3 traits for Q3.")
                                    elif len(selected_traits_q4) != 3:
                                        st.warning("Please select exactly 3 traits for Q4.")
                                    elif not selected_single_trait_q5:
                                        st.warning("Please select a single trait for Q5.")
                                    elif len(least_represented_traits_q6) != 3:
                                        st.warning("Please select exactly 3 traits for Q6.")
                                    elif len(selected_images_q7) != 3:
                                        st.warning("Please select exactly 3 images for Q7.")
                                    elif not st.session_state.selected_image_q8:
                                        st.warning("Please select a single image for Q8.")
                                    elif len(least_represented_images_q9) != 3:
                                        st.warning("Please select exactly 3 images for Q9.")
                                    elif len(selected_modes_q10) != 2:
                                        st.warning("Please select exactly 2 modes for Q10.")
                                    else:
                                        top_two_colors, persona_name, score_counter = run_quiz()
                                        st.write("Your top two colors are: ", ", ".join(top_two_colors))
                                        st.write("Your persona name is: ", persona_name)
                                        st.write("Total Scores for Each Color:")
                                        for color in color_priority:
                                            st.write(f"{color}: {score_counter[color]}")

personality_quiz()
