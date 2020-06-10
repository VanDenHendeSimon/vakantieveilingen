from models.VakantieveilingenController import VakantieveilingenController
from models.DataRepository import DataRepository


def main():
    url = input("url >> ")
    max_price = input("max price >> ")

    try:
        DataRepository.create_auction(url, None, None, None, None)
    except Exception:
        exit("Failed to create auction")

    try:
        DataRepository.create_wishlist(url, max_price)
    except Exception:
        print("Failed to create wishlist item, trying to update")

        try:
            DataRepository.update_wishlist(url, max_price)
        except Exception:
            exit("Failed to update wishlist item")

    for idx, item in enumerate(DataRepository.get_wishlist()):
        print("Item %d:" % (idx + 1))
        print("-" * 50)
        print("url: %s" % item.get("AuctionURL", "Geen URL"))
        print("max price: %.2f\n" % item.get("MaxPrice", -1))


if __name__ == '__main__':
    main()
