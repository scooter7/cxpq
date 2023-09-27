import streamlit as st
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import random

def personality_quiz():
    trait_score_map = {"Confident": "Blue", "Curious": "Green", "Determined": "Maroon", "Imaginative": "Orange", "Poised": "Pink", "Compassionate": "Purple", "Enthusiastic": "Red", "Bold": "Silver", "Innovative": "Yellow", "Influential": "Blue", "Adventurous": "Green", "Tough": "Maroon", "Expressive": "Orange", "Polished": "Pink", "Selfless": "Purple", "Playful": "Red", "Independent": "Silver", "Analytical": "Yellow", "Achieve With Me": "Blue", "Explore With Me": "Green", "Strive With Me": "Maroon", "Create With Me": "Orange", "Refine With Me": "Pink", "Care With Me": "Purple", "Enjoy With Me": "Red", "Defy With Me": "Silver", "Invent With Me": "Yellow",}
    image_score_map = {"OrangeSet.jpg": "Orange", "BrownSet.jpg": "Maroon", "RedSet.jpg": "Red", "YellowSet.jpg": "Yellow", "PurpleSet.jpg": "Purple", "BlueSet.jpg": "Blue", "GreenSet.jpg": "Green", "PinkSet.jpg": "Pink", "BlackSet.jpg": "Silver",}
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
        persona_map = {("Blue", "Maroon"): "Champion", ("Blue", "Green"): "Captain", ("Blue", "Orange"): "Director", ("Blue", "Pink"): "Producer", ("Blue", "Purple"): "Mentor", ("Blue", "Red"): "Coach", ("Blue", "Silver"): "Maverick", ("Blue", "Yellow"): "Visionary", ("Maroon", "Blue"): "Contender", ("Maroon", "Green"): "Need to Find", ("Maroon", "Orange"): "Maker", ("Maroon", "Pink"): "Precisionist", ("Maroon", "Purple"): "Protector", ("Maroon", "Red"): "Energizer", ("Maroon", "Silver"): "Dark Horse", ("Maroon", "Yellow"): "Challenger", ("Green", "Blue"): "Trailblazer", ("Green", "Maroon"): "Adventurer", ("Green", "Orange"): "Seeker", ("Green", "Pink"): "Detective", ("Green", "Purple"): "Ambassador", ("Green", "Red"): "Globetrotter", ("Green", "Silver"): "Ranger", ("Green", "Yellow"): "Researcher", ("Orange", "Blue"): "Architect", ("Orange", "Maroon"): "Artisan", ("Orange", "Green"): "Searcher", ("Orange", "Pink"): "Composer", ("Orange", "Purple"): "Curator", ("Orange", "Red"): "Storyteller", ("Orange", "Silver"): "Nonconformist", ("Orange", "Yellow"): "Ideator", ("Pink", "Blue"): "Connoisseur", ("Pink", "Maroon"): "Perfectionist", ("Pink", "Green"): "Philosopher", ("Pink", "Orange"): "Virtuoso", ("Pink", "Purple"): "Idealist", ("Pink", "Red"): "Aficionado", ("Pink", "Silver"): "Refiner", ("Pink", "Yellow"): "Trendsetter", ("Purple", "Blue"): "Guide", ("Purple", "Maroon"): "Guardian", ("Purple", "Green"): "Shepherd", ("Purple", "Orange"): "Patron", ("Purple", "Pink"): "Confidant", ("Purple", "Red"): "Host", ("Purple", "Silver"): "Advocate", ("Purple", "Yellow"): "Advisor", ("Red", "Blue"): "Motivator", ("Red", "Maroon"): "Dynamo", ("Red", "Green"): "Thrill-seeker", ("Red", "Orange"): "Performer", ("Red", "Pink"): "Enthusiast", ("Red", "Purple"): "Emcee", ("Red", "Silver"): "DaRedevil", ("Red", "Yellow"): "Magician", ("Silver", "Blue"): "Ringleader", ("Silver", "Maroon"): "Instigator", ("Silver", "Green"): "Rogue", ("Silver", "Orange"): "Renegade", ("Silver", "Pink"): "Individualist", ("Silver", "Purple"): "Activist", ("Silver", "Red"): "Rock Star", ("Silver", "Yellow"): "Free-thinker", ("Yellow", "Blue"): "Vanguard", ("Yellow", "Maroon"): "Inventor", ("Yellow", "Green"): "Theorist", ("Yellow", "Orange"): "Originator", ("Yellow", "Pink"): "Dreamer", ("Yellow", "Purple"): "Oracle", ("Yellow", "Red"): "Futurist", ("Yellow", "Silver"): "Reformer",}
        return persona_map.get((primary_color, secondary_color), "")
    
    st.title('Personality Survey')
    st.write("Q1. Here is a list of 9 traits that could make up your personality. "
             "Please select exactly 3 traits that best represent who you are.")
    traits = ["Confident", "Curious", "Determined", "Imaginative", "Poised", "Compassionate", "Enthusiastic", "Bold", "Innovative"]
    random.seed(st.session_state.get('random_seed', 0))
    random.shuffle(traits)
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
            st.write("Q4. Here is a new list of 9 traits that could make up your personality. "
                     "Please select exactly 3 traits that best represent who you are.")
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
                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")
                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]
                random.seed(st.session_state.get('random_seed', 0))
                random.shuffle(remaining_traits_q6)
                least_represented_traits_q6 = [trait for trait in remaining_traits_q6 if st.checkbox(trait, key=f"checkbox_q6_{trait}")]
                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")
                st.write("---")
                if len(least_represented_traits_q6) == 3:
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. "
                             "Please select the 3 that best represent who you are.")
                    image_files_q7 = ["OrangeSet.jpg", "BrownSet.jpg", "RedSet.jpg", "YellowSet.jpg", "PurpleSet.jpg", "BlueSet.jpg", "GreenSet.jpg", "PinkSet.jpg", "BlackSet.jpg"]
                    random.seed(st.session_state.get('random_seed', 0))
                    random.shuffle(image_files_q7)
                    selected_images_q7 = []
                    for file in image_files_q7:
                        image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                        response = requests.get(image_url)
                        image = Image.open(BytesIO(response.content))
                        selected = st.checkbox("", key=f"q7_{file}")
                        st.image(image, use_column_width=True)
                        if selected:
                            selected_images_q7.append(file)
                    if len(selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")
                    st.write("---")
                    if len(selected_images_q7) == 3:
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")
                        selected_image_q8 = st.selectbox("", selected_images_q7, key="radio_q8")
                        st.write("---")
                        st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")
                        remaining_images_q9 = [file for file in image_files_q7 if file not in selected_images_q7]
                        random.seed(st.session_state.get('random_seed', 0))
                        random.shuffle(remaining_images_q9)
                        least_represented_images_q9 = []
                        for file in remaining_images_q9:
                            image_url = f"https://raw.githubusercontent.com/scooter7/cxpq/main/{file}"
                            response = requests.get(image_url)
                            image = Image.open(BytesIO(response.content))
                            selected = st.checkbox("", key=f"q9_{file}")
                            st.image(image, use_column_width=True)
                            if selected:
                                least_represented_images_q9.append(file)
                        if len(least_represented_images_q9) != 3:
                            st.warning("Please select exactly 3 images.")
                        st.write("---")
                        if len(least_represented_images_q9) == 3:
                            st.write("Q10. Below are 9 things called 'Modes of Connection.' "
                                     "Please read each mode and select exactly 3 that best represent who you are.")
                            modes_q10 = ["Achieve With Me", "Explore With Me", "Strive With Me", "Create With Me", "Refine With Me", "Care With Me", "Enjoy With Me", "Defy With Me", "Invent With Me"]
                            random.seed(st.session_state.get('random_seed', 0))
                            random.shuffle(modes_q10)
                            selected_modes_q10 = [mode for mode in modes_q10 if st.checkbox(mode, key=f"checkbox_q10_{mode}")]
                            if len(selected_modes_q10) != 3:
                                st.warning("Please select exactly 3 modes.")
                            st.write("---")
                            if len(selected_modes_q10) == 3:
                                colors, persona_name, score_counter = run_quiz()
                                st.write(f"Your persona is {persona_name}. Here is how you scored in each color:")
                                st.bar_chart(score_counter)

if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(0, 1000000)
    
personality_quiz()
