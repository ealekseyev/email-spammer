from random import randrange as rand

names_people = ["Joe", "Maria", "Evan", "Rohan", "Andy", "Ivan", "Hugo", "Owen", "Vera", "Nick", "Darryl", "Silvana", "Chivis", "Your mom", "David", "Martin", "Chris", "Brianna", "Christina", "Olga", "Noah", "Lightning McQueen", "Melinda", "Eliza", "Samantha", "Olivia", "Mia", "Julia", "Juliette", "Tony", "Anthony", "Anton", "Paul", "Alex", "Sergio", "Rafael", "Diana", "Holly", "Isabel", "Liam", "Ben", "Luke", "Luca", "Oliver", "Mason", "Johnny", "Papa", "Your sister", "Your brother", "Your grandma", "Martina"]
nouns_s_mob = ["person", "cat", "dog", "rat", "media", "queen", "monarch", "member", "photographer", "construction worker", "boy", "girl", "CEO", "savage", "animal", "teen", "train", "truck", "monster truck", "toilet"]
nouns_s_place = ["7/11", "the local am/pm", "the club", "school", "skool", "Santana Row", "your house", "hell", "the mall", "the restaurant"]
verbs_inf_s = ["drive to", "walk to", "cheat on", "eat", "talk with", "sniffle at", "fart on", "go to", "dare", "climb", "fail", "wish on", "repeat", "design", "pick", "cross", "contribute to", "learn", "twist", "provide", "focus", "fold", "fall", "meet", "fit", "collapse"]
verbs_present_s = ["drives to", "walks to", "cheats on", "eats with", "talks to", "sniffles at", "farts on", "goes to", "dares", "climbs", "fails", "wishes at", "designs", "picks on", "crosses", "contributes", "learns", "twists", "provides", "focuses", "folds", "falls", "meets", "fits on", "collapses"]
verbs_past = ["drove to", "walked to", "cheated on", "ate", "talked with", "sniffled at", "farted at", "went to", "dared", "climbed", "failed", "wished on", "repeated", "designed", "picked", "crossed", "contributed to", "learned", "twisted", "provided", "focused", "folded", "fell off", "met", "fit", "collapsed"]
verbs_ing = ["driving to", "walking to", "cheating on", "eating", "talking to", "climbing", "failing", "going to", "wishing on", "designing", "varying", "picking", "contributing to", "crossing", "learning", "twisting", "providing for", "focusing", "folding", "falling off", "meeting with", "fitting", "collapsing off of"]
adj_s = ["slimy", "squeaky", "lush", "pretty", "ugly", "annoying", "disgusting", "egoistic", "flawless", "tricky", "educated", "primal", "overt"]
the_a = ["the", "a"]
the_a_cap = ["The", "A"]

def verb_ing():
	return verbs_ing[rand(len(verbs_ing))]

def verb_past():
	return verbs_past[rand(len(verbs_past))]

def verb_pres():
	return verbs_present_s[rand(len(verbs_present_s))]

def noun_mob():
	return nouns_s_mob[rand(len(nouns_s_mob))]

def noun_place():
	return nouns_s_place[rand(len(nouns_s_place))]

def adj():
	return adj_s[rand(len(adj_s))]

def article():
	return the_a[rand(2)]

def article_cap():
	return the_a_cap[rand(2)]

def verb_inf():
	return verbs_inf_s[rand(len(verbs_inf_s))]

def name():
	return names_people[rand(len(names_people))]

def space(*args):
	lenArgs = len(args)
	s = ""
	for i in range(lenArgs):
		s += args[i]
		if i != lenArgs-1:
			s += " "
	return s

def sent_starter():
	if rand(2) == 1:
		return space(article_cap(), noun_mob())
	else:
		return name()

