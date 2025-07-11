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
            ("Blue", "Maroon"): "Champion: Champions are driven by growth, being frontrunners, and overcoming challenges. They are the first to battle on behalf of the needs, rights, and honor of others. Just the same, they strive to maintain a healthy and productive headspace, combating their own negative thoughts and patterns to stay positive and focused on the task at hand. Champions pledge themselves to value-oriented missions and strive to succeed at all costs. A determination to prevail causes admiration in those who appreciate the commitment and stamina it takes to win.",
            ("Blue", "Green"): "Captain: Captains are driven by growth, being frontrunners, and by a quest for the unknown. They wield immense influence along each step of a journey due to their natural cool-headedness and single-minded orientation toward objectives. They navigate turbulent and challenging times with confidence. A Captain’s wealth of experience and strong sense of self-control equips them to develop sound strategies and lead others down an exciting yet steady path.",
            ("Blue", "Orange"): "Director: Directors are driven by growth, being frontrunners, and by self-expression and artistry. They are both boldly self-assured and ambiguous when translating their creative vision, being one part leader and one part imaginative artisan. They are most comfortable operating from a vantage point of 10,000 feet, adopting a big-picture perspective and musing upon their creations. Directors balance this tendency with concrete and ordered decision-making, where needed, to bring order to many tangible and intangible moving parts.",
            ("Blue", "Pink"): "Producer: Producers are driven by growth, being frontrunners, and by experience, elegance, and beauty in all its forms. They bring forth timeless ideas and concepts and confidently share them with others. When they aspire to achieve something or pursue a high calling, they continue toward that goal until it is perfected and ready for the grandest of stages. A Producer’s commitment to tradition, their idealism, and their ability to propel all that is around them to perfection guarantees that any project in which they are involved is executed according to schedule, with finesse, and to the utmost quality.",
            ("Blue", "Purple"): "Mentor: Mentors are driven by growth, being frontrunners, and by a need to compassionately care for others. They are known for their capacity as wise and trusted guides whose direction and genuine care empower others on their journeys. Naturally friendly and influential, Mentors pay close attention to the feelings, needs, and wants of others and look for opportunities to lend a helping hand. Much of a Mentor's fulfillment in life comes from propelling others to fulfill their own aspirations. They charge into community-rich environments and provide a reliable support system for all those who might benefit from it.",
            ("Blue", "Red"): "Coach: Coaches are driven by growth and being frontrunners, and a desire to excite others. With boundless reserves of enthusiasm, they train and push others to accomplish their goals, while simultaneously meeting their own. As natural mentors, encouragers, and promoters, they inspire others to give their very best. Coaches bring rigor and vigor to every part of their life and take seriously the responsibility of inspiring others to pursue collective success.",
            ("Blue", "Silver"): "Maverick: Mavericks are driven by growth, being frontrunners, and by a desire to challenge the establishment. They are independent thinkers who seek to set their own agenda and chart their own course. They possess great integrity, assured of who they are and rejecting any of society's labels or constraints. Mavericks are comfortable taking outsized risks to move to the front of the pack. They may find themselves torn between their need to achieve publicly laudable deeds and their individualistic desires to reject expectations and conventions and instead act as they will.",
            ("Blue", "Yellow"): "Visionary: Visionaries are driven by growth, being frontrunners, and by a need to innovate. They possess foresight, imagination, and the ambition to bring their insights to life. As natural leaders, they are comfortable with uncertainty and the risk of failure, and are willing to bet it all to pursue the future of their dreams. Strategic and assertive, once they’ve set their sights on something, others can count on Visionaries to lead them to a better tomorrow.",
            ("Blue", "Beige"): "Achiever: Blue Achievers can be found at the front of any effort heading toward victory. While most might buckle under the pressure to succeed and the heaviness of their accolades, Blue Achievers actually thrive under this weight, inviting all eyes and expectations to turn to them for the best results. With much of their sense of self-worth tied to the value others see in their accomplishments, they welcome the responsibility for their team’s well-being, outcomes, and reputation. Blue Achievers are confident, self-assured, visionary, and thrive on the status that comes from conquering adversaries and accomplishing new feats. They are some of the most admirable icons in human history, influencing powerful movements and advancing societal growth. Every collection of people and personalities needs Blue Achievers, as their need to advance, accomplish, and demonstrate their adeptness proves vital in inspiring others to rise to even the most immense undertakings.",
            ("Maroon", "Blue"): "Contender: Contenders are driven to overcome challenges and by growth and being frontrunners. They demonstrate natural ability and grit, persist in the face of difficulties, and relish any chance to engage in contests or rivalry even against their own historical best. Contenders are singularly focused and determined to reach success in every endeavor as they strive to work harder, be better, run faster, and last longer.",
            ("Maroon", "Green"): "Pioneer: Pioneers are driven to overcome challenges and by the quest for the unknown. They are comfortable embarking into wild and uncharted regions, unphased and even excited by unforeseen obstacles. They are at ease within the wilderness and seek the rush and exhilaration of pushing past limitations. Pioneers invite and inspire others to explore with them, with the goal of uncovering new pathways and ultimately bringing deeper meaning to life.",
            ("Maroon", "Orange"): "Maker: Makers are driven to overcome challenges and by self-expression and artistry. They are hands-on in their ideas, taking what is abstract and creating something tangible. Determined, hardworking, and original, Makers take what some consider to be a daunting creative process and embrace it with dedication and vigor. They are appreciated for their hard work, original interpretations, and relentless pursuit of achievement. Makers are always willing to put in the energy and effort required, as long as the final creation is meaningful and satisfying.",
            ("Maroon", "Pink"): "Precisionist: Precisionists are driven to overcome challenges and by experience, elegance, and beauty in all forms. They are uncompromising and disciplined in their endless pursuit of order, accuracy, and perfection. Relentless and practical, their work ethic surpasses that of many others. Precisionists bring time-tested, methodical, and logical approaches to their endeavors, uniting excellence and order with the messiness of grit and grind.",
            ("Maroon", "Purple"): "Protector: Protectors are driven to overcome challenges and by a compassionate need to care for others. They are staunch advocates of justice and find purpose in defending and shielding others from injury, oppression, or harm. They will go to lengths to champion the greater common good, even if it means standing alone. Rather than commit themselves to a single cause or ideal, they lend support and aid to anyone whose plight could be improved.",
            ("Maroon", "Red"): "Energizer: Energizers are driven to overcome challenges and by a desire to entertain and cause others to get excited. Their endless resolve and abundant enthusiasm naturally invigorates others to get involved. Energizers have the charisma and courage to enter life’s circumstances and move both people and events to a desired action or outcome. It is not the end result that satisfies them as much as the opportunity for lively participation and dedicated work during all steps of their journey.",
            ("Maroon", "Silver"): "Dark Horse: Dark Horses are driven to overcome challenges and by a desire to disrupt the norm and challenge the establishment. They have a healthy disdain for age-old cultural systems and standards, preferring instead to live at the edge of society and its expectations and ideas of success. Dark Horses are loath to tolerate defeat and make it their mission to prove others wrong. Often misjudged or underestimated, these rebellious overcomers surprise those quick to dismiss by achieving victory in the end.",
            ("Maroon", "Yellow"): "Challenger: Challengers are driven to overcome obstacles and by a need to invent the future through innovation. They boldly and defiantly reframe potential hurdles as opportunities for personal and societal growth. Dedicated agents of change, Challengers contend that true transformation is possible only through taking continual bold steps forward, however difficult the obstacles or incredible the sacrifice along the way. For Challengers, great progress comes from great effort. Committing their all to a better and brighter future, they motivate individuals, and even systems, to change before their very eyes.",
            ("Maroon", "Beige"): "Competitor: Maroon Competitors are the consummate engines that work hard and persevere to achieve. Defined by their intense determination, resilience against obstacles, and an attitude that just won’t quit, Maroon Competitors are some of the most desirable members of any group pursuing a difficult goal. They are persistent in their drive and seemingly unrelenting in their pace, and will work until victory is realized.",
            ("Green", "Blue"): "Trailblazer: Trailblazers are driven by the quest for the unknown and by growth and being frontrunners. They are explorers at heart as they courageously break new ground to pursue the promise of what might be. They balance their inclination to be introspective and inquisitive with an enterprising spirit and willingness to take charge. They are as theoretical as they are ready for action, and are apt to inspire others to join them on their quest. Exceptional and ambitious scouts, Trailblazers are the first to lead brazen new initiatives all the way from idea to reveal.",
            ("Green", "Maroon"): "Adventurer: Adventurers are driven by the quest for the unknown and by a need to overcome challenges. They feel a rush and exhilaration amid new opportunities and encounters, pushing past any perceived limitations or barriers to uncover what lies ahead. They are determined to demonstrate mastery along every step of their journey and not to leave any path unturned or unconsidered as they pursue new limits and discoveries. Adventurers are reflective of themselves and the world around them, and see every experience as an opportunity to grow in patience, find truth, gain perspective, and press on.",
            ("Green", "Orange"): "Seeker: Seekers are driven by the quest for the unknown and by self-expression through artistry. They chase after wisdom, answers, and truth, and meander down many paths to find it. As continual learners, Seekers probe into life’s mysteries, asking questions few think to ask, thereby yielding novel perspectives and fascinating insights. They find the study of people intriguing and enjoy learning just why they act and think as they do.",
            ("Green", "Pink"): "Detective: Detectives are driven by the quest for the unknown and by experience, elegance, and beauty in all forms. Natural investigators, they subject themselves, their surroundings, and their peers to the highest scrutiny. Aware of even the subtlest of clues, Detectives find and fit together various puzzle pieces to form a beautifully intricate answer or theory. Calculating and precise, they strategize many steps ahead to ensure that knowledge, truth, and order are served.",
            ("Green", "Purple"): "Ambassador: Ambassadors are driven by the quest for the unknown and by a need to compassionately care for others. People entrust their personal stories and information to Ambassadors, believing they will both guard and represent them well. Their equitable appraisal of logic, truth, and the emotions felt by others sets them apart as a voice of reason, able to discern between what is right and wrong or fact and fiction. Ambassadors nurture close relationships and foster community in order to connect people through shared experiences.",
            ("Green", "Red"): "Globetrotter: Globetrotters are driven by the quest for the unknown and a desire to cause others to get excited. They consider the world and its people a treasure trove, replete with exciting experiences and stories, and aspire to learn from each one. Their lively adventures may include the diligent study of foreign cultures, deep and spirited conversations with others, and even wild celebrations in and pilgrimages to new places. Each new experience provides extensive worldly understanding and Globetrotters desire to share this wisdom with others to aid them in their own journeys.",
            ("Green", "Silver"): "Ranger: Rangers are driven by the quest for the unknown and by a desire to challenge the establishment. They are not afraid of controversy as they toe the line between the established and accepted and frontiers not yet known. In so doing, they disrupt the familiar and expose revelations both fresh and unconventional. Indifferent to what others may think, Rangers adopt an outsider's viewpoint and perspective, fearlessly pushing and prodding boundaries to provoke others and foster the most tension.",
            ("Green", "Yellow"): "Researcher: Researchers are driven by the quest for the unknown and by a need to invent the future through innovation. They are devoted to the scholarly practices of inquiry and the examination of complex concepts in order to better understand and transform them. To a Researcher, intelligence and critical study is key to propelling society forward, and to this end, they endeavor to ask brilliant questions in pursuit of more sophisticated solutions. Discontent to rely on intuition alone, they seek knowledge and put forth theories that are intelligent, structured, and beyond reproach.",
            ("Green", "Beige"): "Explorer: Green Explorers are spirited adventurers who are constantly exploring and questioning the world around them. Their insatiable curiosity dives deep into the details in pursuit of enlightenment and understanding. Where a Green Explorer finds themselves at any given moment is typically never their endpoint because they are always searching for something new and not yet known. Green Explorers are society’s trailblazers, satisfied and even propelled by a degree of danger and uncertainty.",
            ("Orange", "Blue"): "Architect: Architects are driven by self-expression and artistry and by growth and being frontrunners. Their intelligent foresight and carefully contrived plans help guide the construction of novel solutions. Architects have a natural ability to imagine creative yet practical approaches to solving the world's complex challenges. They find meaning in building impressive strategies, relationships, and structures that inspire wonder and awe from those who encounter them.",
            ("Orange", "Maroon"): "Artisan: Artisans are driven by self-expression and a need to overcome challenges. They are devoted to their trade or craft and delight in bringing a plan or concept to life. They are pragmatic, tough-minded and decisive, and, at times, may take on too many challenges at once. Artisans are skillful and good problem-solvers, persevering through obstacles to make headway and see a project to completion.",
            ("Orange", "Green"): "Searcher: Searchers are driven by self-expression and artistry and by the quest for the unknown. They believe that only the examined life is worth living as they strive to question everything and make newfound discoveries. Their incessant curiosity and scrutiny means that they think outside the box and bring what is hidden or unexplored to light. Their highest potential is best realized when surrounding themselves with others who accept their creative inquiry and probing personality.",
            ("Orange", "Pink"): "Composer: Composers are driven by self-expression and artistry and by experience, elegance, and beauty in all forms. They approach the act of creation, however messy, with refinement and poise. They are often torn between a desire for both freedom of voice and order and organization. With the right guide rails, they succeed in finding both, expressing their artistic and original abilities within set modes and guidelines. In working with others, Composers value their outside leadership and guidance but still want some degree of self-governance.",
            ("Orange", "Purple"): "Curator: Curators are driven to express themselves through artistry and by a need to compassionately care for others. They seek novel and creative ways of doing things, whether in their artistic endeavors or through service to those around them. Curators play to their passions, doing and creating things that speak to others in deep and distinctive ways. Their work reflects a keen understanding of what’s good for humanity and inspires others to reflect and respond in meaningful ways.",
            ("Orange", "Red"): "Storyteller: Storytellers are driven by self-expression and artistry and by a desire to cause others to get excited. They bring audiences together to share warmly exaggerated, punchy narratives. Natural wordsmiths, Storytellers bend perspectives, twist conclusions, and creatively interpret events and characters. Playful and clever with words, they shock and amuse for the purpose of making unexpected connections, hinting at shared history, and revealing a fuller, richer meaning.",
            ("Orange", "Silver"): "Nonconformist: Nonconformists are driven by self-expression and artistry and by a desire to challenge the establishment. Their need to radically speak their truth sets them apart as offbeat and original among their contemporaries. They take time to listen to the opinions of others, seeking to understand their more conventional perspective in order to bolster their contrary ones. With their views now battle-tested, Nonconformists are not afraid to challenge society’s entrenched positions and implore others to reconsider, or even reset, beliefs.",
            ("Orange", "Yellow"): "Ideator: Ideators are driven by self-expression and artistry and by a need to innovate. They long to imagine and conceive of ingenious ideas and to share these ideas with anyone who may listen. Ideators work out the details and intricacies of each new concept and envision the breadth of possibilities that can come from it. Their ultimate goal is to rouse their contemporaries to join them on a noble mission to collectively and creatively convert the ordinary into the extraordinary.",
            ("Orange", "Beige"): "Creator: Orange Creators make up the world’s creative class because they are so imaginative, self-expressive, and intensely original. They are motivated by bringing new ideas and concepts to life in ways that move and inspire. A large proportion of Orange Creators can be found broadly in the arts, entertainment, and the sciences. They are attracted to fields like music, design, and animation, within a broad range of skilled crafts, as well as in highly technical fields like engineering and architecture. Iconic Orange Creators have shaped global culture with their innate ability to translate mood, emotion, and story into something tangible for all of humanity to experience. Conversely, Orange Creators can be isolated, misunderstood, or hard to reach due to their perceived whimsy and originality.",
            ("Pink", "Blue"): "Connoisseur: Connoisseurs are driven by experience, elegance, and beauty in all forms, and by growth and being frontrunners. They have a sophisticated and discerning palate, and can pass judgement on the qualities of a thing with great expertise. Their extensive knowledge combined with their exquisite taste allow them to take in the whole picture while also perceiving every detail. Connoisseurs are self-aware and are quick to recognize their place and purpose in society. Their perceptions and judgements preserve ideals, continue established traditions, and serve to build a lasting legacy for future generations.",
            ("Pink", "Maroon"): "Perfectionist: Perfectionists are driven by experience, elegance, and beauty in all forms and by a need to overcome challenges. Their exacting standards for excellence push them to chase what is ideal, labeling anything short of perfection as unacceptable. Perfectionists perform with the highest of potential, devoting themselves to their craft and the mastery of every task entrusted to them. They firmly believe that their uncompromising dedication to the ideal will drive them to greatness and victory.",
            ("Pink", "Green"): "Philosopher: Philosophers are driven by experience, elegance, and beauty in all forms and by the quest for the unknown. They are abstract thinkers who seek wisdom and enlightenment through a study of knowledge, truth, and life’s meaning. Methodical and systematic in both thought and action, they bring a refined approach and perspective to the contemplation of complex questions and their answers. Philosophers are measured and meditative in their grasp of big-pictures issues, believing enlightenment can be reached through understanding the fundamental laws of nature.",
            ("Pink", "Orange"): "Virtuoso: Virtuosos are driven by experience, elegance, and beauty in all forms and by self-expression and artistry. Their dazzling skill holds others spellbound as they perform with dignity and grace. Able to tap into timeless pools of classic knowledge, Virtuosos astonish audiences with their ability to broaden minds and unleash creative potential. While they are naturally gifted, Virtuosos meticulously practice and refine their art until it is poised, polished, and ready for performance.",
            ("Pink", "Purple"): "Idealist: Idealists are driven by experience, elegance, and beauty in all forms and by a need to compassionately care for others. They hold fast to a vision of a world that provides the most benefit for all, regardless of practicalities. While Idealists value harmony and stability in their work and life, they will welcome and nurture change if it supports a worthy cause. They believe in the inherent good of humanity and trust that through everyone’s positive contributions, society will progress and all will be well.",
            ("Pink", "Red"): "Aficionado: Aficionados are driven by experience, elegance, and beauty in all forms, and by a desire to cause others to get excited. They pursue their passions and interests with great devotion and enthusiasm. They meticulously commit themselves to their pursuits, not for status or mastery, but because they find them compelling in all their dynamism. Activities are neither a hobby or pastime, but a passionate calling to be cherished for a lifetime.",
            ("Pink", "Silver"): "Refiner: Refiners are driven by experience, elegance, and beauty in all forms and by a desire to challenge the establishment. They approach all pursuits intending to purify and restore what society has degraded, and look to no one for permission to do so. Seeking purity and excellence, they strive to improve all they can, even those things others already perceive as perfect. Refiners approach their work with high ideals and expectations, urging others to also desire what can be, rather than what currently is.",
            ("Pink", "Yellow"): "Trendsetter: Trendsetters are driven by experience, elegance, and beauty in all forms and by a need to invent the futurenovate. They dream up novel ideas and make them popular among the masses. They are very intuitive and can perceive what is missing in society, and then set to the task of creating it. Trendsetters are able to envision and conceive clear ideas of what is best, and they introduce new styles and set trends that have far-reaching effect.",
            ("Pink", "Beige"): "Sophisticate: Pink Sophisticates are a group’s connoisseurs with a refined palate and penchant for all that is excellent. They are experiential and at times even ethereal in their pursuit of beauty in all of its forms. Pink Sophisticates are not for everybody, and this is probably because not just anybody can fit the bill. The Pink Sophisticate’s drive for excellence, refinement, and elegance often leads them to the top of the pack in their respective endeavors. They value self-expression, intentionality, and fine detail, and are often looked to as the standard holders. Society’s Pink Sophisticates often find themselves contributing to luxury brands and companies like Bentley, Versace, and the like.",
            ("Purple", "Blue"): "Guide: Guides are driven by a need to compassionately care for others and by growth and being frontrunners. They are a motivating force whose influence and good standing cause others to look to them for direction at life’s many junctions. Guides draw meaningful satisfaction from steering others toward well-being, fulfillment, and positive change. They are confident, optimistic, helpful, and generous in their provision of care and counsel.",
            ("Purple", "Maroon"): "Guardian: Guardians are driven by a need to compassionately care for others and by a resolve to overcome challenges. They believe that everyone matters equally and that one’s value isn’t determined by their identity, status, or background. Guardians protect, preserve, and care for others and their values, even if it’s at the cost of their own safety or wellbeing. Kind, patient, and empathetic, they inspire others to rise to defend those not yet capable of advocating for themselves.",
            ("Purple", "Green"): "Shepherd: Shepherds are driven by a need to compassionately care for others and by the quest for the unknown. They guide, guard, and watch over others, seeking to steer them to the clearest path toward what is most good. A Shepherd’s worldly knowledge combined with their strong need to help others make them a reliable leader, trusted for their strategic direction. Able to identify common ground and offer wise answers, Shepherds inspire confidence in others as to the paths worth taking.",
            ("Purple", "Orange"): "Patron: Patrons are driven by a need to compassionately care for others and by expressing themselves through artistry. They empower others to bring their creative dreams to life, committing their own resources and influence to that end. They lend their patronship to imaginative ideas and revolutionary causes, actively supporting the people and projects behind them. Patrons believe in the collective abilities of their communities and encourage their original avenues of expression so that together they can realize their grandest potential.",
            ("Purple", "Pink"): "Confidant: Confidants are driven by a need to compassionately care for others and by experience, elegance, and beauty in all its forms. They are the first that others turn to with their most private secrets and aspirations. The depth of their sensitivity and capacity for empathy causes others to trust Confidants fully as a source of comfort and support. Never one to judge, they allow others to voice their emotions and concerns, thereby easing their burdens and distress.",
            ("Purple", "Red"): "Host: Hosts are driven by a need to compassionately care for others and by a desire to cause others to get excited. They exemplify hospitality in their actions and live for the opportunity to receive and entertain guests. Hosts bring people together to foster much-needed bliss and unity. Their simple acts of giving and receiving go a long way to provide others with a sense of comfort and belonging. On the surface, they may seem lighthearted or quick to make a joke, but by ensuring everyone else's needs are met, they show how deeply they care.",
            ("Purple", "Silver"): "Advocate: Advocates are driven by a need to compassionately care for others and by a desire to challenge the establishment. They selflessly support and promote the interests or causes of groups, over and above their own interests. They seek to represent the unvoiced, oppressed, and those who simply need a hand, persuading others to wake up from their complacency and join them in making a radical change. Though valuing their independence, Advocates are willing to fight for what’s right and will enter the fray in order to spark social change.",
            ("Purple", "Yellow"): "Advisor: Advisors are driven by a need to compassionately care for others and by a need to invent the future through innovation. People tend to flock to Advisors for their acute ability to foresee what’s on the horizon and imagine the ramification of any action, seeking their guidance and next-step recommendations. They have an acute understanding of relationship dynamics and how people respond to change, making them wise and intuitive counselors able to heal and bring transformation.",
            ("Purple", "Beige"): "Provider: A world without Purple Providers is one no one would want to endure. Purple Providers are selfless, compassionate, and naturally put the needs of others first, often over their own. They are invaluable to any group or ecosystem for the goodness they bring and for the care they hope to provide. Their genuine concern for others, and the trust that concern cultivates, attracts an immense network of friends and followers.Purple Providers have risen to serve as some of this world’s most effective leaders and guides, and their compassionate empowerment of others has led to the coining of the axiom servant leader.",
            ("Red", "Blue"): "Motivator: Motivators are driven to entertain and excite others and by growth and being frontrunners. They possess compelling charisma and charm that mobilize others toward a great cause or just a great time. Motivators are strongly perceptive and able to read others’ energy levels. They lend their powerful yet positive influence to help others find balance in life and progress toward their goals.",
            ("Red", "Maroon"): "Dynamo: Dynamos are driven to cause others to get excited and by a need to overcome challenges. They are forceful and energetic individuals who are not shy in making their presence felt. Whether on the sidelines or in the fray, their presence and energy is palpable. Dynamos are friendly, generous with their attention, and confident in their own and their peer’s abilities. As natural leaders, Dynamos lend their impressive willpower to others so that all might overcome their personal obstacles. They are quick to enter a competition or contest, confident in their ability to win.",
            ("Red", "Green"): "Thrill-seeker: Thrill-seekers are driven to cause others to get excited and by the quest for the unknown. They purposefully seek out and enjoy risk-laden activities and adventures. They feel most alive when truly present within any intense experience, as adrenaline courses through their veins. These real-world experiences not only satisfy Thrill-seekers’ cravings for constant excitement, but inspire deep reflection and perspective that is hard to come by any other way.",
            ("Red", "Orange"): "Performer: Performers are driven to cause others to get excited and by self-expression and artistry. They are most engaged when in front of an audience. As self-proclaimed stars, they carry out a playful rendition of life full of color and energy. With a robust imagination, Performers see the promise and possibility for fun in everything and delight others with their original stories, reenactments, and improvisation. They dedicate much energy to honing their craft, reworking their productions for maximal effect and impact.",
            ("Red", "Pink"): "Enthusiast: Enthusiasts are driven to cause others to get excited and by experience, elegance, and beauty in all forms. They are ardent supporters of people and causes and enthusiastically devote themselves to the pursuits they believe in. They radiate joy, laugh freely, and bring a zest for life to everything they do. Enthusiasts are sensitive to any uncomfortable or unwelcome tension in a room and deploy humor as a happy distractant. They use their charisma and dynamic energy to uplift others out of tough moments and to muster them toward a greater purpose.",
            ("Red", "Purple"): "Emcee Emcees are driven to entertain and excite others and by a compassionate need to care for others. They draw energy and inspiration from the people around them. They possess a natural ability to read a room and the people within it, and use that insight to perform in ways that leave others feeling moved and uplifted. While Emcees are skilled at capturing the attention of others, they are not protective of the stage but invite others to join them in the spotlight.",
            ("Red", "Silver"): "DareDevil: Daredevils are driven to cause others to get excited and by a desire to challenge the establishment. They are reckless, bold, and pursue activities that demonstrate their daring bravado. Known for their spirited antics, Daredevils take on the greatest risks without regard for the safety of themselves or others. Hurling themselves at the boundary between right and wrong is not just thrill-seeking behavior, but their way to confront long-held traditions and challenge the conventions of the day.",
            ("Red", "Yellow"): "Magician: Magicians are driven to entertain and cause others to get excited and by a need to innovate. They make incredible things happen, tapping into boundless potential to bring to light what others thought was impossible. Their insight into what is possible infuses them with the enthusiasm and comfort to pursue and enact change. A Magician’s flair for showmanship leads them to playfully dramatize the extraordinary act of transformation.",
            ("Red", "Beige"): "Entertainer: performances and stories, and may be the single most in-demand and attractive Archetype in the room; as evidenced by the increasing success of America’s entertainment market. Red Entertainers elevate the daily mundane to something more vibrant, more sensational, and simply more fun. They generate excitement and enjoyment — encouraging laughter, playfulness, and general optimism. Sometimes their whimsy and volume can run its course in a group setting, but there’s no doubt that Red Entertainers deliver much-needed vibrancy and color.",
            ("Silver", "Blue"): "Ringleader: Ringleaders are driven to challenge the establishment and by growth and being frontrunners. They are natural activators and inspire others to rally in support of unconventional ideas. They are confident, courageous, and assertive when in command, using position and status to provoke audiences to carry out radical change. Ringleaders are known for their enthralling demonstrations of mastery and power, always insisting on taking center stage.",
            ("Silver", "Maroon"): "Instigator: Instigators are driven to disrupt the norm and by a need to overcome challenges. They cause others to question even their most sacred beliefs and convictions by stirring up latent feelings of discontent with \"the establishment.\" Relentless and tenacious, they goad, provoke, and urge others until a point is reached where all are ready to take action. The end goal of their aggressive agitation is not anarchy, but a restructuring of convention and wisdom.",
            ("Silver", "Green"): "Rogue: Rogues are driven to challenge the establishment and by the quest for the unknown. They get lost in their own thoughts as they probe ideas and opinions forming humanity’s wild frontier. Comfortable with chaos, they are quick to question the status quo and purposefully push the envelope. Rogues enjoy challenging the ideas and beliefs of others, but always to enliven discourse, dive deeper into truth, and maybe someday find it.",
            ("Silver", "Orange"): "Renegade: Renegades are driven to challenge the establishment and by self-expression and artistry. They reject lawful and conventional behavior and seek opportunities to showcase their own unique way of doing things. A Renegade’s non-conformist attitude means they create and express themselves in the most revolutionary of ways. Their wild and messy creative impulses often lead them down a path of solo artistry that is free of rules, propriety, or boundary.",
            ("Silver", "Pink"): "Individualist: Individualists are driven to challenge the establishment and by experience, elegance, and beauty in all forms. They are quite comfortable pursuing independent courses of thought or activity, even to the point of detaching from the people around them. With lofty dreams of tomorrow, Individualists reconsider society’s conventions and seek for higher principles beyond prescribed limits or established bounds. After considerable review, Individualists advocate for timeless and sublime ideals that the world may have forgotten or foolishly rejected.",
            ("Silver", "Purple"): "Activist: Activists are driven to challenge the establishment and by a need to compassionately care for others. They support bold and brazen action around controversial issues, either through radical support and devotion or organizing staunch opposition. They seek to free anyone who is oppressed or held back by a broken system, and charge boldly into conflict to make that happen. Activists empower people to stand alongside them and advocate for causes that may be unpopular, obscure, or systemic within society.",
            ("Silver", "Red"): "Rock Star: Rock Stars are driven to challenge the establishment and by a desire to entertain. Due to their commanding presence, star reputation, and alluring personality, many admire Rock Stars and covet their attention and devotion. With mountains of energy and boundless enthusiasm, Rock Stars chase what fascinates them, treating the world as their wild and crazy playground. Around each corner they glimpse tantalizing and boundless opportunities for adventure.",
            ("Silver", "Yellow"): "Free-thinker: Free-thinkers are driven to challenge the establishment and by a need to innovate. Happily at home within their own thoughts, they are prone to speculate and form their own opinions, regardless of the facts or authority of others. Free-thinkers value autonomy above all and believe that everyone should slash any constraints that bind imagination. Living into this value, Free-thinkers arrive at powerful and unexpected connections with the potential to shift the status quo in big ways.",
            ("Silver", "Beige"): "Rebel: Without a doubt the most polarizing Archetype of them all, Silver Rebels are rule-breakers, system fighters, activists, and daredevils who refuse to conform to any norm. They are relatively rare within group settings, preferring the freedom that comes with independence—which may be good since many people claim they can’t relate at all to this Archetype. Despite that, Silver Rebels have proven to be one of the most intriguing, inspiring, and attractive Archetypes throughout history, and are a much-needed force in today’s era. They have an ability to effortlessly draw followings, even to seemingly unconventional or controversial ideas and causes. The founders of America were, in fact, pure revolutionaries who fought for an entirely new way of life. Many marvel at the free and fearless pirate, the leathered motorcyclist, the cool and defiant celebrity, these incarnations of an Archetype so many—perhaps secretly—wish they could be bold enough to embody.",
            ("Yellow", "Blue"): "Vanguard: Vanguards are driven to invent the future through innovation and by growth and being frontrunners. Always at the forefront of new concepts, ideas, and strategies, they set a benchmark that they believe others should aspire to. Known for great imagination, insight, and boldness, Vanguards are skilled at navigating and distilling complex and dynamic social and political systems. They form intelligent strategies and put them into practice to propel transformation and set the standards of tomorrow.",
            ("Yellow", "Maroon"): "Inventor: Inventors are driven to innovate and by a need to overcome challenges. They tirelessly toil to devise the new and novel. They take an ingenious approach to their work and conduct exhaustive experiments to arrive at their next breakthrough. While others are content to daydream or speculate about the future, Inventors are driven to create it. When challenges arise, they push through them, seeing both the joy and duty in putting in the hard work that developing leading-edge solutions requires.",
            ("Yellow", "Green"): "Theorist: Theorists are driven to invent the future through innovation and by the quest for the unknown. They form astonishing opinions and theories within their own mind but do not always go so far as to test them against reality. Intellectual, systematic, and logical in their thinking, they possess a natural ability to connect the dots. Their aspiration is to understand everything, but in their journey to do so, they may learn the value of intuition and embrace that which cannot be fully explained or known.",
            ("Yellow", "Orange"): "Originator: Originators are driven to innovation, self-expression, and artistry. Their imaginative and creative tendencies lead them to inventive ideas and undertakings. Spontaneous, passion-driven, and full of inspiration, Originators perform best in unstructured situations. It is within the chaotic act of creation that they truly come alive and find the space to try out their original ideas.",
            ("Yellow", "Pink"): "Dreamer: Dreamers are driven to innovate and by experience, elegance, and beauty in all forms. With heads often in the clouds, they are quite content to muse over ideals. Believing that anything is possible, they intuit and imagine new ways to refine or perfect the world. Dreamers’ primary aspirations are to share their visions for a better world, and then inspire others to build it.",
            ("Yellow", "Purple"): "Oracle: Oracles are driven to innovate and by a need to compassionately care for others. Oracles have been gifted with the rare gift of foresight, perceiving opportunities and conceiving of ideas that help improve the world around them. They voice their ideas to all who are willing to listen and are apt to rally support for a cause. They have a knack for forecasting the future and the effect that any given action might have on humanity. Oracles are deeply empathetic and sensitive and take great care to share their gifts in ways that meaningfully shape society.",
            ("Yellow", "Red"): "Futurist: Futurists are driven to invent the future and by a desire to cause others to get excited. Their zest and zeal for life is strongest when thinking about the future and all the possibilities it contains. Their view of tomorrow is optimistic, full of promise and boundless in joy. Futurists adopt a rosy outlook that overlooks any potential downsides and they come most truly alive when collaborating with others to brainstorm new and exciting ideas.",
            ("Yellow", "Silver"): "Reformer: Reformers are driven to innovate and by a desire to challenge the establishment. They work for and advocate change, even if it flies in the face of established wisdom. While some may interpret their cry for renewal and rebirth as nothing but nostalgia, Reformers possesses the wisdom of hindsight and see potential where others have become complacent. While they are prone to see the world as full of flaws, they are uniquely able to rouse and guide humanity back to its essential self.",
            ("Yellow", "Beige"): "Innovator: Yellow Innovators are an instrumental—and sometimes rare—asset to any group, society, or culture. These are the individuals that need to invent, transform, and continuously develop new products, services, and processes. They are constant sources of ideas, visions, and opportunities for advancement and progress. Yellow Innovators can be high-risk individuals who recognize that true innovation means stepping into the experimental unknown, even if it means moments of failure. They dabble in theories and are comfortable working in the gray, in search of brilliant and transformational solutions. Incessant ingenuity and a thirst for reaching into the unseen is a hallmark of this Archetype. Without them, global civilization might still be stuck in the Stone Age. It was Yellow Innovators who invented the wheel that gave humanity early mobility, and the aircraft that gave humanity flight. When you need to make tomorrow come into being today and when you need to create what others are not, turn to Yellow Innovators.",
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
                                cols[j].image(image, use_container_width=True)

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
                            st.image(image, use_container_width=True)
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
                            st.image(image, use_container_width=True)
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
                                cols_q9[i % 3].image(image, use_container_width=True)

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
