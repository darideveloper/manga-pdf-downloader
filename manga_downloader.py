import os
import json
from time import sleep
from PIL import Image
from scraping_manager.automate import WebScraping
import requests

class MangaDownloader (WebScraping):
    
    def __init__ (self):
        
        # Paths
        self.current_folder = os.path.dirname (__file__)
        self.images_folder = os.path.join (self.current_folder, 'images')
        self.pdfs_folder = os.path.join (self.current_folder, 'pdfs')
        self.manga_file = os.path.join (self.current_folder, 'mangas.json')

        # Read settings
        with open (self.manga_file, "r") as file:
            self.mangas = json.load (file)
            
        # Start chrome
        super().__init__ (headless=False)

    def download (self):
        """ Download images from mangas in junji-ito.com/manga/ and save images in images folder
        """
        
        # Loop for each mange in settings
        for manga_name, data in self.mangas.items ():
            
            # Get manga data
            page = data["page"]
            selector_image = data["selector_image"]
            selector_link = data["selector_link"]
            
            print (f"Manga: {manga_name}")
            
            # Create images folder if not exists 
            images_folder = os.path.join (self.images_folder, manga_name)
            os.makedirs (images_folder, exist_ok=True)
            
            # Load page 
            self.set_page (page)

            chapters = self.get_attribs (selector_link, "href")
            chapters.reverse ()
            
            # Get images urls from all chapters
            image_counter = 0
            for chapter in chapters:
                
                sleep (3)
                
                # Open each chapter
                self.set_page (chapter)
                self.zoom (0.1)
                self.refresh_selenium ()
                
                print (f"\tChapter: {chapter}")
                
                # download images
                image_links = self.get_attribs (selector_image, "src")

                for image_link in image_links:
                    
                    image_link = image_link.split ("?")[0]
                 
                    # Incress counter and add 0 to left
                    image_counter += 1
                    image_counter_str = str(image_counter).zfill (4)

                    # Get extension from image link
                    image_extension = image_link.split (".")[-1]
                    
                    # Save image
                    for _ in range (3):
                        res = requests.get (image_link)
                        image_path = os.path.join (images_folder, f"{image_counter_str}.{image_extension}")
                        try:
                            with open (image_path, "wb") as file:
                                file.write (res.content)
                        except:
                            print ("\t\tImage corrupted, trying again...")
                            sleep (3)                        
                            continue
                        else:
                            break

    def create_pdf (self):
        """ Convert already downloaded images to pdf and save pdfs in pdfs folder
        """
         
        # Loop for each mange in settings
        print ("Convering images to pdf...")
        for manga_name, url in self.mangas.items ():
            
            print (f"Creating pdf for: {manga_name}")
            
            # Get images from mangda folder 
            current_images_folder = os.path.join (self.images_folder, manga_name)
            images = os.listdir (current_images_folder)
            images_paths = list(map(lambda image: os.path.join (current_images_folder, image), images))
                        
            # Convert to pdf
            images = []
            for image_path in images_paths:
                image = Image.open (image_path)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                images.append (image)
            output_file = os.path.join (self.pdfs_folder, f"{manga_name}.pdf")
            images[0].save(
                output_file, "PDF" ,resolution=100.0, save_all=True, append_images=images
            )
                                    


