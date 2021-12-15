import re
from math import sqrt, gcd
from typing import Generator


class Solver:
    def __init__(self, always_use_sqrt: bool = False):
        """Class-container for quadratic equation solver

        Args:
            always_use_sqrt (bool, optional): if set to True solution will always be a number, no strings like 'sqrt(1488.0) / 2.0' will be returned. Defaults to False.
        """
        self.always_use_sqrt = always_use_sqrt

    def normalize_equation(self, equation: str) -> str:
        """Normalizes equation so other methods will be able work with it

        Args:
            equation (str): equation to normailze

        Returns:
            str: normalized equation
        """
        # We remove whitespaces to not fuck with 'em,
        # But we add a whitespace to the end so we can detect the end of an equation
        equation = equation.strip().replace(" ", "") + " "
        # We remove * and ^ just so we will have something like x2 - 3.14x + 14 = 0 not x^2 - 3,14*x + 14 = 0
        equation = equation.replace("*", "").replace("^", "").replace(",", ".")
        # We add + to the beginning if there is no mark
        if not equation.startswith(("+", "-")):
            equation = "+" + equation
        # We change a variable name to x, so we don't have to fuck with different names
        equation = "".join(("x" if character.isalpha() else character for character in equation))
        # We add coefficient +-1 to anything with x if there is no coefficient
        equation = re.sub(r"\+x", "+1x", equation)
        equation = re.sub(r"\-x", "-1x", equation)

        return equation

    def get_coefficient(self, pattern: str, equation: str) -> float:
        """Gets one and only one coefficient of an equation w/o [=] (for example: gets coefficient a)

        Args:
            pattern (str): pattern of a coefficient to get
            equation (str): equation with coefficients

        Returns:
            float: sum of all coeficients in equation
        """
        occurences = re.finditer(pattern, equation)
        coefficients = (re.search(r"[+-][+-]?(\d*\.)?\d+", occurence[0])[0] for occurence in occurences)

        return sum((float(i) for i in coefficients))

    def get_all_coefficients(self, equation: str) -> tuple[float, float, float]:
        """Gets all coefficients of equation w/o [=]

        Args:
            equation (str): equation from which coefficients are to be taken

        Returns:
            tuple[float, float, float]: tuple containing (a, b, c) coefficients
        """
        equation = self.normalize_equation(equation)

        a_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+x2[ +-]", equation)
        b_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+x[ +-]", equation)
        c_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+[ +-]", equation)

        return (a_coefficient, b_coefficient, c_coefficient)

    def get_equation_coefficients(self, equation: str) -> Generator[float, None, None] | tuple[float, ...]:
        """Gets final coefficients of an equation

        Returns:
            Generator[float, None, None] | tuple[float, ...]: generator object with (a, b, c) coefficients
        """
        left_part, right_part = (part.strip() for part in equation.split("="))

        left_coefficients = self.get_all_coefficients(left_part)
        right_coefficients = self.get_all_coefficients(right_part)
        final_coefficients = tuple(left_coef - right_coef for left_coef, right_coef in zip(left_coefficients, right_coefficients))

        # We will divide all coefficients by one number if we will not fall in float numbers lake
        if all(float(i).is_integer() for i in final_coefficients):
            coefficients_gcd = gcd(*(int(i) for i in final_coefficients))
            final_coefficients = (i / coefficients_gcd for i in final_coefficients)

        return final_coefficients

    def solve_quadratic_equation(self, equation: str) -> (tuple[float | str, float | str] | float | None):
        """Solves quadratic equation and returns roots

        Args:
            equation (str): quadratic equation to solve

        Returns:
            tuple[float | str, float | str] | float | None]: tuple containing roots if there are 2 of them (roots can be represented as strings if they are irrational), 1 number if there is only one root and None if there is no real solutions
        """
        a, b, c = self.get_equation_coefficients(equation)

        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return None
        elif discriminant == 0:
            return -b / (2*a)

        discriminant_sqrt = sqrt(discriminant)
        altered_discriminant_sqrt = discriminant_sqrt

        for i in (j*j for j in range(int(discriminant_sqrt), 1, -1)):
            if discriminant % i == 0:
                altered_discriminant_sqrt = f"{sqrt(i)}*sqrt({discriminant/i})"

        if self.always_use_sqrt or (discriminant_sqrt * 10**str(discriminant)[::-1].find('.')).is_integer():
            x1 = (-b + discriminant_sqrt) / (2*a)
            x2 = (-b - discriminant_sqrt) / (2*a)
        else:
            if b != 0:
                x1 = f"({-b} + {altered_discriminant_sqrt}) / {(2*a)}"
                x2 = f"({-b} - {altered_discriminant_sqrt}) / {(2*a)}"
            elif a != 0:
                x1 = f"({altered_discriminant_sqrt}) / {(2*a)}"
                x2 = f"(-{altered_discriminant_sqrt}) / {(2*a)}"
            else:
                x1 = f"{altered_discriminant_sqrt}"
                x2 = f"-{altered_discriminant_sqrt}"

        return (x1, x2)

    def print_solution(self, equation: str):
        """Pretty prints solution to an equation

        Args:
            equation (str): equation to solve and print
        """
        result = self.solve_quadratic_equation(equation)
        if isinstance(result, tuple):
            print(f"{equation.strip()}: {result[0]}; {result[1]}")
        elif isinstance(result, float):
            print(f"{equation.strip()}: {result}")
        elif result is None:
            print(f"{equation.strip()}: No real roots")


if __name__ == "__main__":
    solver = Solver()
    with open("./quadratic_equations.txt", encoding="utf-8") as file:
        for line in file:
            solver.print_solution(line)
    #solver.print_solution("5х2-25 = 0")
