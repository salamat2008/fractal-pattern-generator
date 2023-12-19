import re
from typing import Iterable


class LSystem2d:
    """
    what?
    """
    _rules: dict[str, str] = {}
    commandskeys = ()

    def __init__(self, rules: Iterable[str] | dict[str, str], commandskeys: Iterable[str]):
        self.rules = rules
        self.commandskeys = commandskeys

    @property
    def rules(self) -> dict[str, str]:
        """
        :return: dict[str, str]
        """
        return self._rules

    @rules.setter
    def rules(self, rules: Iterable[str] | dict[str, str]) -> None:
        self._rules.clear()
        if isinstance(rules, dict):
            self._rules = rules.copy()
        else:
            for item in rules:
                item = self.unformatting(item)
                item = item.split(maxsplit = 1)
                if len(item) > 1:
                    self._rules[item[0]] = item[1]

    def userules(self, axiom: str, n_iter: int) -> tuple[tuple[str, int], ...]:
        axiom = self.unformatting(axiom)
        for _ in range(n_iter):
            for key, value in self.rules.items():
                axiom = axiom.replace(key, value)
        return self.formatting(axiom)

    def formatting(self, string: str) -> tuple[tuple[str, int], ...]:
        """
        :raises TypeError:
        :arg string:
        :return: tuple[tuple[str, int], ...]
        """
        if not isinstance(string, str):
            raise TypeError("The argument must be a string")
        for command in sorted(self.commandskeys):
            for schar in '$&*+.?[\\]^{|}':
                if schar in command:
                    command = command.replace(schar, f'\\{schar}')
            string = re.sub(f'({command})+', lambda match: f" {match.group(1)}({len(match.group(0))}) ", string)
        return tuple((str(math.group(1)), int(math.group(2))) for math in re.finditer(r'(\w+)\((\d+)\)', string))

    @staticmethod
    def unformatting(arg: str | Iterable[tuple[str, int]]) -> str:
        """
        :raises TypeError:
        :parameter arg:
        :returns: str
        """
        if not isinstance(arg, str | tuple):
            raise TypeError("The argument must be a string")
        if isinstance(arg, str):
            string = re.sub(r'(.)\((\d+)\)', lambda match: f'{match.group(1) * int(match.group(2))}', arg)
        else:
            string = ''
            for character, count in arg:
                string += f'{character * count}'
        return string


if __name__ == '__main__':
    pass