def rand_sentence():
	mode = rand(6)
	if mode == 0:
		return space(sent_starter(), verb_past(), noun_place()) + "."
	elif mode == 1:
		return space(sent_starter(), "is", verb_ing(), name()) + "."
	elif mode == 2:
		return space(sent_starter(), "is", verb_ing(), noun_place()) + "."
	elif mode == 3:
		return space(sent_starter(), "is", verb_ing(), noun_place()) + "."
	elif mode == 4:
		return space(sent_starter(), "likes to", verb_inf(), noun_place()) + "."
	elif mode == 5:
		return space(sent_starter(), "dislikes", verb_ing(), noun_place()) + "."
	elif mode == 6:
		return space(sent_starter(), adj(), verb_past(), noun_place()) + "."

def rand_name():
	first = ["Alex", "Evan", "Melinda", "Bill", "Steve", "Steven", "Vanessa", "Vera", "Nick", "Nicholas", "Olga", "Julia", "Emma", "Maria", "Oleg", "Andrew", "Niko", "Jake", "Mason", "Logan", "Noah", "Oliver", "Ben", "James", "Liam", "Will", "Mike", "Michael", "Lewis", "Clark", "Andy", "Sebastian", "Aiden", "Daniel", "Henry", "Jackson", "Matt", "Matthew", "Joe", "John", "Carter", "Wyatt", "Owen", "Samuel", "Sam", "Josh", "Joshua", "Charley", "Justin", "Charles", "Jefferson", "Connor", "Eli", "Hunter", "Asher", "Thomas", "Brandon", "Ryan", "Caleb", "Leo", "Nate", "Nathan", "Jack", "Jonathan", "Robert", "Bill", "Anthony", "Tony", "Austin", "Evan", "Ian", "Vaughn", "Larena", "Adam", "Dominic", "Luca", "Lucas", "Zack", "Zachary", "George", "Tyler", "Cole", "Ashton", "Kevin", "Luis", "Richard", "Patrick", "Joel", "Avery", "Myles", "Emiliano", "Kyle", "Cody", "Dante", "Collin", "Jared", "Shane", "Solomon", "Olivia", "Isabella", "Sophia", "Emily", "Abby", "Abigail", "Ella", "Sofia", "Riley", "Lily", "Lillian", "Audrey", "Penelope", "Grace", "Nora", "Zoey", "Alice", "Leah", "Violet", "Brooks", "Anna", "Caroline", "Eva", "Ruby", "Allison", "Nevaeh", "Piper", "Alexa", "Vivian", "Arianna", "Catherine", "Katherine", "Mackenzie", "Clara", "Natalia", "Athena", "Kylie", "Iris", "Annabelle", "Valeria", "Anastasia", "Alyssa", "Ariel", "Cecilia", "Alina", "Kelly", "Sydney", "Daisy", "Kimberly", "Sarah", "Elise", "Alexis", "Diana", "Amara", "Daniela", "Brooke", "Amy", "Nicole", "Rebecca", "Evelyn", "Fiona", "Georgia", "Lila", "Noelle", "Angelina", "Adrianna", "Juliet", "Selena", "Angela", "Phyillis", "Aspen", "Cali", "Jane", "Jan", "Gabrielle"]
	last = ["Smith", "Dickinson", "Doe", "Alexeyev", "Kiraly", "Van Dyne", "Williams", "Miller", "Wilson", "Jones", "Johnson", "Richardson", "Davis", "Moore", "Taylor", "Anderson", "Martin", "Thompson", "Mayfield", "Martinez", "Robinson", "Garcia", "Clark", "Lewis", "Lee", "Li", "Woo", "Wu", "Lu", "Walker", "Howard", "Greene", "Scott", "Wright", "Hernandez", "Murphy", "Perry", "Henderson", "Barnes", "Gupta", "Bansal", "Reed", "Rogers", "King", "Stark", "Cook", "Ross", "Hughes", "Powell", "Bennett", "Stewart", "Price", "Brown", "Coleman", "Jenkins", "Halpert", "Bryant", "Cox", "Flores", "Foster", "Simmons", "Hayes"]
	return space(first[rand(len(first))], last[rand(len(last))])
	
if __name__ == "__main__":
	print(rand_sentence())
	print(rand_name())
