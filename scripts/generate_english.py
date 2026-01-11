#!/usr/bin/env python3
"""
English Comprehension & Grammar Question Generator for 11+ Tutor

Uses public domain passages (Aesop's Fables, classic literature) for comprehension.
Generates grammar, spelling, and punctuation questions.
"""

import sqlite3
import json
import random
import uuid
from typing import List, Dict

# =============================================================================
# Public Domain Passages (Aesop's Fables - perfect for 11+ age group)
# =============================================================================

COMPREHENSION_PASSAGES = [
    {
        "title": "The Hare and the Tortoise",
        "text": """A Hare was making fun of the Tortoise one day for being so slow. "Do you ever get anywhere?" he asked with a mocking laugh.

"Yes," replied the Tortoise, "and I get there sooner than you think. I'll run you a race and prove it."

The Hare was much amused at the idea of running a race with the Tortoise, but for the fun of the thing he agreed. So the Fox, who had consented to act as judge, marked the distance and started the runners off.

The Hare was soon far out of sight, and to make the Tortoise feel very deeply how ridiculous it was for him to try a race with a Hare, he lay down beside the course to take a nap until the Tortoise should catch up.

The Tortoise meanwhile kept going slowly but steadily, and, after a time, passed the place where the Hare was sleeping. But the Hare slept on very peacefully; and when at last he did wake up, the Tortoise was near the goal. The Hare now ran his swiftest, but he could not overtake the Tortoise in time.""",
        "moral": "Slow and steady wins the race.",
        "questions": [
            {"q": "Why did the Hare make fun of the Tortoise?", "a": "Because the Tortoise was slow", "wrong": ["Because the Tortoise was small", "Because the Tortoise was green", "Because the Tortoise couldn't swim"]},
            {"q": "Who acted as the judge for the race?", "a": "The Fox", "wrong": ["The Owl", "The Bear", "The Rabbit"]},
            {"q": "What did the Hare do during the race?", "a": "He took a nap", "wrong": ["He stopped to eat", "He got lost", "He helped the Tortoise"]},
            {"q": "What is the moral of this story?", "a": "Slow and steady wins the race", "wrong": ["The fastest always wins", "Never trust a fox", "Hares are faster than tortoises"]},
            {"q": "How did the Tortoise win the race?", "a": "By keeping going slowly but steadily", "wrong": ["By cheating", "By taking a shortcut", "By running very fast"]},
        ]
    },
    {
        "title": "The Lion and the Mouse",
        "text": """A Lion lay asleep in the forest, his great head resting on his paws. A timid little Mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the Lion's nose.

Roused from his nap, the Lion laid his huge paw angrily on the tiny creature to kill her.

"Spare me!" begged the poor Mouse. "Please let me go and some day I will surely repay you."

The Lion was much amused to think that a Mouse could ever help him. But he was generous and finally let the Mouse go.

Some days later, while stalking his prey in the forest, the Lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring.

The Mouse knew the voice and quickly found the Lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the Lion was free.

"You laughed when I said I would repay you," said the Mouse. "Now you see that even a Mouse can help a Lion." """,
        "moral": "A kindness is never wasted.",
        "questions": [
            {"q": "What woke the Lion from his sleep?", "a": "The Mouse running across his nose", "wrong": ["A loud noise", "The hunter", "Another lion"]},
            {"q": "Why did the Lion let the Mouse go?", "a": "He was generous", "wrong": ["He was scared", "The Mouse was too small to eat", "He was too tired"]},
            {"q": "How did the Lion get trapped?", "a": "In a hunter's net", "wrong": ["In a hole", "In a cage", "In a river"]},
            {"q": "How did the Mouse help the Lion?", "a": "By gnawing through the rope", "wrong": ["By calling for help", "By fighting the hunter", "By finding a key"]},
            {"q": "What does this story teach us?", "a": "A kindness is never wasted", "wrong": ["Lions are dangerous", "Mice are very clever", "Never trust a mouse"]},
        ]
    },
    {
        "title": "The Fox and the Grapes",
        "text": """One hot summer's day a Fox was strolling through an orchard till he came to a bunch of Grapes just ripening on a vine which had been trained over a lofty branch.

"Just the thing to quench my thirst," said he.

Drawing back a few paces, he took a run and a jump, and just missed the bunch. Turning round again with a One, Two, Three, he jumped up, but with no greater success.

Again and again he tried after the tempting morsel, but at last had to give it up, and walked away with his nose in the air, saying: "I am sure they are sour."

It is easy to despise what you cannot get.""",
        "moral": "It is easy to despise what you cannot get.",
        "questions": [
            {"q": "What did the Fox want?", "a": "The grapes", "wrong": ["The apples", "Some water", "The vine"]},
            {"q": "Why couldn't the Fox reach the grapes?", "a": "They were too high", "wrong": ["They were too far away", "There was a fence", "They were guarded"]},
            {"q": "How many times did the Fox try to get the grapes?", "a": "Many times", "wrong": ["Once", "Twice", "Never"]},
            {"q": "What did the Fox say about the grapes when he gave up?", "a": "They are sour", "wrong": ["They are sweet", "They are poisonous", "They are not ripe"]},
            {"q": "What does this story teach us?", "a": "People often pretend to dislike what they cannot have", "wrong": ["Foxes don't like grapes", "Grapes grow very high", "Always keep trying"]},
        ]
    },
    {
        "title": "The Boy Who Cried Wolf",
        "text": """There was once a young Shepherd Boy who tended his sheep at the foot of a mountain near a dark forest. It was rather lonely for him all day, so he thought upon a plan by which he could get a little company and some excitement.

He rushed down towards the village calling out "Wolf, Wolf," and the villagers came out to meet him, and some of them stopped with him for a considerable time.

This pleased the boy so much that a few days afterwards he tried the same trick, and again the villagers came to his help.

But shortly after this a Wolf actually did come out from the forest, and began to worry the sheep, and the boy of course cried out "Wolf, Wolf," still louder than before.

But this time the villagers, who had been fooled twice before, thought the boy was again deceiving them, and nobody stirred to come to his help.

So the Wolf made a good meal off the boy's flock, and when the boy complained, the wise man of the village said: "A liar will not be believed, even when he speaks the truth." """,
        "moral": "A liar will not be believed, even when he speaks the truth.",
        "questions": [
            {"q": "What was the boy's job?", "a": "He was a shepherd", "wrong": ["He was a farmer", "He was a hunter", "He was a woodcutter"]},
            {"q": "Why did the boy cry 'Wolf'?", "a": "He was lonely and wanted company", "wrong": ["He saw a wolf", "He was scared", "He was testing the villagers"]},
            {"q": "What happened when the wolf really came?", "a": "Nobody came to help", "wrong": ["Everyone came running", "The boy ran away", "The sheep fought the wolf"]},
            {"q": "What happened to the sheep?", "a": "The wolf ate them", "wrong": ["They ran away", "The villagers saved them", "The boy protected them"]},
            {"q": "What is the moral of this story?", "a": "Liars will not be believed even when telling the truth", "wrong": ["Wolves are dangerous", "Always listen to children", "Sheep need protection"]},
        ]
    },
    {
        "title": "The Ant and the Grasshopper",
        "text": """In a field one summer's day a Grasshopper was hopping about, chirping and singing to its heart's content. An Ant passed by, bearing along with great toil an ear of corn he was taking to the nest.

"Why not come and chat with me," said the Grasshopper, "instead of toiling and moiling in that way?"

"I am helping to lay up food for the winter," said the Ant, "and recommend you to do the same."

"Why bother about winter?" said the Grasshopper; "we have got plenty of food at present."

But the Ant went on its way and continued its toil.

When the winter came the Grasshopper had no food, and found itself dying of hunger, while it saw the ants distributing every day corn and grain from the stores they had collected in the summer.

Then the Grasshopper knew: It is best to prepare for the days of necessity.""",
        "moral": "It is best to prepare for the days of necessity.",
        "questions": [
            {"q": "What was the Grasshopper doing in summer?", "a": "Singing and hopping about", "wrong": ["Collecting food", "Sleeping", "Building a house"]},
            {"q": "What was the Ant doing?", "a": "Collecting food for winter", "wrong": ["Playing with the Grasshopper", "Looking for water", "Building a bridge"]},
            {"q": "What did the Grasshopper think about winter?", "a": "He didn't worry about it", "wrong": ["He was preparing for it", "He was scared of it", "He thought it would be warm"]},
            {"q": "What happened to the Grasshopper in winter?", "a": "He had no food and was hungry", "wrong": ["He had plenty of food", "He moved to another field", "He stayed with the Ant"]},
            {"q": "What does this story teach us?", "a": "It is wise to prepare for the future", "wrong": ["Summer is the best season", "Ants are better than grasshoppers", "Singing is a waste of time"]},
        ]
    },
    {
        "title": "The Crow and the Pitcher",
        "text": """A Crow, half-dead with thirst, came upon a Pitcher which had once been full of water; but when the Crow put its beak into the mouth of the Pitcher he found that only very little water was left in it, and that he could not reach far enough down to get at it.

He tried, and he tried, but at last had to give up in despair.

Then a thought came to him, and he took a pebble and dropped it into the Pitcher. Then he took another pebble and dropped it into the Pitcher. Then he took another pebble and dropped that into the Pitcher.

At last, at last, he saw the water mount up near him, and after casting in a few more pebbles he was able to quench his thirst and save his life.""",
        "moral": "Little by little does the trick.",
        "questions": [
            {"q": "What was the Crow's problem?", "a": "He couldn't reach the water", "wrong": ["The water was dirty", "The pitcher was broken", "There was no water"]},
            {"q": "What did the Crow drop into the pitcher?", "a": "Pebbles", "wrong": ["Sticks", "Leaves", "Sand"]},
            {"q": "Why did dropping pebbles help?", "a": "It made the water level rise", "wrong": ["It cleaned the water", "It made a hole", "It cooled the water"]},
            {"q": "What is the moral of this story?", "a": "Little by little does the trick", "wrong": ["Crows are clever", "Water is precious", "Never give up hope"]},
            {"q": "How did the Crow feel at the start?", "a": "Half-dead with thirst", "wrong": ["Very happy", "Slightly hungry", "Quite sleepy"]},
        ]
    },
    {
        "title": "The North Wind and the Sun",
        "text": """The North Wind boasted of great strength. The Sun argued that there was great power in gentleness.

"We shall have a contest," said the Sun.

Far below, a man traveled a winding road. He was wearing a warm winter coat.

"As a test of strength," said the Sun, "Let us see which of us can take the coat off that man."

"It will be quite simple for me to force him to remove his coat," bragged the Wind.

The Wind blew so hard, the birds clung to the trees. The world was filled with dust and leaves. But the harder the wind blew down the road, the tighter the shivering man clung to his coat.

Then the Sun came out from behind a cloud. Sun warmed the air and the frosty ground. The man on the road unbuttoned his coat.

The sun grew slowly brighter and brighter.

Soon the man felt so hot, he took off his coat and sat down in a shady spot.""",
        "moral": "Gentleness and kind persuasion win where force and bluster fail.",
        "questions": [
            {"q": "What did the North Wind and Sun argue about?", "a": "Which of them was more powerful", "wrong": ["Who was older", "Who was taller", "Who was faster"]},
            {"q": "What was the contest?", "a": "To make the man remove his coat", "wrong": ["To race across the sky", "To make it rain", "To move the clouds"]},
            {"q": "What happened when the Wind blew hard?", "a": "The man held his coat tighter", "wrong": ["The man took off his coat", "The man ran away", "The man fell down"]},
            {"q": "How did the Sun win?", "a": "By making the man feel hot", "wrong": ["By blinding the man", "By burning the coat", "By calling for help"]},
            {"q": "What does this story teach us?", "a": "Gentleness works better than force", "wrong": ["The sun is stronger than wind", "Coats are important", "Always listen to the sun"]},
        ]
    },
    {
        "title": "The Dog and His Reflection",
        "text": """A Dog had stolen a piece of meat out of a butcher's shop, and was crossing a river on his way home, when he saw his own reflection in the stream below.

Thinking that it was another dog with another piece of meat, he resolved to make himself master of that also. But when he snapped at the reflection, he dropped the meat he was carrying, and it sank to the bottom and was lost.

He tried to get it back, but the current carried it away. He searched and searched, but the meat was gone forever.

The Dog had to go home with nothing.""",
        "moral": "Beware lest you lose the substance by grasping at the shadow.",
        "questions": [
            {"q": "Where did the Dog get the meat?", "a": "From a butcher's shop", "wrong": ["From his owner", "From another dog", "From the river"]},
            {"q": "What did the Dog see in the water?", "a": "His own reflection", "wrong": ["Another dog", "A fish", "A bone"]},
            {"q": "Why did the Dog drop the meat?", "a": "He snapped at his reflection", "wrong": ["He fell in the river", "The meat was too heavy", "Someone took it"]},
            {"q": "What happened to the meat?", "a": "It sank and was lost forever", "wrong": ["Another dog ate it", "It floated away", "The Dog found it later"]},
            {"q": "What does this story teach us?", "a": "Don't be greedy or you'll lose what you have", "wrong": ["Dogs shouldn't swim", "Meat sinks in water", "Rivers are dangerous"]},
        ]
    },
    {
        "title": "The Goose That Laid the Golden Eggs",
        "text": """A Man and his Wife had the good fortune to possess a Goose which laid a Golden Egg every day. Lucky though they were, they soon began to think they were not getting rich fast enough, and imagining the bird must be made of gold inside, they decided to kill it in order to secure the whole store of precious metal at once.

But when they cut it open they found it was just like any other goose.

Thus, they neither got rich all at once, as they had hoped, nor enjoyed any longer the daily addition to their wealth.

Much wanting more, they lost all.""",
        "moral": "Much wanting more, we lose all.",
        "questions": [
            {"q": "What was special about the Goose?", "a": "It laid golden eggs", "wrong": ["It could talk", "It was very large", "It could fly very high"]},
            {"q": "How often did the Goose lay golden eggs?", "a": "Every day", "wrong": ["Once a week", "Once a month", "Once a year"]},
            {"q": "Why did they kill the Goose?", "a": "They thought it was full of gold inside", "wrong": ["They were hungry", "The goose was sick", "They needed feathers"]},
            {"q": "What did they find inside?", "a": "It was like any other goose", "wrong": ["Lots of gold", "Silver coins", "Precious gems"]},
            {"q": "What does this story teach us?", "a": "Greed can cause you to lose everything", "wrong": ["Geese are valuable", "Gold is inside birds", "Always save money"]},
        ]
    },
]

