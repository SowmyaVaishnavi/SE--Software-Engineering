import logging
import operator
import re
import secrets

PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
SALES = {"total": 0}
RECEIPT_LINES = []

PROMO_PATTERN = re.compile(r"^\s*total\s*([-+*/])\s*(\d+(?:\.\d+)?)\s*$")
OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Return the total (with tax) for cart_items and record the sale."""
    if receipts is None:
        receipts = []
    subtotal = 0
    for item in cart_items:
        try:
            subtotal = subtotal + PRICE_LIST[item[0]] * item[1]
        except (KeyError, TypeError):
            logging.warning("Skipping invalid cart item: %s", item)
    total = subtotal + subtotal * tax_rate
    receipts.append(total)
    SALES["total"] += total
    receipt_number = secrets.randbelow(9000) + 1000
    RECEIPT_LINES.append(f"Receipt #{receipt_number} total={total:.2f}")
    return total


def apply_promo_code(code_str):
    """Apply a promo like 'total * 0.9' or 'total - 50' to the sales total."""
    match = PROMO_PATTERN.match(code_str)
    if not match:
        raise ValueError(f"Invalid promo code: {code_str!r}")
    operation, value = match.groups()
    return OPERATORS[operation](SALES["total"], float(value))


def update_stock(item, qty):
    """Report a stock update for item; warn if the item is unknown."""
    if item not in PRICE_LIST:
        logging.warning("Cannot update stock: %s not in price list", item)
        return
    print("Stock updated for", item, "by", qty)


def save_receipt_log(file="pos_log.txt"):
    """Append all receipt lines to the log file."""
    with open(file, "a", encoding="utf-8") as log_file:
        for line in RECEIPT_LINES:
            log_file.write(line + "\n")


def print_sales():
    """Print the running sales total."""
    print(f"Sales so far: {SALES['total']}")


def main():
   
    print("Bill 1:", process_checkout([("pen", 3), ("notebook", 2)]))
    print("Bill 2:", process_checkout([("bag", 1), ("laptop", 1)]))
    print("Bill 3:", process_checkout([("bottle", -4)]))
    print("Bill 4:", process_checkout([("pen", "2")], tax_rate=-1))
    update_stock("laptop", 5)
    print("After promo:", apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    try:
        print("After your promo:", apply_promo_code(code))
    except (ValueError, ZeroDivisionError) as err:
        print("Invalid promo code:", err)
    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()
