import math
import re
from decimal import Decimal
from typing import Generator, Iterable

from rich.console import Console
from rich.table import Table


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
        # We remove * and ^ and replace , with . just so we will have something like x2 - 3.14x + 14 = 0, not x^2 - 3,14*x + 14 = 0 and it will be easier for us to use
        equation = equation.replace("*", "").replace("^", "").replace(",", ".")
        # We add + to the beginning if there is no mark, so later we can easily check only if there is a - or +
        if not equation.startswith(("+", "-")):
            equation = "+" + equation
        # We change a variable name to x, so we don't have to fuck with different names
        equation = "".join(("x" if character.isalpha() else character for character in equation))
        # We add coefficient +-1 to anything with x if there is no coefficient, so every x will have its own coefficient
        equation = re.sub(r"\+x", "+1x", equation)
        equation = re.sub(r"\-x", "-1x", equation)

        return equation

    def reduce_numbers(self, first_number: Decimal, second_number: Decimal) -> tuple[Decimal, Decimal]:
        fraction_gcd = Decimal(math.gcd(int(first_number), int(second_number)))

        return (first_number/fraction_gcd, second_number/fraction_gcd)

    def get_reduced_equation(self, a: Decimal, b: Decimal, c: Decimal) -> str:
        quadratic_coefficient = "x^2 " if a == 1 else "-x^2 " if a == -1 else f"{a}x^2 "

        linear_coefficient_sign = "+" if b > 0 else "-"
        linear_coefficient = f"{linear_coefficient_sign} {abs(b)}x " if b != 0 else ""

        free_term_sign = "+" if c > 0 else "-"
        free_term = f"{free_term_sign} {abs(c)} " if c != 0 else ""

        return f"{quadratic_coefficient}{linear_coefficient}{free_term}= 0"

    def get_coefficient(self, pattern: str, equation: str) -> Decimal:
        """Gets one and only one coefficient of an equation w/o [=] (for example: gets coefficient of a)

        Args:
            pattern (str): pattern of a coefficient to get
            equation (str): equation with coefficients

        Returns:
            Decimal: sum of all coeficients in equation
        """
        occurences = re.finditer(pattern, equation)
        coefficients = (re.search(r"[+-][+-]?(\d*\.)?\d+", occurence[0])[0] for occurence in occurences)

        return Decimal(sum((Decimal(i) for i in coefficients)))

    def get_all_coefficients(self, equation: str) -> tuple[Decimal, Decimal, Decimal]:
        """Gets all coefficients of equation w/o [=]

        Args:
            equation (str): equation from which coefficients are to be taken

        Returns:
            tuple[Decimal, Decimal, Decimal]: tuple containing (a, b, c) coefficients
        """
        equation = self.normalize_equation(equation)

        a_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+x2[ +-]", equation)
        b_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+x[ +-]", equation)
        c_coefficient = self.get_coefficient(r"[+-][+-]?(\d*\.)?\d+[ +-]", equation)

        return (a_coefficient, b_coefficient, c_coefficient)

    def get_equation_coefficients(self, equation: str) -> Generator[Decimal, None, None] | tuple[Decimal, ...]:
        """Gets final coefficients of an equation

        Returns:
            Generator[Decimal, None, None] | tuple[Decimal, ...]: generator object with (a, b, c) coefficients
        """
        # We split equation by [=], we will work with both parts separately
        left_part, right_part = (part.strip() for part in equation.split("="))

        left_coefficients = self.get_all_coefficients(left_part)
        right_coefficients = self.get_all_coefficients(right_part)
        # We subtract right coefficients from left as if we take numbers from one part to another
        final_coefficients = tuple(left_coef - right_coef for left_coef, right_coef in zip(left_coefficients, right_coefficients))

        # We will divide all coefficients by one number if we will not fall in float numbers lake
        if all(float(i).is_integer() for i in final_coefficients):
            coefficients_gcd = math.gcd(*(int(i) for i in final_coefficients))
            final_coefficients = (i / coefficients_gcd for i in final_coefficients)

        return final_coefficients

    def get_equation_solution(self, a: Decimal, b: Decimal) -> str:
        numerator, denominator = self.reduce_numbers(-b, (2*a)) if b != 0 else (-b, 2*a)
        free_term = f"({a})" if a < 0 else str(a)

        return  f"x = {-b} / (2*{free_term}) = {numerator} / {denominator} = {(numerator / denominator).normalize()}"

    def get_equation_solutions(self, discriminant: Decimal, a: Decimal, b: Decimal) -> str:
        """Gets 2 roots of full quadratic equation

        Returns:
            str: tuple with (root1, root2)
        """
        taking_out1 = taking_out2 = ""
        reduced_taking_out1 = reduced_taking_out2 = ""
        discriminant_sqrt = discriminant.sqrt()
        free_term = f"({a})" if a < 0 else str(a)

        numerator1, denominator1 = self.reduce_numbers((-b + discriminant_sqrt), (2*a))
        numerator2, denominator2 = self.reduce_numbers((-b - discriminant_sqrt), (2*a))

        letter_formula1 = "(-b + sqrt(discriminant)) / (2*a) =\n"
        letter_formula2 = "(-b - sqrt(discriminant)) / (2*a) =\n"

        full_formula1 = f" ({-b} + sqrt({discriminant})) / (2*{free_term}) =\n"
        full_formula2 = f" ({-b} - sqrt({discriminant})) / (2*{free_term}) =\n"

        linear_coefficient1 = f"{-b} + " if b != 0 else ""
        linear_coefficient2 = f"{-b} - " if b != 0 else ""

        # We take out the biggest square root from discriminant, so it will be not sqrt(20), but 2*sqrt(5)
        if not float(discriminant_sqrt).is_integer():
            for i in (Decimal(j*j) for j in range(int(discriminant_sqrt), 0, -1)):
                if discriminant % i == 0:
                    taken_out = i.sqrt()
                    decimated_root = discriminant/i

                    reduced_taken_out, reduced_denominator = self.reduce_numbers(taken_out, 2*a)
                    denominator1 = denominator2 = reduced_denominator

                    taking_out1 = f" ({linear_coefficient1}{taken_out}*sqrt({decimated_root})) / (2*{a}) =\n"
                    taking_out2 = f" ({linear_coefficient2}{taken_out}*sqrt({decimated_root})) / (2*{a}) =\n"

                    reduced_taking_out1 = f" ({linear_coefficient1}{reduced_taken_out}*sqrt({decimated_root})) / {reduced_denominator} =\n"
                    reduced_taking_out2 = f" ({linear_coefficient2}{reduced_taken_out}*sqrt({decimated_root})) / {reduced_denominator} =\n"

                    root_extraction1 = f" ({linear_coefficient1}{discriminant_sqrt}) / {reduced_denominator} =\n"
                    root_extraction2 = f" ({linear_coefficient2}{discriminant_sqrt}) / {reduced_denominator} =\n"

                    numerator_addition1 = f" {-b + discriminant_sqrt} / {reduced_denominator} =" if reduced_denominator != 0 else ""
                    numerator_addition2 = f" {-b - discriminant_sqrt} / {reduced_denominator} =" if reduced_denominator != 0 else ""

                    break

        root_extraction1 = f" ({linear_coefficient1}{discriminant_sqrt}) / (2*{a}) =\n"
        root_extraction2 = f" ({linear_coefficient2}{discriminant_sqrt}) / (2*{a}) =\n"

        numerator_addition1 = f" {-b + discriminant_sqrt} / {2*a} =\n"
        numerator_addition2 = f" {-b - discriminant_sqrt} / {2*a} =\n"

        dividing1 =  f" {numerator1} / {denominator1} =\n"
        dividing2 =  f" {numerator2} / {denominator2} =\n"

        result1 = f" {(numerator1 / denominator1).normalize()}"
        result2 = f" {(numerator2 / denominator2).normalize()}"

        expression1 = f"x1 = {letter_formula1}{full_formula1}{taking_out1}{reduced_taking_out1}{root_extraction1}{numerator_addition1}{dividing1}{result1}"
        expression2 = f"x2 = {letter_formula2}{full_formula2}{taking_out2}{reduced_taking_out2}{root_extraction2}{numerator_addition2}{dividing2}{result2}"

        return f"{expression1}\n\n{expression2}"

    def solve_quadratic_equation(self, equation: str) -> (tuple[str, str, str]):
        """Solves quadratic equation and returns roots

        Args:
            equation (str): quadratic equation to solve

        Returns:
            tuple[str, str, str]: tuple containing roots if there are 2 of them (roots can be represented as strings if they are irrational), 1 number if there is only one root and None if there is no real solutions
        """
        a, b, c = self.get_equation_coefficients(equation)
        reduced_equation = self.get_reduced_equation(a, b, c)
        discriminant = b*b - 4*a*c

        if discriminant < 0:
            solution = "No real roots"
        elif discriminant == 0:
            solution = self.get_equation_solution(a, b)
        else:
            solution = self.get_equation_solutions(discriminant, a, b)

        return (reduced_equation, f"D = {b}^2 - 4*{a}*{c} = {b*b} - {4*a*c} = {discriminant}", solution)


    def print_solution(self, equations: Iterable):
        """Pretty prints solution to an equation

        Args:
            equation (str): equation to solve and print
        """
        console = Console()
        table = Table(title="Equations solutions")
        table.add_column("Equation", justify="center", style="red")
        table.add_column("Reduced equation", justify="center", style="green")
        table.add_column("Discriminant", justify="center", style="cyan")
        table.add_column("Solution", justify="center", style="green")

        for equation in equations:
            reduced_equation, discriminant, solution = self.solve_quadratic_equation(equation)
            table.add_row(equation, reduced_equation, discriminant, solution, end_section=True)

        console.print(table)


if __name__ == "__main__":
    solver = Solver()
    #solver.print_solution((line for line in open("./quadratic_equations.txt", encoding="utf-8")))
    solver.print_solution(("4x2 + 14x = 0.5",))
