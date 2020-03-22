from pylev import damerau_levenshtein


class ParseCommand:
    def __init__(self, command_list):
        self.command_list = command_list

    def get_command(self, command):
        score = 99999999
        best = ""
        for c in self.command_list:
            s = damerau_levenshtein(command, c)
            if s < score:
                best = c
                score = s
        return best


if __name__ == '__main__':
    commands = [
        "covid",
        "metro",
        "bolsa",
        "wiki",
        "news",
        "r",
        "tempo",
        "moedas",
        "isso",
        "aquilo",
    ]
    cmd = ParseCommand(commands)
    c = cmd.get_command("moeda")
    if c != "moedas":
        print("Deu merda. Retornou {}".format(c))
    else:
        print("Comando e: {}".format(c))


