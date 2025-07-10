class SymbolTable:
    def __init__(self):
        self._table = {
            "SP": "0", "LCL": "1", "ARG": "2",
            "THIS": "3", "THAT": "4", "R0": "0",
            "R1": "1", "R2": "2", "R3": "3",
            "R4": "4", "R5": "5", "R6": "6",
            "R7": "7", "R8": "8", "R9": "9",
            "R10": "10", "R11": "11", "R12": "12",
            "R13": "13", "R14": "14", "R15": "15",
            "SCREEN": "16384", "KBD": "24576"
        }
    
    def contains(self, symbol: str) -> bool:
        return self._table.get(symbol, False)
    
    def get_address(self, symbol: str) -> int:
        if not self.contains(symbol):
            return None
        return int(self._table[symbol])

    def add_entry(self, symbol: str, address: int):
        if self.contains(symbol):
            return self.get_address(symbol)
        self._table[symbol] = str(address)