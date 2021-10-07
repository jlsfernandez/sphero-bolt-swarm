import asyncio
import json
import threading
from sphero.sphero_bolt import SpheroBolt


# [dict[str, str]]
def get_json_data(file: str) -> list:
    """Reads json file and returns a list of dictionaries.

    Parameters
    ----------
    file : str
        location of the json file.

    Returns
    -------
    list[dict[str, str]]
        list with one or more dictionaries.
    """

    with open(file) as json_file:
        return json.load(json_file)


async def run(address_dict):
    bolts = []

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-B198")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-67EA")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-4D1E")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    for bolt in bolts:
        connected = await bolt.connect()
        if not connected:
            bolts.remove(bolt)
        else:
            await bolt.wake()
            await bolt.resetYaw()
            # bolt.queue.put(lambda: bolt.wake())
            # bolt.queue.put(lambda: bolt.resetYaw())

    for bolt in bolts:
        bolt.queue.put(lambda: bolt.setMatrixLED(255, 255, 0))
        bolt.queue.put(lambda: bolt.setBothLEDColors(255, 255, 0))
        await asyncio.sleep(0.05)

    for bolt in bolts:
        bolt.queue.put(lambda: bolt.roll(50, 0, 5))
        bolt.queue.put(lambda: bolt.roll(50, 180, 5))
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(get_json_data('bolt_addresses.json')))
