import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random
from streamlit import caching
from streamlit.report_thread import get_report_ctx

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def personality_quiz():
    traits = [
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

    ctx = get_report_ctx()
    session_state = SessionState(ctx=ctx)

    if not hasattr(session_state, 'random_traits_q1'):
        session_state.random_traits_q1 = random.sample(traits, len(traits))
    
    if not hasattr(session_state, 'random_remaining_traits_q3'):
        session_state.random_remaining_traits_q3 = random.sample([trait for trait in traits if trait not in session_state.selected_traits_q1], len([trait for trait in traits if trait not in session_state.selected_traits_q1]))

    if not hasattr(session_state, 'random_traits_q4'):
        session_state.random_traits_q4 = random.sample([
            "Influential",
            "Adventurous",
            "Tough",
            "Expressive",
            "Polished",
            "Selfless",
            "Playful",
            "Independent",
            "Analytical"
        ], 9)

    if not hasattr(session_state, 'random_remaining_traits_q6'):
        session_state.random_remaining_traits_q6 = random.sample([trait for trait in session_state.random_traits_q4 if trait not in session_state.selected_traits_q4], len([trait for trait in session_state.random_traits_q4 if trait not in session_state.selected_traits_q4]))

    if not hasattr(session_state, 'random_image_files_q7'):
        session_state.random_image_files_q7 = random.sample([
            "OrangeSet.jpg",
            "BrownSet.jpg",
            "RedSet.jpg",
            "YellowSet.jpg",
            "PurpleSet.jpg",
            "BlueSet.jpg",
            "GreenSet.jpg",
            "PinkSet.jpg",
            "BlackSet.jpg"
        ], 9)

    if not hasattr(session_state, 'random_remaining_images_q9'):
        session_state.random_remaining_images_q9 = random.sample([file for file in session_state.random_image_files_q7 if file not in session_state.selected_images_q7], len([file for file in session_state.random_image_files_q7 if file not in session_state.selected_images_q7]))

    if not hasattr(session_state, 'random_modes_of_connection'):
        session_state.random_modes_of_connection = random.sample([
            "Achieve With Me",
            "Explore With Me",
            "Strive With Me",
            "Create With Me",
            "Refine With Me",
            "Care With Me",
            "Enjoy With Me",
            "Defy With Me",
            "Invent With Me"
        ], 9)

    if not hasattr(session_state, 'selected_traits_q1'):
        session_state.selected_traits_q1 = []
    
    if not hasattr(session_state, 'selected_single_trait_q2'):
        session_state.selected_single_trait_q2 = ""

    if not hasattr(session_state, 'least_represented_traits_q3'):
        session_state.least_represented_traits_q3 = []
    
    if not hasattr(session_state, 'selected_traits_q4'):
        session_state.selected_traits_q4 = []
    
    if not hasattr(session_state, 'selected_single_trait_q5'):
        session_state.selected_single_trait_q5 = ""
    
    if not hasattr(session_state, 'least_represented_traits_q6'):
        session_state.least_represented_traits_q6 = []
    
    if not hasattr(session_state, 'selected_images_q7'):
        session_state.selected_images_q7 = []
    
    if not hasattr(session_state, 'selected_image_q8'):
        session_state.selected_image_q8 = ""
    
    if not hasattr(session_state, 'least_represented_images_q9'):
        session_state.least_represented_images_q9 = []
    
    if not hasattr(session_state, 'selected_modes_q10'):
        session_state.selected_modes_q10 = []

    def run_quiz():
        score_counter = Counter({color: 3 for color in color_priority})  # Start with 3 points for each color

        for answer in session_state.selected_traits_q1:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[session_state.selected_single_trait_q2]] += 1
        for answer in session_state.least_represented_traits_q3:
            score_counter[trait_score_map[answer]] -= 1
        for answer in session_state.selected_traits_q4:
            score_counter[trait_score_map[answer]] += 1
        score_counter[trait_score_map[session_state.selected_single_trait_q5]] += 1
        for answer in session_state.least_represented_traits_q6:
            score_counter[trait_score_map[answer]] -= 1
        for image in session_state.selected_images_q7:
            score_counter[image_score_map[image]] += 1
        score_counter[image_score_map[session_state.selected_image_q8]] += 1
        for image in session_state.least_represented_images_q9:
            score_counter[image_score_map[image]] -= 1
        for mode in session_state.selected_modes_q10:
            score_counter[trait_score_map[mode]] += 1

        sorted_scores = sorted(score_counter.items(), key=lambda item: (-item[1], color_priority.index(item[0])))
        top_two_colors = [color for color, _ in sorted_scores[:2]]
        persona_name = get_persona_name(top_two_colors[0], top_two_colors[1])
        return top_two_colors, persona_name, score_counter

    def get_persona_name(primary_color, secondary_color):
        persona_map = {
            ("Blue", "Maroon"): "Champion",
            ("Blue", "Green"): "Captain",
            ("Blue", "Orange"): "Director",
            ("Blue", "Pink"): "Producer",
            ("Blue", "Purple"): "Mentor",
            ("Blue", "Red"): "Coach",
            ("Blue", "Silver"): "Maverick",
            ("Blue", "Yellow"): "Visionary",
            ("Blue", "Beige"): "Achiever",
            ("Maroon", "Blue"): "Contender",
            ("Maroon", "Green"): "Need to Find",
            ("Maroon", "Orange"): "Maker",
            ("Maroon", "Pink"): "Precisionist",
            ("Maroon", "Purple"): "Protector",
            ("Maroon", "Red"): "Energizer",
            ("Maroon", "Silver"): "Dark Horse",
            ("Maroon", "Yellow"): "Challenger",
            ("Maroon", "Beige"): "Competitor",
            ("Green", "Blue"): "Trailblazer",
            ("Green", "Maroon"): "Adventurer",
            ("Green", "Orange"): "Seeker",
            ("Green", "Pink"): "Detective",
            ("Green", "Purple"): "Ambassador",
            ("Green", "Red"): "Globetrotter",
            ("Green", "Silver"): "Ranger",
            ("Green", "Yellow"): "Researcher",
            ("Green", "Beige"): "Explorer",
            ("Orange", "Blue"): "Architect",
            ("Orange", "Maroon"): "Artisan",
            ("Orange", "Green"): "Searcher",
            ("Orange", "Pink"): "Composer",
            ("Orange", "Purple"): "Curator",
            ("Orange", "Red"): "Storyteller",
            ("Orange", "Silver"): "Nonconformist",
            ("Orange", "Yellow"): "Ideator",
            ("Orange", "Beige"): "Creator",
            ("Pink", "Blue"): "Connoisseur",
            ("Pink", "Maroon"): "Perfectionist",
            ("Pink", "Green"): "Philosopher",
            ("Pink", "Orange"): "Virtuoso",
            ("Pink", "Purple"): "Idealist",
            ("Pink", "Red"): "Aficionado",
            ("Pink", "Silver"): "Refiner",
            ("Pink", "Yellow"): "Trendsetter",
            ("Pink", "Beige"): "Sophisticate",
            ("Purple", "Blue"): "Guide",
            ("Purple", "Maroon"): "Guardian",
            ("Purple", "Green"): "Shepherd",
            ("Purple", "Orange"): "Patron",
            ("Purple", "Pink"): "Confidant",
            ("Purple", "Red"): "Host",
            ("Purple", "Silver"): "Advocate",
            ("Purple", "Yellow"): "Advisor",
            ("Purple", "Beige"): "Provider",
            ("Red", "Blue"): "Motivator",
            ("Red", "Maroon"): "Dynamo",
            ("Red", "Green"): "Thrill-seeker",
            ("Red", "Orange"): "Performer",
            ("Red", "Pink"): "Enthusiast",
            ("Red", "Purple"): "Emcee",
            ("Red", "Silver"): "DaRedevil",
            ("Red", "Yellow"): "Magician",
            ("Red", "Beige"): "Entertainer",
            ("Silver", "Blue"): "Ringleader",
            ("Silver", "Maroon"): "Instigator",
            ("Silver", "Green"): "Rogue",
            ("Silver", "Orange"): "Renegade",
            ("Silver", "Pink"): "Individualist",
            ("Silver", "Purple"): "Activist",
            ("Silver", "Red"): "Rock Star",
            ("Silver", "Yellow"): "Free-thinker",
            ("Silver", "Beige"): "Rebel",
            ("Yellow", "Blue"): "Vanguard",
            ("Yellow", "Maroon"): "Inventor",
            ("Yellow", "Green"): "Theorist",
            ("Yellow", "Orange"): "Originator",
            ("Yellow", "Pink"): "Dreamer",
            ("Yellow", "Purple"): "Oracle",
            ("Yellow", "Red"): "Futurist",
            ("Yellow", "Silver"): "Reformer",
            ("Yellow", "Beige"): "Innovator"
        }

        return persona_map.get((primary_color, secondary_color), "")

    st.title('CollegeXpress Personality Survey')

    st.write("Q1. Here is a list of 9 traits that could make up your personality. "
             "Please select exactly 3 traits that best represent who you are.")
    for trait in session_state.random_traits_q1:
        selected = st.checkbox(trait, key=f"checkbox_q1_{trait}")
        if selected:
            session_state.selected_traits_q1.append(trait)

    if len(session_state.selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")

    st.write("---")

    if len(session_state.selected_traits_q1) == 3:
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        session_state.selected_single_trait_q2 = st.radio("", session_state.selected_traits_q1, key="radio_q2")

        st.write("---")

        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        for trait in session_state.random_remaining_traits_q3:
            selected = st.checkbox(trait, key=f"checkbox_q3_{trait}")
            if selected:
                session_state.least_represented_traits_q3.append(trait)

        if len(session_state.least_represented_traits_q3) != 3:
            st.warning("Please select exactly 3 traits.")

        st.write("---")

        if len(session_state.least_represented_traits_q3) == 3:
            st.write("Q4. Here is a new list of 9 traits that could make up your personality. "
                     "Please select exactly 3 traits that best represent who you are.")
            for trait in session_state.random_traits_q4:
                selected = st.checkbox(trait, key=f"checkbox_q4_{trait}")
                if selected:
                    session_state.selected_traits_q4.append(trait)

            if len(session_state.selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")

            st.write("---")

            if len(session_state.selected_traits_q4) == 3:
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                session_state.selected_single_trait_q5 = st.radio("", session_state.selected_traits_q4, key="radio_q5")

                st.write("---")

                for trait in session_state.random_remaining_traits_q6:
                    selected = st.checkbox(trait, key=f"checkbox_q6_{trait}")
                    if selected:
                        session_state.least_represented_traits_q6.append(trait)

                if len(session_state.least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")

                st.write("---")

                if len(session_state.least_represented_traits_q6) == 3:
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. "
                             "Please take a moment to view all the groups. Then select the 3 that best represent who you are.")

                    for i, file in enumerate(session_state.random_image_files_q7):
                        image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                        response = requests.get(image_url)
                        image = Image.open(BytesIO(response.content))
                        selected = st.checkbox("", key=f"q7_{i}")
                        if selected:
                            session_state.selected_images_q7.append(file)
                        st.image(image, use_column_width=True)

                    if len(session_state.selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")

                    st.write("---")

                    if len(session_state.selected_images_q7) == 3:
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")

                        for i, file in enumerate(session_state.selected_images_q7):
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            selected = st.checkbox("", key=f"q8_{i}")
                            st.image(image, use_column_width=True)
                            if selected:
                                if session_state.selected_image_q8:
                                    st.warning("Please select only one image.")
                                else:
                                    session_state.selected_image_q8 = file

                        st.write("Your selected image: ")
                        if session_state.selected_image_q8:
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{session_state.selected_image_q8}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            st.image(image, use_column_width=True)

                        st.write("---")

                        if session_state.selected_image_q8:
                            st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")

                            for i, file in enumerate(session_state.random_remaining_images_q9):
                                image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                                response = requests.get(image_url)
                                image = Image.open(BytesIO(response.content))
                                selected = st.checkbox("", key=f"q9_{i}")
                                if selected:
                                    session_state.least_represented_images_q9.append(file)
                                st.image(image, use_column_width=True)

                            if len(session_state.least_represented_images_q9) != 3:
                                st.warning("Please select exactly 3 images.")

                            st.write("---")

                            if len(session_state.least_represented_images_q9) == 3:
                                st.write("Q10. Below are 9 things called 'Modes of Connection.' They describe how a person can make an impression, grow friendships, and inspire others. "
                                         "Which two 'Modes of Connection' sound most like what you would use to make an impression, grow friendships, and inspire others?")

                                for mode in session_state.random_modes_of_connection:
                                    selected = st.checkbox(mode, key=f"checkbox_q10_{mode}")
                                    if selected:
                                        session_state.selected_modes_q10.append(mode)

                                if len(session_state.selected_modes_q10) != 2:
                                    st.warning("Please select exactly 2 modes.")

                                st.write("---")

                                st.write("Please click 'Submit' once you have completed the quiz.")
                                if st.button("Submit"):
                                    if len(session_state.selected_traits_q1) != 3:
                                        st.warning("Please select exactly 3 traits for Q1.")
                                    elif not session_state.selected_single_trait_q2:
                                        st.warning("Please select a single trait for Q2.")
                                    elif len(session_state.least_represented_traits_q3) != 3:
                                        st.warning("Please select exactly 3 traits for Q3.")
                                    elif len(session_state.selected_traits_q4) != 3:
                                        st.warning("Please select exactly 3 traits for Q4.")
                                    elif not session_state.selected_single_trait_q5:
                                        st.warning("Please select a single trait for Q5.")
                                    elif len(session_state.least_represented_traits_q6) != 3:
                                        st.warning("Please select exactly 3 traits for Q6.")
                                    elif len(session_state.selected_images_q7) != 3:
                                        st.warning("Please select exactly 3 images for Q7.")
                                    elif not session_state.selected_image_q8:
                                        st.warning("Please select a single image for Q8.")
                                    elif len(session_state.least_represented_images_q9) != 3:
                                        st.warning("Please select exactly 3 images for Q9.")
                                    elif len(session_state.selected_modes_q10) != 2:
                                        st.warning("Please select exactly 2 modes for Q10.")
                                    else:
                                        top_two_colors, persona_name, score_counter = run_quiz()
                                        st.write("Your top two colors are: ", ", ".join(top_two_colors))
                                        st.write("Your persona name is: ", persona_name)
                                        st.write("Total Scores for Each Color:")
                                        for color in color_priority:
                                            st.write(f"{color}: {score_counter[color]}")

personality_quiz()
