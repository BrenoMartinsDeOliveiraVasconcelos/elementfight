
def validate_num_input(array, uinput: str):
    if uinput.isnumeric():
        if int(uinput) <= len(array):
            return True

    return False


def validate_nonidx_number_input(uinput: str, minimum: int):
    if uinput.isnumeric():
        if int(uinput) >= minimum:
            return True

    return False


def print_list(items: list):
    index = 0
    for i in items:
        index += 1
        print(f"[{index}] {i}")


def highest_force_element(elements: list):
    highest = 0
    element = None
    for elem in elements:
        if elem.force > highest:
            highest = elem.force
            element = elem

    return [highest, element]
