from typing import List, Dict

sample_list: List[int] = [2, 4, 5, 6]
sample_dict: Dict[str, str] = {"username": "aaa"}

price: int = 100
tax: float = 1.1

def calc_price_including_tax(price: int, tax: float) -> int:
    return int(price*tax)

if __name__ == "__main__":
    print(f"{calc_price_including_tax(price=price, tax=tax)}円")