# =============================================================================
# Grammar & Spelling Content
# =============================================================================

SPELLING_WORDS = {
    "correct": [
        ("necessary", "neccesary", "neccessary", "necesary"),
        ("accommodate", "accomodate", "acommodate", "acomodate"),
        ("separate", "seperate", "seperete", "separete"),
        ("occasion", "occassion", "ocasion", "ocassion"),
        ("beginning", "begining", "beggining", "beginnning"),
        ("definitely", "definately", "definitley", "definatly"),
        ("occurrence", "occurence", "occurance", "occurrance"),
        ("embarrass", "embarass", "embaras", "embarras"),
        ("recommend", "recomend", "reccommend", "recommand"),
        ("receive", "recieve", "receeve", "recive"),
        ("believe", "beleive", "belive", "beleeve"),
        ("weird", "wierd", "weerd", "weard"),
        ("achieve", "acheive", "achive", "acheeve"),
        ("height", "hight", "heigth", "heighth"),
        ("rhythm", "rythm", "rhythym", "rithm"),
        ("beautiful", "beautifull", "beutiful", "beautful"),
        ("disappear", "dissappear", "disapear", "dissapear"),
        ("government", "goverment", "governmant", "goverrnment"),
        ("environment", "enviroment", "environmant", "enviornment"),
        ("immediately", "immediatly", "imediately", "immediatley"),
        ("knowledge", "knowlege", "knowledg", "knowladge"),
        ("maintenance", "maintainance", "maintenence", "maintanance"),
        ("occurrence", "occurence", "occurance", "occurrance"),
        ("parliament", "parliment", "parlament", "parlimant"),
        ("professional", "proffessional", "profesional", "proffesional"),
        ("pronunciation", "pronounciation", "prononciation", "pronounsiation"),
        ("questionnaire", "questionaire", "questionair", "questionare"),
        ("restaurant", "restarant", "resturant", "restraunt"),
        ("successful", "successfull", "succesful", "sucessful"),
        ("tomorrow", "tommorow", "tommorrow", "tomorow"),
        ("unfortunately", "unfortunatly", "unfortunatley", "unfortuantely"),
        ("Wednesday", "Wensday", "Wednsday", "Wendesday"),
        ("because", "becuase", "becouse", "beacuse"),
        ("February", "Febuary", "Feburary", "Febrary"),
        ("different", "diffrent", "diferent", "differant"),
        ("library", "libary", "liberry", "libray"),
        ("surprise", "suprise", "surprize", "surprice"),
        ("calendar", "calender", "calandar", "calander"),
        ("argument", "arguement", "arguemnt", "argumetn"),
        ("category", "catagory", "categorie", "catagorie"),
    ],
}

