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

    random.seed(42)
    random.shuffle(traits)

    st.write("Q1. Here is a list of 9 traits that could make up your personality. "
             "Please select exactly 3 traits that best represent who you are.")
    selected_traits_q1 = []
    for trait in traits:
        selected = st.checkbox(trait, key=f"checkbox_q1_{trait}")
        if selected:
            selected_traits_q1.append(trait)

    if len(selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")

    st.write("---")

    if len(selected_traits_q1) == 3:
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q2 = st.radio("", selected_traits_q1, key="radio_q2")

        st.write("---")

        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits if trait not in selected_traits_q1]

        random.shuffle(remaining_traits_q3)

        least_represented_traits_q3 = []
        for trait in remaining_traits_q3:
            selected = st.checkbox(trait, key=f"checkbox_q3_{trait}")
            if selected:
                least_represented_traits_q3.append(trait)

        if len(least_represented_traits_q3) != 3:
            st.warning("Please select exactly 3 traits.")

        st.write("---")

        if len(least_represented_traits_q3) == 3:
            st.write("Q4. Here is a new list of 9 traits that could make up your personality. "
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

            random.shuffle(traits_q4)

            selected_traits_q4 = []
            for trait in traits_q4:
                selected = st.checkbox(trait, key=f"checkbox_q4_{trait}")
                if selected:
                    selected_traits_q4.append(trait)

            if len(selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")

            st.write("---")

            if len(selected_traits_q4) == 3:
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                selected_single_trait_q5 = st.radio("", selected_traits_q4, key="radio_q5")

                st.write("---")

                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]

                random.shuffle(remaining_traits_q6)

                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")

                least_represented_traits_q6 = []
                for trait in remaining_traits_q6:
                    selected = st.checkbox(trait, key=f"checkbox_q6_{trait}")
                    if selected:
                        least_represented_traits_q6.append(trait)

                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")

                st.write("---")

                if len(least_represented_traits_q6) == 3:
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

                    random.shuffle(image_files_q7)

                    selected_images_q7 = []

                    for i, file in enumerate(image_files_q7):
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

                            random.shuffle(remaining_images_q9)

                            least_represented_images_q9 = []

                            for i, file in enumerate(remaining_images_q9):
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
                                st.write("Q10. Below are 9 things called 'Modes of Connection.' They describe how a person can make an impression, grow friendships, and inspire others. "
                                         "Please select the 3 that best describe you.")

                                modes_q10 = [
                                    "Advocate",
                                    "Ambassador",
                                    "Architect",
                                    "Connoisseur",
                                    "Maverick",
                                    "Visionary",
                                    "Nonconformist",
                                    "Creator",
                                    "Researcher"
                                ]

                                random.shuffle(modes_q10)

                                selected_modes_q10 = []

                                for mode in modes_q10:
                                    selected = st.checkbox(mode, key=f"checkbox_q10_{mode}")
                                    if selected:
                                        selected_modes_q10.append(mode)

                                if len(selected_modes_q10) != 3:
                                    st.warning("Please select exactly 3 modes.")

                                st.write("---")

                                if len(selected_modes_q10) == 3:
                                    st.write("Thank you for completing the survey!")

                                    top_two_colors, persona_name, score_counter = run_quiz()

                                    st.write(f"Your top two colors are {top_two_colors[0]} and {top_two_colors[1]}.")
                                    st.write(f"Your persona name is {persona_name}.")
                                    st.write("Here is the breakdown of your scores:")
                                    for color, score in score_counter.items():
                                        st.write(f"- {color}: {score}")

                                    st.write("---")
                                    st.write("Would you like to save your results?")

                                    if st.button("Submit"):
                                        st.success("Results submitted successfully!")

    if not selected_traits_q1:
        st.warning("Please complete all the questions.")

personality_quiz()
