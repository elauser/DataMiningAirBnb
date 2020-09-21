import csv
import aiohttp
import aiofiles
import asyncio


async def download_all_images(csv_reader):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for row in csv_reader:
            url = row["host_picture_url"]
            file = "Images/" + row["id"] + ".jpg"
            task = asyncio.ensure_future(download_image(url, file, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


async def download_image(url, file, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            f = await aiofiles.open(file, mode="wb")
            await f.write(await resp.read())
            await f.close()


if __name__ == "__main__":
    with open("SourceData/listingsNY_aug.csv", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        asyncio.get_event_loop().run_until_complete(download_all_images(csv_reader))