GRAMMAR_QUESTIONS = [
    {"sentence": "The children ___ playing in the garden.", "answer": "are", "wrong": ["is", "be", "am"]},
    {"sentence": "She ___ to the shop yesterday.", "answer": "went", "wrong": ["go", "goes", "going"]},
    {"sentence": "I have ___ my homework.", "answer": "done", "wrong": ["did", "do", "doing"]},
    {"sentence": "The cat sat on ___ mat.", "answer": "the", "wrong": ["a", "an", "some"]},
    {"sentence": "He runs ___ than his brother.", "answer": "faster", "wrong": ["fast", "fastest", "more fast"]},
    {"sentence": "She is the ___ girl in the class.", "answer": "tallest", "wrong": ["taller", "tall", "more tall"]},
    {"sentence": "They ___ been waiting for an hour.", "answer": "have", "wrong": ["has", "had", "having"]},
    {"sentence": "The book ___ on the table.", "answer": "is", "wrong": ["are", "be", "am"]},
    {"sentence": "We ___ to school every day.", "answer": "go", "wrong": ["goes", "going", "went"]},
    {"sentence": "___ you like some tea?", "answer": "Would", "wrong": ["Will", "Do", "Are"]},
    {"sentence": "Neither the teacher ___ the students were late.", "answer": "nor", "wrong": ["or", "and", "but"]},
    {"sentence": "The team ___ playing well today.", "answer": "is", "wrong": ["are", "be", "were"]},
    {"sentence": "I saw ___ elephant at the zoo.", "answer": "an", "wrong": ["a", "the", "some"]},
    {"sentence": "She speaks French very ___.", "answer": "well", "wrong": ["good", "nice", "fine"]},
    {"sentence": "The news ___ very surprising.", "answer": "was", "wrong": ["were", "are", "have"]},
    {"sentence": "If I ___ you, I would apologize.", "answer": "were", "wrong": ["was", "am", "be"]},
    {"sentence": "He asked me ___ I wanted to join.", "answer": "whether", "wrong": ["weather", "wether", "if or not"]},
    {"sentence": "The scissors ___ on the desk.", "answer": "are", "wrong": ["is", "was", "be"]},
    {"sentence": "Each of the students ___ a book.", "answer": "has", "wrong": ["have", "had", "having"]},
    {"sentence": "I wish I ___ taller.", "answer": "were", "wrong": ["was", "am", "be"]},
    {"sentence": "The committee ___ its decision.", "answer": "made", "wrong": ["make", "makes", "making"]},
    {"sentence": "She ___ her keys before leaving.", "answer": "checked", "wrong": ["check", "checks", "checking"]},
    {"sentence": "There ___ many books on the shelf.", "answer": "are", "wrong": ["is", "was", "be"]},
    {"sentence": "He ___ never seen a whale.", "answer": "has", "wrong": ["have", "is", "was"]},
    {"sentence": "The dog and the cat ___ friends.", "answer": "are", "wrong": ["is", "be", "was"]},
    {"sentence": "She asked ___ the museum was open.", "answer": "if", "wrong": ["that", "what", "which"]},
    {"sentence": "They ___ arrived when it started raining.", "answer": "had", "wrong": ["have", "has", "was"]},
    {"sentence": "I ___ reading this book for two hours.", "answer": "have been", "wrong": ["am", "was", "had"]},
    {"sentence": "___ of the options is correct.", "answer": "Neither", "wrong": ["None", "Both", "Either"]},
    {"sentence": "She speaks more ___ than her sister.", "answer": "quietly", "wrong": ["quiet", "quieter", "quietest"]},
]

