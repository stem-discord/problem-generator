import json

from loader import QuestionLoader


if __name__ == "__main__":
  print("===== MAIN =========")
  with open("questions.json") as f: 
    data = json.load(f)
    q = QuestionLoader(data)
    q.get_random_question().print_everything()
  
