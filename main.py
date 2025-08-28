import argparse
import datetime
import time

import coloring

from src.tg_client import TgClient

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--phone", help="Phone")
    args = parser.parse_args()

    client = TgClient(args.phone)
    
    cur_gifts_id = []
    while 1:
        try:
            star_balance = client.get_stars()
            gifts = client.get_available_gifts()

            # if "gift" in g:

            new_gifts = [
                g for g in gifts if g["gift"]["remaining_count"] != 0
                # g for g in gifts if g["remaining_count"] != 0
                # g for g in gifts if g["last_send_date"] == 0
            ]

            # sorted_new_gifts = sorted(
            #     new_gifts,
            #     key=lambda x: x['gift']['star_count'],
            #     reverse=True
            # )

            sorted_new_gifts = sorted(
                new_gifts,
                # key=lambda x: x['star_count'],
                key=lambda x: x['gift']['star_count'],
                reverse=True
            )

            for ng in sorted_new_gifts:
                # gift_id = ng["id"]
                # gift_price = ng['star_count']

                gift_id = ng["gift"]["id"]
                gift_price = ng["gift"]['star_count']

                if gift_id not in cur_gifts_id:
                    cur_gifts_id.append(gift_id)
                    print(datetime.datetime.now(), f"New Gift | {gift_price} STARS")

                    while star_balance >= gift_price:
                        coloring.print_green(f'buy gift #{gift_id}')
                        print(client.send_gift(gift_id, client.user_id))
                        star_balance = client.get_stars()

                    coloring.print_red(f"no stars for gift #{gift_id}")

        except Exception as e:
            print(coloring.red(f"[!] Error: {str(e)}"))
        finally:
            time.sleep(1)
