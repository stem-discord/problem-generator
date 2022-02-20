import sympy
import random
import re
from simple_parser import parse

class IRange:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def get_random_value(self):
        raise NotImplementedError("The method is not implemented")


class IntegerRange(IRange):
    """
    Inclusive
    """
    def __init__(self, minimum, maximum):
        super().__init__(minimum, maximum)

    def get_random_value(self):
        return random.randint(self.minimum, self.maximum)

class DecimalRange(IRange):
    """
    Inclusive
    """
    def __init__(self, minimum, maximum):
        super().__init__(minimum, maximum)

    def get_random_value(self):
        return self.minimum + (self.maximum - self.minimum) * random.random()


# Match multiple Match objects
eval_regex = re.compile(r"\$\$(.*?)\$\$", flags=re.S)

class Variable:
    def __init__(self, name, generator, description="An ordinary variable"):
        if len(name) > 1:
          raise Exception("Due to a weird limitation you cannot have multi character variable names")
        self.name = name
        self.symbol = sympy.Symbol(name)
        self.generator = generator
        self.randomize()

    def randomize(self):
        self.value = self.generator.get_random_value()

    def __repr__(self):
        return f"<Variable {self.name} generator={repr(self.generator)}>"

def get_generator(obj):
  if r := obj["range"]:
    # split by -
    minimum, maximum = r.split('-')

    if "." in minimum or "." in maximum:
      # assume decimal
      return DecimalRange(float(minimum), float(maximum))
    else:
      # assume integer
      return IntegerRange(int(minimum), int(maximum))
      

def to_variables(variables_list):
  ret = []
  for obj in variables_list:
    ret.append(Variable(obj["name"], get_generator(obj)))  
  return ret

def expr_subs_variables(expr, variables):
  for var in variables:
    expr = expr.subs(var.symbol, var.value)
  return expr

def evaluate_expression(string, variables):
    global eval_regex
    return re.sub(eval_regex, lambda x: str(expr_subs_variables(parse(x.group(1)), variables).evalf(2)), string)

class Question:
  def __init__(self, id, question, variables, answer, explanation):
    """
    variables is a list of variables
    """
    self.id = id
    self.question = question
    self.variables = to_variables(variables)
    self.answer = answer
    self.explanation = explanation

  def randomize(self):
    for v in self.variables:
      v.randomize()

  def print_everything(self):
    print("Question\n", evaluate_expression(self.question, self.variables))
    print("The answer is\n", evaluate_expression(self.answer, self.variables))
    print("The explanation is\n", evaluate_expression(self.explanation, self.variables))

class QuestionLoader:
    def __init__(self, data):
        self.questions = []
        for question in data["questions"]:
          self.questions.append(Question(question["id"], question["question"], question["variables"], question["answer"], question["explanation"]))

    def get_random_question(self):
        q = random.choice(self.questions)
        q.randomize()
        return q

    def get_question_by_id(self, id):
        for q in self.questions:
          if q.id == id:
            return q

        return None
