# Yandex-search-image-scrapper
# Installation guide

1. Create environment inside project folder :
# For Win:
    python -m venv env
# For MacOS:
    virtualenv venv

2. Activate environment:
    For Win: .\env\Scripts\activate
    For MacOS: source venv/bin/activate

3. Installing all required packages:
pip install -r requirments.txt

4. Put only one search image in the folder "search-image"
# Note: 
    - The image must be in (jpg, png, jpeg) format. 
    - Image size must be less than 1.5MB to avoid any error.

5. Run the program using this command:
python main.py
# While running the program: 
    - The program will create a folder named "scrapped_images" in the project folder.
    - The program will create a folder named "failed_urls.txt" in the project folder.

6. After the program is finished, you can find all the scrapped images in the folder "scrapped_images".
# Warning: 
    - Don't delete the folder "failed_urls.txt" because it contains all the failed urls during scrapping.
    - Don't delete the folder "scrapped_images" because it contains all the scrapped images.

7.Run following command to download failed urls during scrapping:
python download_failed_urls_image.py

8. After the program is finished, you should delete unnecessary files except:
    - main.py
    - download_failed_urls_image.py
    - scrapper.py
    - env
    - __pycache__
    - requirments.txt
    - README.md
    - .gitignore

9. Before you search for another image, you should delete all the files in the folder "scrapped_images" and "failed_urls.txt" and put the new image in the folder "search-image".

10. Enjoy the program.