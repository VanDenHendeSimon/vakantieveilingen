from models.VakantieveilingenController import VakantieveilingenController
import json


def main():
    # Fetch blacklist
    with open('./data/blacklist.json', 'r') as f:
        blacklist = json.load(f)

    # Contact vakantieveiligen
    controller = VakantieveilingenController()
    if controller.login("simonvdhende@outlook.com"):
        # Authentication successfull

        auctions = controller.explore_products(5)
        for auction in auctions:
            auction.update(controller.process_auction(auction))
            print(auction)
            print("-" * 20)

        print("DONE")


if __name__ == '__main__':
    main()
