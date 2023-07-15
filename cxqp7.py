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

    random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
    random.shuffle(traits)  # Randomize the order of traits

    q1_placeholder = st.empty()
    q1_placeholder.write("Q1. Here is a list of 9 traits that could make up your personality. "
                     "Please select exactly 3 traits that best represent who you are.")
    selected_traits_q1 = []
    for trait in traits:
        selected = q1_placeholder.checkbox(trait, key=f"checkbox_q1_{trait}")
        if selected:
            selected_traits_q1.append(trait)

    if len(selected_traits_q1) != 3:
        q1_placeholder.warning("Please select exactly 3 traits.")

    q2_placeholder = st.empty()
    q3_placeholder = st.empty()
    q4_placeholder = st.empty()
    q5_placeholder = st.empty()
    q6_placeholder = st.empty()
    q7_placeholder = st.empty()
    q8_placeholder = st.empty()
    q9_placeholder = st.empty()
    q10_placeholder = st.empty()
    submit_button_placeholder = st.empty()

    if len(selected_traits_q1) == 3:
        q2_placeholder.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q2 = q2_placeholder.selectbox("", selected_traits_q1, key="radio_q2")

        q3_placeholder.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits if trait not in selected_traits_q1]

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(remaining_traits_q3)  # Randomize the order of remaining_traits_q3

        least_represented_traits_q3 = []
        for trait in remaining_traits_q3:
            selected = q3_placeholder.checkbox(trait, key=f"checkbox_q3_{trait}")
            if selected:
                least_represented_traits_q3.append(trait)

        if len(least_represented_traits_q3) != 3:
            q3_placeholder.warning("Please select exactly 3 traits.")

    if len(least_represented_traits_q3) == 3:
        q4_placeholder.write("Q4. Here is a new list of 9 traits that could make up your personality. "
                     "Please select exactly 3 traits that best represent who you are.")
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

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(traits_q4)  # Randomize the order of traits_q4

        selected_traits_q4 = []
        for trait in traits_q4:
            selected = q4_placeholder.checkbox(trait, key=f"checkbox_q4_{trait}")
            if selected:
                selected_traits_q4.append(trait)

        if len(selected_traits_q4) != 3:
            q4_placeholder.warning("Please select exactly 3 traits.")

    if len(selected_traits_q4) == 3:
        q5_placeholder.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q5 = q5_placeholder.selectbox("", selected_traits_q4, key="radio_q5")

        remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(remaining_traits_q6)  # Randomize the order of remaining_traits_q6

        q6_placeholder.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")

        least_represented_traits_q6 = []
        for trait in remaining_traits_q6:
            selected = q6_placeholder.checkbox(trait, key=f"checkbox_q6_{trait}")
            if selected:
                least_represented_traits_q6.append(trait)

        if len(least_represented_traits_q6) != 3:
            q6_placeholder.warning("Please select exactly 3 traits.")

    if len(least_represented_traits_q6) == 3:
        q7_placeholder.write("Q7. On this page there are 9 groups of icons meant to represent personalities. "
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

        selected_images_q7 = []

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(image_files_q7)  # Randomize the order of image_files_q7

        for i in range(0, len(image_files_q7), 3):
            cols = q7_placeholder.columns(3)
            for j in range(3):
                if i + j < len(image_files_q7):  # check if index exists
                    file = image_files_q7[i + j]
                    image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    selected = cols[j].checkbox("", key=f"q7_{i+j}")
                    if selected:
                        selected_images_q7.append(file)
                    cols[j].image(image, use_column_width=True)

        if len(selected_images_q7) != 3:
            q7_placeholder.warning("Please select exactly 3 images.")

    if len(selected_images_q7) == 3:
        q8_placeholder.write("Q8. Of the 3 groups of icons you selected, which single group is most like you?")
        selected_image_q8 = q8_placeholder.selectbox("", selected_images_q7, key="radio_q8")

        remaining_images_q9 = [file for file in image_files_q7 if file not in selected_images_q7]

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(remaining_images_q9)  # Randomize the order of remaining_images_q9

        q9_placeholder.write("Q9. Now think about this list and select the 3 groups of icons that least represent who you are.")

        least_represented_images_q9 = []
        for i in range(0, len(remaining_images_q9), 3):
            cols = q9_placeholder.columns(3)
            for j in range(3):
                if i + j < len(remaining_images_q9):  # check if index exists
                    file = remaining_images_q9[i + j]
                    image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    selected = cols[j].checkbox("", key=f"q9_{i+j}")
                    if selected:
                        least_represented_images_q9.append(file)
                    cols[j].image(image, use_column_width=True)

        if len(least_represented_images_q9) != 3:
            q9_placeholder.warning("Please select exactly 3 images.")

    if len(least_represented_images_q9) == 3:
        q10_placeholder.write("Q10. Here is a list of 9 modes of thought that could make up your personality. "
                     "Please select exactly 3 modes that best represent who you are.")

        modes_q10 = [
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

        random.seed(st.session_state.get('random_seed', 0))  # Set the random seed
        random.shuffle(modes_q10)  # Randomize the order of modes_q10

        selected_modes_q10 = []
        for mode in modes_q10:
            selected = q10_placeholder.checkbox(mode, key=f"checkbox_q10_{mode}")
            if selected:
                selected_modes_q10.append(mode)

        if len(selected_modes_q10) != 3:
            q10_placeholder.warning("Please select exactly 3 modes.")

    if len(selected_modes_q10) == 3:
        submit_button_placeholder.empty()
        submit_button_placeholder.button("Submit")

    if submit_button_placeholder.button_clicked:
        top_two_colors, persona_name, score_counter = run_quiz()

        q1_placeholder.empty()
        q2_placeholder.empty()
        q3_placeholder.empty()
        q4_placeholder.empty()
        q5_placeholder.empty()
        q6_placeholder.empty()
        q7_placeholder.empty()
        q8_placeholder.empty()
        q9_placeholder.empty()
        q10_placeholder.empty()
        submit_button_placeholder.empty()

        st.subheader(f"Congratulations! Your top two colors are {top_two_colors[0]} and {top_two_colors[1]}.")
        st.write(f"You are a {persona_name}!")
        st.write("Here are the scores for each color:")
        st.write(score_counter)

personality_quiz()
