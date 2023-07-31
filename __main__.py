from src.manga_downloader import MangaDownloader

downloader = MangaDownloader ()

print ("MANGA DOWNLOADER...")

# Main menu
while True:
    print ("Select an option:")
    print ("1. Download mangas")
    print ("2. Create pdfs\n")
    input = input("")

    if input == "1":
        downloader.download ()
        print ("Download finished")
    elif input == "2":
        downloader.create_pdf ()
        print ("PDFs created")
    else:
        print ("Invalid option")
        continue
    
    break