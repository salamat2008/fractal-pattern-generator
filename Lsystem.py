from json import dumps, loads
from re import escape, finditer, sub
from sqlite3 import connect as sqconnect
from typing import Iterable, NamedTuple


class Coincidences(NamedTuple):
    character: str
    quantity: int


class LSystem:
    _rules: dict[str, str] = {}
    _keywords: list[list[str]] = ()

    def __init__(
            self,
            arg1: Iterable[str] | dict[str, str] | str | "LSystem" | None = None,
            arg2: Iterable[str] | Iterable[Iterable[str]] | None = None,
    ) -> None:
        """
        LSystem(self, arg1: Iterable[str] | dict[str, str] | str,
        arg2: Iterable[str] | Iterable[Iterable[str]])

        LSystem(self, arg1: LSystem2d)
        :raises TypeError:
        :parameter args:
        """
        if isinstance(arg1, LSystem):
            print(type(arg1))
            self.keywords = arg1.keywords.copy()
            self.rules = arg1.rules.copy()
        elif (arg2 is not None) and (arg1 is not None):
            self.keywords = arg2
            self.rules = arg1

    @property
    def rules(self) -> dict[str, str]:
        return self._rules

    @rules.setter
    def rules(self, rules: Iterable[str] | dict[str, str] | str) -> None:
        if isinstance(rules, dict):
            self._rules = rules.copy()
        elif isinstance(rules, str):
            self._rules.clear()
            rules: list = self.multiplication(rules).split(maxsplit = 1)
            if len(rules) == 2:
                self._rules[rules[0]] = rules[1]
        elif isinstance(rules, Iterable):
            self._rules.clear()
            rules: Iterable
            for rule in rules:
                rule = self.multiplication(rule).split(maxsplit = 1)
                if len(rule) == 2:
                    self._rules[rule[0]] = rule[1]
        else:
            raise TypeError

    @property
    def keywords(self) -> list[list[str]]:
        return self._keywords

    @keywords.setter
    def keywords(self, keywords: Iterable[str] | Iterable[Iterable[str]]) -> None:
        if not isinstance(keywords, Iterable):
            raise TypeError(
                    "The argument must be a Iterable[Iterable[str]] or Iterable[str]"
            )
        temp1 = []
        for keyword in keywords:
            if isinstance(keyword, str):
                temp1.append([keyword])
            elif isinstance(keyword, Iterable):
                temp1.append(sorted(keyword))
            else:
                raise TypeError(
                        "The argument must be a Iterable[Iterable[str]] or Iterable[str]"
                )
        self._keywords = temp1

    def generate_action_string(self, axiom: str, n_iter: int, mymemoryisendless: bool = False
                               ) -> tuple[Coincidences, ...]:
        """
        :param mymemoryisendless: bool
        :param axiom: str or Iterable[tuple[str, int]]
        :param n_iter: int
        :return: tuple[Coincidences, ...]
        """

        def insert_in_to_tables(table: str, column: str, value: str) -> int:
            cursor.execute(f"SELECT {column}_id FROM {table} WHERE {column} = ?", (value,))
            if not cursor.fetchone():
                cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
            cursor.execute(f"SELECT {column}_id FROM {table} WHERE {column} = ?", (value,))
            return cursor.fetchone()[0]

        def toCoincidences(obj: Iterable):
            return Coincidences(*obj)

        with sqconnect("Lsystemouts.db") as connection:
            cursor = connection.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS rules (
                rule_id INTEGER NOT NULL UNIQUE,
                rule TEXT UNIQUE,
                PRIMARY KEY("rule_id" AUTOINCREMENT)
                );
            CREATE TABLE IF NOT EXISTS axioms (
                axiom_id INTEGER NOT NULL UNIQUE,
                axiom TEXT NOT NULL UNIQUE,
                PRIMARY KEY("axiom_id" AUTOINCREMENT)
                );
            CREATE TABLE IF NOT EXISTS conclusions (
                conclusion_id INTEGER NOT NULL UNIQUE,
                rule_id INTEGER NOT NULL,
                Keywords_array_id INTEGER NOT NULL,
                axiom_id INTEGER NOT NULL,
                n_iter INTEGER NOT NULL DEFAULT 1,
                conclusion TEXT NOT NULL,
                PRIMARY KEY("conclusion_id" AUTOINCREMENT)
                );
            CREATE TABLE IF NOT EXISTS kkeywords (
                Keywords_array_id INTEGER NOT NULL UNIQUE,
                Keywords_array TEXT UNIQUE,
                PRIMARY KEY("Keywords_array_id" AUTOINCREMENT)
                )
            """)
            rules: str = dumps(self.rules)
            Keywords: str = dumps(self.keywords)
            axiom = self.multiplication(axiom)
            n_iter: int
            temp = (insert_in_to_tables("rules", "rule", rules),
                    insert_in_to_tables("kkeywords", "Keywords_array", Keywords),
                    insert_in_to_tables("axioms", "axiom", axiom))
            cursor.execute("""
            SELECT conclusion_id, 
            conclusions.rule_id, 
            conclusions.Keywords_array_id, 
            conclusions.axiom_id, 
            n_iter 
            FROM conclusions 
            JOIN rules, kkeywords, axioms
            ON conclusions.rule_id = rules.rule_id AND 
            conclusions.Keywords_array_id = kkeywords.Keywords_array_id AND
            conclusions.axiom_id = axioms.axiom_id
            WHERE rule = ? AND 
            Keywords_array = ? AND 
            axiom = ? AND
            n_iter = ?
            """, (rules, Keywords, axiom, n_iter))
            result = cursor.fetchone()
            if not result:
                if not mymemoryisendless:
                    for _key_, _value_ in self.rules.items():
                        factor = (_value_.count(_key_) / len(_key_)) ** n_iter
                        if factor > 2_000_000:
                            raise OverflowError()
                for _ in range(n_iter):
                    for _key_, _value_ in self.rules.items():
                        axiom = axiom.replace(_key_, _value_)
                action_string = self.formatting(axiom)
                cursor.execute("""
                    INSERT INTO conclusions (rule_id, Keywords_array_id, axiom_id, n_iter, conclusion)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                               (*temp, n_iter, dumps(action_string)))
            else:
                cursor.execute('SELECT conclusion FROM conclusions WHERE conclusion_id = ?', [result[0]])
                action_string = tuple(map(toCoincidences, loads(cursor.fetchone()[0])))
            return action_string

    @staticmethod
    def cleardatabase():
        with sqconnect("Lsystemouts.db") as connection:
            cursor = connection.cursor()
            cursor.executescript(
                    """
                    DROP TABLE IF EXISTS rules;
                    DROP TABLE IF EXISTS axioms;
                    DROP TABLE IF EXISTS conclusions;
                    DROP TABLE IF EXISTS kkeywords;
                    """
            )

    def formatting(self, string: str) -> tuple[Coincidences, ...]:
        """
        :param string: str
        :return: tuple[tuple[str, int], ...]
        """

        def repl(match):
            return f" {match.group(1)}({len(match.group(0)) // len(keywords[0])})"

        for keywords in self.keywords:
            for keyword in keywords:
                string = string.replace(keyword, keywords[0])
            string = sub(f"(?<! )({escape(keywords[0])})+", repl, string)
        return tuple(Coincidences(match.group(1), int(match.group(2))) for match in finditer(r"(\S+)\((\d+)\)", string))

    def multiplication(self, argument: str) -> str:
        """
        :parameter argument: str
        :returns: str
        """

        def repl(match):
            return match.group(1) * int(match.group(2))

        for keywords in self.keywords:
            for keyword in keywords:
                argument = sub(f"({escape(keyword)})" + r"\((\d+)\)", repl, argument)
        argument = sub(r"(.)\((\d+)\)", repl, argument)
        return argument

    def __repr__(self):
        return f"{self.__class__.__name__}{self.rules, self.keywords}"

    def __str__(self):
        return f"{self.__class__.__name__}{self.rules, self.keywords}"


if __name__ == "__main__":
    lsus = LSystem(
            {"F": "FLFRRFLF"},
            (
                ("F", "forward"),
                ("B", "back"),
                ("L", "left"),
                ("R", "right"),
                ("Mf", "mforward"),
                ("Mb", "mback"),
                ("T", 'triangle'),
                ("S", 'square'),
                ("E", 'circle'),
                ("C", 'change')
            ))
    print(lsus.generate_action_string('F', 1))
