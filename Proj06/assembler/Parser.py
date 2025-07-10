from dataclasses import dataclass
from SymbolTable import SymbolTable
from sys import argv, exit
from Code import Code

class Command:
    pass

@dataclass
class A(Command):
    value: str

@dataclass
class L(Command):
    value: str

@dataclass
class C(Command):
    value: str


class Parser:
    def __init__(self, content):
        self.commands = content.split("\n")
        self.instruction = -1
        self.current = None
        self.advance()

    def has_more_commands(self) -> bool:
        return self.instruction + 1 < len(self.commands)

    def advance(self):
        if not self.has_more_commands():
            return
        self.instruction += 1
        command = self.command_type(self.commands[self.instruction].strip())
        # skip empty lines & comments
        if not command.value or command.value.startswith("//"):
            self.advance()
        else:
            self.current = command

    @staticmethod
    def command_type(command: str) -> Command:
        command = command.split("//")[0].strip()
        if not command:
            return A("")
        if command.startswith("@"):
            return A(command[1:].strip())
        if command.startswith("(") and command.endswith(")"):
            return L(command[1:-1].strip())
        return C(command.strip())

    def symbol(self) -> str:
        if isinstance(self.current, (A, L)):
            return self.current.value
        return None


def single_pass(content: str):
    table = SymbolTable()
    parser = Parser(content)

    rom_address = 0
    ram_address = 16
    result = []

    while True:
        cmd = parser.current

        if isinstance(cmd, L):
            if not table.contains(cmd.value):
                table.add_entry(cmd.value, rom_address)
        else:
            if isinstance(cmd, A):
                sym = cmd.value
                if not sym.isdigit():
                    if not table.contains(sym):
                        table.add_entry(sym, ram_address)
                        ram_address += 1
                    cmd = A(str(table.get_address(sym)))
            result.append(cmd)
            rom_address += 1

        if not parser.has_more_commands():
            break
        parser.advance()

    return result


def parse_C_parts(value: str):
    dest = ""
    comp = ""
    jump = ""

    if "=" in value:
        dest, rest = value.split("=", 1)
    else:
        rest = value

    if ";" in rest:
        comp, jump = rest.split(";", 1)
    else:
        comp = rest

    return dest.strip(), comp.strip(), jump.strip()


def pass2(commands, outpath):
    with open(outpath, "w") as output:
        for cmd in commands:
            if isinstance(cmd, A):
                output.write(f"{int(cmd.value):016b}\n")
            elif isinstance(cmd, C):
                dest, comp, jump = parse_C_parts(cmd.value)
                comp_bits = Code.comp(comp)
                dest_bits = Code.dest(dest)
                jump_bits = Code.jump(jump)

                if not comp_bits or not dest_bits or not jump_bits:
                    print(f"Invalid C-instruction: {cmd.value}")
                    exit(1)

                output.write(f"111{comp_bits}{dest_bits}{jump_bits}\n")


def main():
    if len(argv) != 2:
        print("Invalid argument length.")
        exit(1)

    path = argv[1]
    if not path.endswith(".asm"):
        print("Invalid file extension. Only .asm files are allowed.")
        exit(1)

    with open(path, "r") as f:
        content = f.read().strip()
        if not content:
            print("Empty file")
            exit(1)

    commands = single_pass(content)
    outpath = path.replace(".asm", ".hack")
    pass2(commands, outpath)

    print(f"Wrote: {outpath}")


if __name__ == "__main__":
    main()
