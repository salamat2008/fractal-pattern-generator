import pickle
from json import dumps
from re import escape, finditer, sub
from sqlite3 import connect as sql_connect
from typing import Generator, Iterable


class LSystem:
    _rules: dict[str, str] = {}
    _keywords: list[list[str]] = ()
    
    def __init__(
            self,
            rule: Iterable[str] | dict[str, str] | str | "LSystem" = None,
            keywords: Iterable[str] | Iterable[Iterable[str]] = None,
    ) -> None:
        """
        Initialize the LSystem object.

        :param rule: Rules of the LSystem. Can be an iterable of strings, a dictionary of strings,
                     a single string, or another LSystem object.
        :param keywords: Keywords of the LSystem. Can be an iterable of strings or an iterable of iterables of strings.
        """
        if isinstance(rule, LSystem):
            self.keywords = rule.keywords.copy()
            self.rules = rule.rules.copy()
        elif rule is not None and keywords is not None:
            self.keywords = keywords
            self.rules = rule
    
    @property
    def rules(self) -> dict[str, str]:
        """
        Get the rules of the LSystem.

        :return: Dictionary of rules.
        """
        return self._rules
    
    @rules.setter
    def rules(self, rules: Iterable[str] | dict[str, str] | str) -> None:
        """
        Set the rules of the LSystem.

        :param rules: Rules of the LSystem. Can be an iterable of strings, a dictionary of strings, or a single string.
        """
        if isinstance(rules, dict):
            self._rules = rules.copy()
        elif isinstance(rules, str):
            self._rules.clear()
            rules_list = self.multiplication(rules).split(maxsplit = 1)
            if len(rules_list) == 2:
                self._rules[rules_list[0]] = rules_list[1]
        elif isinstance(rules, Iterable):
            self._rules.clear()
            for rule in rules:
                rule_list = self.multiplication(rule).split(maxsplit = 1)
                if len(rule_list) == 2:
                    self._rules[rule_list[0]] = rule_list[1]
        else:
            raise TypeError("Invalid type for rules.")
    
    @property
    def keywords(self) -> list[list[str]]:
        """
        Get the keywords of the LSystem.

        :return: List of keywords.
        """
        return self._keywords
    
    @keywords.setter
    def keywords(self, keywords: Iterable[str] | Iterable[Iterable[str]]) -> None:
        """
        Set the keywords of the LSystem.

        :param keywords: Keywords of the LSystem. Can be an iterable of strings or an iterable of iterables of strings.
        """
        if not isinstance(keywords, Iterable):
            raise TypeError("Invalid type for keywords. Must be an iterable.")
        temp_keywords = []
        for keyword in keywords:
            if isinstance(keyword, str):
                temp_keywords.append([keyword])
            elif isinstance(keyword, Iterable):
                temp_keywords.append(sorted(keyword, key = len))
            else:
                raise TypeError("Invalid type for keywords. Must be an iterable of strings or iterables of strings.")
        self._keywords = temp_keywords
    
    def generate_action_string(
            self, string: str, number_of_iterations: int, my_memory_endless: bool = False
    ) -> list[tuple[str, int]]:
        """
        Generate the action string based on the LSystem.

        :param string: Starting string.
        :param number_of_iterations: Number of iterations to perform.
        :param my_memory_endless: Flag indicating whether the memory is endless.
        :return: List of tuples representing the action string.
        """
        
        def insert_into_tables(table: str, column: str, value: str) -> int:
            cursor.execute(f"SELECT {column}_id FROM {table} WHERE {column} = ?", (value,))
            if not cursor.fetchone():
                cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
            cursor.execute(f"SELECT {column}_id FROM {table} WHERE {column} = ?", (value,))
            return cursor.fetchone()[0]
        
        with sql_connect("../Lsystem_outs.db") as connection:
            cursor = connection.cursor()
            cursor.executescript(
                    """
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
                        conclusion BLOB NOT NULL,
                        PRIMARY KEY("conclusion_id" AUTOINCREMENT)
                    );
                    CREATE TABLE IF NOT EXISTS keywords (
                        Keywords_array_id INTEGER NOT NULL UNIQUE,
                        Keywords_array TEXT UNIQUE,
                        PRIMARY KEY("Keywords_array_id" AUTOINCREMENT)
                    )
                    """
            )
            
            rules = dumps(self.rules)
            keywords = dumps(self.keywords)
            
            string = self.multiplication(string)
            temp = (
                insert_into_tables("rules", "rule", rules),
                insert_into_tables("keywords", "Keywords_array", keywords),
                insert_into_tables("axioms", "axiom", string)
            )
            
            cursor.execute(
                    """
                    SELECT conclusion_id,
                    conclusions.rule_id,
                    conclusions.Keywords_array_id,
                    conclusions.axiom_id,
                    n_iter
                    FROM conclusions
                    JOIN rules, keywords, axioms
                    ON conclusions.rule_id = rules.rule_id AND
                    conclusions.Keywords_array_id = keywords.Keywords_array_id AND
                    conclusions.axiom_id = axioms.axiom_id
                    WHERE rule = ? AND
                    Keywords_array = ? AND
                    axiom = ? AND
                    n_iter = ?
                    """,
                    (rules, keywords, string, number_of_iterations)
            )
            
            result = cursor.fetchone()
            
            if not result:
                if not my_memory_endless:
                    for _key, _value in self.rules.items():
                        factor = (_value.count(_key) / len(_key)) ** number_of_iterations
                        if factor > 3_000_000:
                            raise OverflowError("Memory limit exceeded.")
                for _ in range(number_of_iterations):
                    for _key, _value in self.rules.items():
                        string = string.replace(_key, _value)
                action_string = tuple(self.formatting(string))
                cursor.execute(
                        """
                        INSERT INTO conclusions (rule_id, Keywords_array_id, axiom_id, n_iter, conclusion)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (*temp, number_of_iterations, pickle.dumps(action_string))
                )
            else:
                cursor.execute('SELECT conclusion FROM conclusions WHERE conclusion_id = ?', [result[0]])
                action_string = pickle.loads(cursor.fetchone()[0])
            
            return action_string
    
    @staticmethod
    def clear_database():
        """
        Clear the LSystem database.
        """
        with sql_connect("../Lsystem_outs.db") as connection:
            cursor = connection.cursor()
            cursor.executescript(
                    """
                    DROP TABLE IF EXISTS rules;
                    DROP TABLE IF EXISTS axioms;
                    DROP TABLE IF EXISTS conclusions;
                    DROP TABLE IF EXISTS keywords;
                    """
            )
    
    def formatting(self, string: str) -> Generator[tuple[str, int], None, None]:
        """
        Format the string by replacing keywords and adding quantity information.

        :param string: Input string.
        :return: Generator of tuples representing the formatted string.
        """
        for keywords in self.keywords:
            for keyword in keywords:
                string = string.replace(keyword, keywords[0])
            string = sub(
                    f"(?<! )(?P<keyword>{escape(keywords[0])})+",
                    lambda match: f" {match.group(1)}({len(match.group(0)) // len(keywords[0])})",
                    string
            )
        result = (
            (match.group(1), int(match.group(2))) for match in finditer(
                r"(?P<keyword>\S+)\((?P<quantity>\d+)\)",
                string, )
        )
        return result
    
    def multiplication(self, argument: str) -> str:
        """
        Perform multiplication of characters based on the keywords.

        :param argument: Input string.
        :return: Resulting string after multiplication.
        """
        for keywords in self.keywords:
            for keyword in keywords:
                argument = sub(
                        f"(?P<keyword>{escape(keyword)})" + r"\((?P<quantity>\d+)\)",
                        lambda match: match.group(1) * int(match.group(2)),
                        argument
                )
        argument = sub(
                r"(?P<keyword>.)\((?P<quantity>\d+)\)",
                lambda match: match.group(1) * int(match.group(2)),
                argument
        )
        return argument
    
    def __repr__(self):
        return f"{self.__class__.__name__}{self.rules, self.keywords}"


if __name__ == "__main__":
    pass
