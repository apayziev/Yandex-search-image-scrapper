from scraper import (
    driver,
    get_image_url,
    scroll_down,
    get_data,
    save_image,
)
import os

cwd = os.getcwd()

if __name__ == "__main__":
    try:
        # Open Chrome and navigate to Url
        url = get_image_url()
        if url is None:
            raise Exception("Invalid URL")
        driver.get(url)

        # Scroll down for more image
        scroll_down(4)

        # Get data from yandexs
        urls_dict = get_data()

        driver.quit()
        # Save image from exported url
        save_image(urls_dict)

        for file in os.listdir(cwd):
            # If the file is a .tmp or .jpg file, delete it
            if file.endswith(".tmp") or file.endswith(".jpg"):
                os.remove(file)

    except Exception as exc:
        print(exc)
