from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))

def parse(string):
  global transformations
  return parse_expr(string, transformations=transformations)
