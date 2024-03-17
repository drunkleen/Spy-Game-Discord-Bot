import random


with open("word_list.txt", "r", encoding="utf-8") as file:
    word_list = file.readlines()
    random_word = random.choice(word_list).strip()
    print("Random word:", random_word)

print(random_word)
