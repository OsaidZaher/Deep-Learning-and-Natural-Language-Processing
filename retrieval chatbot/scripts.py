
# -*- coding: utf-8 -*-
from collections import Counter
from responses import responses, blank_spot
from user_functions import preprocess, compare_overlap, extract_nouns, compute_similarity
import spacy
import re

# Load SpaCy model
word2vec = spacy.load('en_core_web_sm')

exit_commands = ("quit", "goodbye", "exit", "no")

class ChatBot:
    def __init__(self):
        self.menu_items = {
            "steak": ["meat", "beef", "ribeye", "sirloin", "filet"],
            "pasta": ["spaghetti", "noodles", "fettuccine", "linguine", "penne"],
            "salad": ["greens", "caesar", "garden", "vegetables"],
            "fish": ["salmon", "tuna", "seafood", "cod", "halibut"],
            "dessert": ["cake", "ice cream", "chocolate", "pie", "sweet"],
            "soup": ["broth", "chowder", "bisque"]
        }

        self.intent_patterns = {
            "dietary": r"(vegan|vegetarian|gluten|allergy|allergic|nuts)",
            "price": r"(cost|price|expensive|cheap|dollar|money)",
            "ingredients": r"(made|contain|ingredient|spicy|fresh)",
            "timing": r"(time|long|minutes|hour|available|when)",
            "recommendations": r"(recommend|best|popular|favorite|suggestion)"
        }

    def make_exit(self, user_message):
        if any(command.lower() in user_message.lower() for command in exit_commands):
            print("Thank you for dining with us! Have a great day!")
            return True
        return False

    def identify_intent(self, user_message):
        user_message = user_message.lower()
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, user_message):
                return intent
        return "general"

    def find_menu_item(self, nouns):
        for noun in nouns:
            noun = noun.lower()
            for item, keywords in self.menu_items.items():
                if noun in keywords or noun == item:
                    return item
        return blank_spot

    def find_intent_match(self, responses, user_message):
        intent = self.identify_intent(user_message)
        intent_responses = [r for r in responses if intent in r.lower()]

        if not intent_responses:
            intent_responses = responses

        bow_user_message = Counter(preprocess(user_message))
        processed_responses = [Counter(preprocess(response)) for response in intent_responses]
        similarity_list = [compare_overlap(response, bow_user_message) for response in processed_responses]
        response_index = similarity_list.index(max(similarity_list))
        return intent_responses[response_index]

    def find_entities(self, user_message):
        nouns = extract_nouns(preprocess(user_message))
        menu_item = self.find_menu_item(nouns)
        if menu_item != blank_spot:
            return menu_item

        tokens = word2vec(" ".join(nouns))
        category = word2vec(blank_spot)
        word2vec_result = compute_similarity(tokens, category)
        word2vec_result.sort(key=lambda x: x[2])

        return word2vec_result[-1][0] if word2vec_result else blank_spot

    def respond(self, user_message):
        if not user_message.strip() or len(user_message.split()) < 2:
            print("I'm sorry, could you please provide more details about what you'd like to know?")
            return input("What would you like to know about our menu? ")

        best_response = self.find_intent_match(responses, user_message)
        entity = self.find_entities(user_message)

        print(best_response.format(entity))
        return input("\nWhat else would you like to know about our menu? ")

    def chat(self):
        try:
            print("Welcome to our restaurant! 🍽️")  # Using a simple emoji
        except UnicodeEncodeError:
            print("Welcome to our restaurant!")  # Fallback without emoji
            
        print("You can ask about our dishes, prices, ingredients, or dietary options.")
        user_message = input("\nWhat would you like to know? ")

        while not self.make_exit(user_message):
            user_message = self.respond(user_message)

if __name__ == "__main__":
    bot = ChatBot()
    bot.chat()