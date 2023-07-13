import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random
import hashlib

# Function to create a seed from the user session and question number
def create_seed(session_id, question_number):
    # Use a hash function to ensure the seed is an integer
    seed = int(hashlib.sha256(f"{session_id}{question_number}".encode()).hexdigest(), 16) % 10**8
    return seed

# Function to randomize a list using a seed
def randomize_list(list_str, seed):
    options = list_str.split(', ')
    random.seed(seed)
    random_options = random.sample(options, len(options))
    random_list_str = ', '.join(random_options)
    return random_list_str

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
            ("Blue", "Maroon"): "Champion",
            ("Blue", "Green"): "Captain",
            # ... (omitted for brevity)
        }
        return persona_map.get((primary_color, secondary_color), "")

    st.title('CollegeXpress Personality Survey')

    # Placeholder for the user session ID
    # In a real application, this should be replaced with the actual session ID
    session_id = 1

    # Randomize the traits for question 1
    traits_q1 = [
        "Confident",
        "Curious",
        "Determined",
        "Imaginative",
        "Poised",
        "Compassionate",
        "Enthusiastic",
        "Bold",
        "Innovative"
    ]
    traits_q1 = randomize_list(traits_q1, create_seed(session_id, 1))

    st.write("Q1. Here is a list of 9 traits that could make up your personality. "
             "Please select exactly 3 traits that best represent who you are.")
    selected_traits_q1 = st.multiselect("", traits_q1, key="multiselect_q1")
    if len(selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")
    else:
        # Q2
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q2 = st.radio("", selected_traits_q1, key="radio_q2")

        # Q3
        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits_q1 if trait not in selected_traits_q1]
        least_represented_traits_q3 = st.multiselect("", remaining_traits_q3, key="multiselect_q3")
        if len(least_represented_traits_q3) != 3:
            st.warning("Please select exactly 3 traits.")
        else:
            # Q4
            traits_q4 = [
                "Influential",
                "Adventurous",
                "Tough",
                "Expressive",
                "Polished",
                "Selfless",
                "Playful",
                "Independent",
                "Analytical"
            ]
            traits_q4 = randomize_list(traits_q4, create_seed(session_id, 4))

            st.write("Q4. Here is a new list of 9 traits that could make up your personality. "
                     "Please select exactly 3 traits that best represent who you are.")
            selected_traits_q4 = st.multiselect("", traits_q4, key="multiselect_q4")
            if len(selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")
            else:
                # Q5
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                selected_single_trait_q5 = st.radio("", selected_traits_q4, key="radio_q5")

                # Q6
                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")
                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]
                least_represented_traits_q6 = st.multiselect("", remaining_traits_q6, key="multiselect_q6")
                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")
                else:
                    # Q7
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. "
                             "Please take a moment to view all the groups. Then select the 3 that best represent who you are.")
                    image_files_q7 = [
                        "OrangeSet.jpg",
                        "BrownSet.jpg",
                        "RedSet.jpg",
                        "YellowSet.jpg",
                        "PurpleSet.jpg",
                        "BlueSet.jpg",
                        "GreenSet.jpg",
                        "PinkSet.jpg",
                        "BlackSet.jpg"
                    ]
                    selected_images_q7 = st.multiselect("", image_files_q7, key="multiselect_q7")
                    if len(selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")
                    else:
                        # Q8
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")
                        selected_image_q8 = st.radio("", selected_images_q7, key="radio_q8")

                        # Q9
                        st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")
                        remaining_images_q9 = [image for image in image_files_q7 if image not in selected_images_q7]
                        least_represented_images_q9 = st.multiselect("", remaining_images_q9, key="multiselect_q9")
                        if len(least_represented_images_q9) != 3:
                            st.warning("Please select exactly 3 images.")
                        else:
                            # Q10
                            st.write("Q10. Below are 9 things called 'Modes of Connection.' They describe how a person can make an impression, grow friendships, and inspire others. "
                                     "Which two 'Modes of Connection' sound most like what you would use to make an impression, grow friendships, and inspire others?")
                            modes_of_connection = [
                                "Achieve With Me",
                                "Explore With Me",
                                "Strive With Me",
                                "Create With Me",
                                "Refine With Me",
                                "Care With Me",
                                "Enjoy With Me",
                                "Defy With Me",
                                "Invent With Me"
                            ]
                            modes_of_connection = randomize_list(modes_of_connection, create_seed(session_id, 10))
                            selected_modes_q10 = st.multiselect("", modes_of_connection, key="multiselect_q10")
                            if len(selected_modes_q10) != 2:
                                st.warning("Please select exactly 2 modes.")
                            else:
                                # Submit
                                st.write("Please click 'Submit' once you have completed the quiz.")
                                if st.button("Submit"):
                                    top_two_colors, persona_name, score_counter = run_quiz()
                                    st.write("Your top two colors are: ", ", ".join(top_two_colors))
                                    st.write("Your persona name is: ", persona_name)
                                    st.write("Total Scores for Each Color:")
                                    for color in color_priority:
                                        st.write(f"{color}: {score_counter[color]}")

personality_quiz()