PUNCTUATION_QUESTIONS = [
    {"sentence": "whats your name", "answer": "What's your name?", "type": "missing punctuation"},
    {"sentence": "i cant believe it", "answer": "I can't believe it!", "type": "missing punctuation"},
    {"sentence": "the boys ball", "answer": "the boy's ball", "type": "apostrophe"},
    {"sentence": "its raining outside", "answer": "It's raining outside.", "type": "apostrophe/capital"},
    {"sentence": "london is the capital of england", "answer": "London is the capital of England.", "type": "capitals"},
    {"sentence": "we visited paris france and rome italy", "answer": "We visited Paris, France and Rome, Italy.", "type": "capitals/commas"},
    {"sentence": "dr smith said hello", "answer": "Dr. Smith said, \"Hello.\"", "type": "abbreviation/quotes"},
    {"sentence": "i like apples oranges and bananas", "answer": "I like apples, oranges, and bananas.", "type": "commas"},
]


class EnglishQuestionGenerator:
    """Generate English comprehension and grammar questions."""
    
    def __init__(self, db_path: str = "elevenplustutor.db"):
        self.db_path = db_path
    
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def save_question(self, question: dict):
        """Save a question to the database."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO questions (
                id, exam_type, subject, topic, question_type, difficulty,
                question_text, options, correct_answer, correct_index,
                marks_available, hint, worked_solution
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question['id'],
            question.get('exam_type', '11plus_gl'),
            question['subject'],
            question.get('topic', question['question_type']),
            question['question_type'],
            question['difficulty'],
            question['question_text'],
            json.dumps(question['options']),
            question['correct_answer'],
            question['correct_index'],
            question.get('marks_available', 1),
            question.get('hint'),
            question.get('worked_solution')
        ))
        
        conn.commit()
        conn.close()
    
    def generate_comprehension_questions(self) -> List[dict]:
        """Generate comprehension questions from passages."""
        questions = []
        
        for passage in COMPREHENSION_PASSAGES:
            # Create question data with passage
            for q_data in passage['questions']:
                options = [q_data['a']] + q_data['wrong']
                random.shuffle(options)
                correct_index = options.index(q_data['a'])
                
                question_text = json.dumps({
                    'type': 'comprehension',
                    'title': passage['title'],
                    'passage': passage['text'],
                    'question': q_data['q']
                })
                
                questions.append({
                    'id': str(uuid.uuid4()),
                    'subject': 'english',
                    'question_type': 'comprehension',
                    'difficulty': 3,
                    'question_text': question_text,
                    'options': options,
                    'correct_answer': q_data['a'],
                    'correct_index': correct_index,
                    'worked_solution': f"From the passage '{passage['title']}': The answer is '{q_data['a']}'."
                })
        
        return questions
    
    def generate_spelling_questions(self, count: int = 30) -> List[dict]:
        """Generate spelling questions."""
        questions = []
        
        for _ in range(count):
            word_set = random.choice(SPELLING_WORDS['correct'])
            correct = word_set[0]
            wrong = list(word_set[1:])
            
            options = [correct] + wrong
            random.shuffle(options)
            correct_index = options.index(correct)
            
            questions.append({
                'id': str(uuid.uuid4()),
                'subject': 'english',
                'question_type': 'spelling',
                'difficulty': random.choice([2, 3]),
                'question_text': "Which word is spelled correctly?",
                'options': options,
                'correct_answer': correct,
                'correct_index': correct_index,
                'worked_solution': f"The correct spelling is '{correct}'."
            })
        
        return questions
    
    def generate_grammar_questions(self) -> List[dict]:
        """Generate grammar questions."""
        questions = []
        
        for g in GRAMMAR_QUESTIONS:
            options = [g['answer']] + g['wrong']
            random.shuffle(options)
            correct_index = options.index(g['answer'])
            
            questions.append({
                'id': str(uuid.uuid4()),
                'subject': 'english',
                'question_type': 'grammar',
                'difficulty': random.choice([2, 3]),
                'question_text': f"Choose the correct word to complete the sentence:\n\n{g['sentence']}",
                'options': options,
                'correct_answer': g['answer'],
                'correct_index': correct_index,
                'worked_solution': f"The correct answer is '{g['answer']}'."
            })
        
        return questions


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate English questions')
    parser.add_argument('--type', choices=['comprehension', 'spelling', 'grammar', 'all'], default='all')
    parser.add_argument('--db', default='elevenplustutor.db')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    generator = EnglishQuestionGenerator(args.db)
    questions = []
    
    if args.type in ['comprehension', 'all']:
        print("Generating comprehension questions...")
        questions.extend(generator.generate_comprehension_questions())
    
    if args.type in ['spelling', 'all']:
        print("Generating spelling questions...")
        questions.extend(generator.generate_spelling_questions(30))
    
    if args.type in ['grammar', 'all']:
        print("Generating grammar questions...")
        questions.extend(generator.generate_grammar_questions())
    
    if args.dry_run:
        print(f"\nGenerated {len(questions)} questions (not saved)")
        for q in questions[:3]:
            print(f"\nType: {q['question_type']}")
            print(f"Q: {q['question_text'][:100]}...")
    else:
        for q in questions:
            generator.save_question(q)
        print(f"\nSaved {len(questions)} English questions to database")


if __name__ == '__main__':
    main()
