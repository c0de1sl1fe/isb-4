import hashlib
import multiprocessing as mp


def algorithm_luhn(card_num: str) -> bool:
    """the function implements the moon algorithm, which checks 
    the validity of the card number"""
    number_card_reverse = list(map(int, card_num))[::-1]
    for i in range(1, len(number_card_reverse), 2):
        number_card_reverse[i] *= 2
        if number_card_reverse[i] > 9:
            number_card_reverse[i] = number_card_reverse[i] % 10 + \
                number_card_reverse[i] // 10
    return sum(number_card_reverse) % 10 == 0


def check_num_card(default_hash: str, bin: int, main_part_card: list, last_num: str) -> bool:
    """the function compares the hash of the assumed 
    card number with the specified hash"""
    card_num = f"{bin}{main_part_card:06d}{last_num}"
    tmp = hashlib.sha3_224(card_num.encode()).hexdigest()
    if tmp == default_hash:
        return card_num
    return False


def find_num_card(default_hash: str, bins: list, last_num: str, pool: int) -> int:
    """the function creates card numbers and searches
    for the desired one by a given hash"""
    list_num = range(1000000)
    arg = []
    for bin in bins:
        for elem in list_num:
            arg.append((default_hash, bin, elem, last_num))
    with mp.Pool(processes=pool) as p:
        for result in p.starmap(check_num_card, arg):
            if result:
                p.terminate()
                return result
    return 0
