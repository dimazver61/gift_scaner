import argparse
import time

import coloring

from src.tg_client import TgClient

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Phone")
    args = parser.parse_args()

    client = TgClient(args.phone)

    gifts = client.get_available_gifts()
    # cur_gifts_id = [g["id"] for g in gifts if g["remaining_count"] != 0]
    cur_gifts_id = []
    while 1:
        try:
            gifts = client.get_available_gifts()
            new_gifts = [g for g in gifts if g["remaining_count"] != 0]
            new_gifts_id = [g["id"] for g in new_gifts]

            for ngi in new_gifts_id:
                if ngi not in cur_gifts_id:

                    print("новый гифт")
                    cur_gifts_id.append(ngi)
                    gift = [ng for ng in new_gifts if ng["id"] == ngi][0]

                    text = f"New Gift | {gift['star_count']} STARS"

                    time.sleep(2)
                    client.tg.send_message(907409516, text)

                    # time.sleep(2)
                    # client.tg.send_message(112298936, text)

        except Exception as e:
            print(coloring.red(f"[!] Error: {str(e)}"))
        finally:
            time.sleep(10)

    # purchase_result = client.tg.call_method("starTransactionTypeGiftPurchase", {
    #     "owner_id": 907409516,
    #     # "gift": gift
    # })
    # purchase_result.wait()
    #
    # if purchase_result.error:
    #     print(purchase_result.error_info)

    # gifts = [Gift(**g) for g in m.update["gifts"]]
    # select_gifts = [g for g in gifts if g.remaining_count != 0 and g.upgrade_star_count != 0]
    #
    # for g in select_gifts:
    #     print(g.sticker.emoji, g.total_count, g.star_count, g.remaining_count)
