import streamlit as st
from PIL import Image
from collections import Counter

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
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\OrangeSet.jpg": "Orange",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BrownSet.jpg": "Maroon",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\RedSet.jpg": "Red",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\YellowSet.jpg": "Yellow",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\PurpleSet.jpg": "Purple",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BlueSet.jpg": "Blue",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\GreenSet.jpg": "Green",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\PinkSet.jpg": "Pink",
        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BlackSet.jpg": "Silver",
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
        return top_two_colors, persona_name

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
    st.write("Welcome to the CollegeXpress personality survey, powered by Carnegie. "
             "In the next ten to fifteen minutes, you will be asked a series of questions "
             "aimed at determining your authentic personality, defined by our 9-archetype theory. "
             "There are no right or wrong answers. Please think about the questions and your own "
             "personality as what is true both in your student life and personal life. "
             "If you are stuck between two options, select the option that is most accurate on your best day.")

    st.write("---")

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

    st.write("Q1. Here is a list of 9 traits that could make up your personality. "
             "Please select exactly 3 traits that best represent who you are.")
    selected_traits_q1 = st.multiselect("Select three traits", traits, [], key="checkbox_q1")

    if len(selected_traits_q1) != 3:
        st.warning("Please select exactly 3 traits.")

    st.write("---")

    if len(selected_traits_q1) == 3:
        st.write("Q2. Of the 3 traits you selected, which single trait is most like you?")
        selected_single_trait_q2 = st.selectbox("", selected_traits_q1, key="select_q2")

        st.write("---")

        st.write("Your selected single trait: ", selected_single_trait_q2)

        st.write("---")

        st.write("Q3. Now think about this list and select the 3 traits that least represent who you are.")
        remaining_traits_q3 = [trait for trait in traits if trait not in selected_traits_q1]
        least_represented_traits_q3 = st.multiselect("", remaining_traits_q3, [], key="checkbox_q3")

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
            selected_traits_q4 = st.multiselect("Select three traits", traits_q4, [], key="checkbox_q4")

            if len(selected_traits_q4) != 3:
                st.warning("Please select exactly 3 traits.")

            st.write("---")

            if len(selected_traits_q4) == 3:
                st.write("Q5. Of the 3 traits you selected, which single trait is most like you?")
                selected_single_trait_q5 = st.selectbox("", selected_traits_q4, key="select_q5")

                st.write("---")

                st.write("Your selected single trait: ", selected_single_trait_q5)

                st.write("---")

                remaining_traits_q6 = [trait for trait in traits_q4 if trait not in selected_traits_q4]

                st.write("Q6. Now think about this list and select the 3 traits that least represent who you are.")
                least_represented_traits_q6 = st.multiselect("", remaining_traits_q6, [], key="checkbox_q6")

                if len(least_represented_traits_q6) != 3:
                    st.warning("Please select exactly 3 traits.")

                st.write("---")

                if len(least_represented_traits_q6) == 3:
                    st.write("Q7. On this page there are 9 groups of icons meant to represent personalities. "
                             "Please take a moment to view all the groups. Then select the 3 that best represent who you are.")

                    image_files_q7 = [
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\OrangeSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BrownSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\RedSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\YellowSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\PurpleSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BlueSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\GreenSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\PinkSet.jpg",
                        "C:\\Users\\jvineburgh\\OneDrive - Clarus Corporation\\Desktop\\BlackSet.jpg"
                    ]

                    selected_images_q7 = []

                    for i, file in enumerate(image_files_q7):
                        selected = st.checkbox("", key=f"q7_{i}")
                        if selected:
                            selected_images_q7.append(file)
                        st.image(Image.open(file), use_column_width=True)

                    if len(selected_images_q7) != 3:
                        st.warning("Please select exactly 3 images.")

                    st.write("---")

                    if len(selected_images_q7) == 3:
                        st.write("Q8. Of the 3 you selected, which group of icons is most like you?")

                        selected_image_q8 = None

                        for i, file in enumerate(selected_images_q7):
                            selected = st.checkbox("", key=f"q8_{i}")
                            st.image(Image.open(file), use_column_width=True)
                            if selected:
                                if selected_image_q8:
                                    st.warning("Please select only one image.")
                                else:
                                    selected_image_q8 = file

                        st.write("Your selected image: ")
                        if selected_image_q8:
                            st.image(Image.open(selected_image_q8), use_column_width=True)

                        st.write("---")

                        if selected_image_q8:
                            st.write("Q9. Now think about these icon groups remaining and select the 3 that least represent who you are.")
                            remaining_images_q9 = [file for file in image_files_q7 if file not in selected_images_q7]

                            least_represented_images_q9 = []

                            for i, file in enumerate(remaining_images_q9):
                                selected = st.checkbox("", key=f"q9_{i}")
                                if selected:
                                    least_represented_images_q9.append(file)
                                st.image(Image.open(file), use_column_width=True)

                            if len(least_represented_images_q9) != 3:
                                st.warning("Please select exactly 3 images.")

                            st.write("---")

                            if len(least_represented_images_q9) == 3:
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

                                selected_modes_q10 = st.multiselect("Select two modes", modes_of_connection, [], key="checkbox_q10")

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
        elif not selected_image_q8:
            st.warning("Please select a single image for Q8.")
        elif len(least_represented_images_q9) != 3:
            st.warning("Please select exactly 3 images for Q9.")
        elif len(selected_modes_q10) != 2:
            st.warning("Please select exactly 2 modes for Q10.")
        else:
            top_two_colors, persona_name = run_quiz()
            st.write("Your top two colors are: ", ", ".join(top_two_colors))
            st.write("Your persona name is: ", persona_name)

personality_quiz()
