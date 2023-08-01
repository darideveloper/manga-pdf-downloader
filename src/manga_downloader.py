import os
import json
from time import sleep
from PIL import Image
from src.chrome_dev.chrome_dev import ChromDevWrapper
import requests
from dotenv import load_dotenv

load_dotenv ()

CHROME_PATH = os.getenv ("CHROME_PATH")

class MangaDownloader (ChromDevWrapper):
    
    def __init__ (self):
        
        # Paths
        self.current_folder = os.path.dirname (__file__)
        self.parent_folder = os.path.dirname (self.current_folder)
        self.images_folder = os.path.join (self.parent_folder, 'images')
        self.pdfs_folder = os.path.join (self.parent_folder, 'pdfs')
        self.manga_file = os.path.join (self.parent_folder, 'mangas.json')
        
        # Read settings
        with open (self.manga_file, "r") as file:
            self.mangas = json.load (file)
            

    def download (self):
        """ Download images from mangas in junji-ito.com/manga/ and save images in images folder
        """
        
        # Start chrome
        super().__init__ (chrome_path=CHROME_PATH)
        
        # Loop for each mange in settings
        for manga_name, data in self.mangas.items():
            
            # Get data
            manga_url = data["url"]
            manga_start_at = data["start_at"]
            selector_link = data["selector_link"]
            selector_img = data["selector_img"]
            img_attrib = data["img_attrib"]

            print (f"\nManga: {manga_name}")
            
            # Create images folder if not exists 
            images_folder = os.path.join (self.images_folder, manga_name)
            os.makedirs (images_folder, exist_ok=True)
            
            # Load page 
            self.set_page (manga_url)

            chapters = self.get_attribs(selector_link, "href")
            chapters.reverse ()
            
            # Filter chapters
            chapters = chapters[manga_start_at:]
            
            if not chapters:
                print ("\tNo chapters found, skipping manga...")
                continue
            
            # Get images urls from all chapters
            image_counter = 0
            for chapter in chapters:
                
                sleep (3)
                
                print (f"\tChapter: {chapter}")
                
                
                # Loop for load images
                image_links = []
                while True:
                    # Open each chapter
                    page_loaded = False
                    for _ in range (3):
                        try:
                            self.set_page (chapter)
                        except:
                            sleep (5)
                            continue
                        else:
                            page_loaded = True
                            break
                    
                    if not page_loaded:
                        print ("\t\tPage not loaded, skipping manga...")
                        break
                    
                    # Zoom out to get all images
                    # self.zoom (0.1)
                    
                    # download images
                    image_links = self.get_attribs (selector_img, img_attrib)
                    
                    if not image_links:
                        print ("\t\tNo images found, trying again...")
                        sleep (10)
                        continue
                    
                    break

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
        
        print ("Convering images to pdf...")
        
        # Get mangas folders from images folder
        mangas_folders = os.listdir (self.images_folder)
         
        # Loop for each mange 
        for manga in mangas_folders:
            
            print (f"Creating pdf for: {manga}")
            
            # Get images from mangda folder 
            current_images_folder = os.path.join (self.images_folder, manga)
            images = os.listdir (current_images_folder)
            images_paths = list(map(lambda image: os.path.join (current_images_folder, image), images))
                        
            # Convert to pdf
            images = []
            corrupted_counter = 0
            for image_path in images_paths:
                try:
                    image = Image.open (image_path)
                except:
                    corrupted_counter += 1
                else:
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    images.append (image)
            output_file = os.path.join (self.pdfs_folder, f"{manga}.pdf")
            images[0].save(
                output_file, "PDF" ,resolution=100.0, save_all=True, append_images=images
            )
            
            if corrupted_counter:
                print (f"\t{corrupted_counter} possible corrupted images")
                
            print (f"\t{len(images)} images converted to pdf")
                
            # Close images
            for image in images:
                image.close ()
                
            # Clean data of all open images
            Image.core._initialized = None
            
                                        


