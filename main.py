import argparse
import datetime
from pprint import pprint
import time

import coloring

from src.tg_client import TgClient

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Phone")
    args = parser.parse_args()

    client = TgClient(args.phone)
    
    cur_gifts_id = []
    while 1:
        try:
            star_balance = client.get_stars()
            gifts = client.get_available_gifts()

            new_gifts = [g for g in gifts 
                         if g["gift"]["remaining_count"] != 0
                         ]
                         
            sorted_new_gifts = sorted(
                new_gifts,
                key=lambda x: x['gift']['star_count'],
                reverse=True
            )

            for ng in sorted_new_gifts:
                gift_id = ng["gift"]["id"]
                gift_price = ng["gift"]['star_count']

                if gift_id not in cur_gifts_id:
                    cur_gifts_id.append(gift_id)

                    print(datetime.datetime.now(), f"New Gift | {gift_price} STARS")
                    if star_balance > gift_price:
                        coloring.print_green('buy gift')
                        print(client.send_gift(gift_id, client.user_id))
                        break
                    else:
                        coloring.print_red("no stars for gift")
                        
        except Exception as e:
            print(coloring.red(f"[!] Error: {str(e)}"))
        finally:
            time.sleep(1)