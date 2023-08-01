<div><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a><a href='https://www.twitch.tv/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Twitch&color=b9a3e3&logo=Twitch&logoColor=ffffff&label=' alt='Twitch' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/manga-pdf-downloader/blob/master/logo.png?raw=true' alt='Manga Pdf Downloader' height='80px'/>



# Manga Pdf Downloader

This project allow ou to download Mangas (al chapters or starting from specific one) and export them to a single pdf file.

Project type: **personal**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li>
<li><a href='#roadmap'>Roadmap</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://requests.readthedocs.io/en/latest/' target='_blank'> <img src='https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png' alt='Requests' title='Requests' height='50px'/> </a></div>

# Media

![Chapter Page](https://github.com/darideveloper/manga-pdf-downloader/blob/master/screenshots/chapter-page.png?raw=true)

![Chapters List Page](https://github.com/darideveloper/manga-pdf-downloader/blob/master/screenshots/chapters-list-page.png?raw=true)

![Terminal Converting](https://github.com/darideveloper/manga-pdf-downloader/blob/master/screenshots/terminal-convert.png?raw=true)

![Terminal Downloader](https://github.com/darideveloper/manga-pdf-downloader/blob/master/screenshots/terminal-download.png?raw=true)

# Details

The project query the chapters and images from manga onlinea read pages, doenload each image and merge the images in a single pdf file. 

You can download a full manga (all chapters), or start in specific chapter (more details in the settings sections). 



## CSS selectors & HTML Tags



For correctly use this project, ou should know about [css selectors](https://www.w3schools.com/cssref/css_selectors.php) and the basics about [html tags](https://www.w3schools.com/tags/ref_byfunc.asp)



## Limitations



the project requiere manga pages who have images stored directly, without streaming, and no bot protection.



If you can open the image link directly in your browser, you can use it in this project.



[Sample image who can be opened directly](https://github.com/darideveloper/manga-pdf-downloader/blob/master/logo.png?raw=true)

# Install

## Third party modules



Install all modules from pip: 



``` bash

$ pip install -r requirements.txt

```



## Programs



To run the project, the following software must be installed:



* Python >= 3.10

# Settings

## Enviroment variables



In the file *.env*, are the main options and settings of the project.



Create a **.env** file, with the following structure:



```bash

{

    "Manga 1 name": {

        "url": "https://manga-1-page",

        "start_at": 0,

        "selector_link": "a",

        "selector_img": "img",

        "img_attrib": "src"

    },

		...

}

```



Sample: 



```bash

{

    "Made in Abyss": {

        "url": "https://www.mangaread.org/manga/made-in-abyss/",

        "start_at": 0,

        "selector_link": "li.wp-manga-chapter > a",

        "selector_img": ".page-break.no-gaps > img[data-src]",

        "img_attrib": "data-src"

    },

    "Saihate No Paladin": {

        "url": "https://www.mangaread.org/manga/saihate-no-paladin/",

        "start_at": 0,

        "selector_link": "li.wp-manga-chapter > a",

        "selector_img": ".page-break.no-gaps > img[data-src]",

        "img_attrib": "src"

    }

}

```



### Key



The key in the previous dictionary is the manga name. It'll be used for the PDF file name and the images folder. 



### url



The web page where all manga chapters are listed.



### start_at



The chapter where the bot'll start downloading the images.



*Note: this is not the chapter number, is the chapter index. Example:* 

*If the manga have the following chapters: 1, 1.1, 2, 3, 3.1..., and you set as 'start_at` the value `2`, the bot will start downloading from the chapter 1.1



### selector_link



The css selector of the chapter link in the manga chapter list page. (usually an `a` html tag)



### selector_img



The css selector of each image, in the chapter preview page (usually an `img` html tag)



### img_attrib



The html stribute where the image link its located (usually a `src` or `data-src` html attribute)

# Run

Run the project folder with python: 

```sh

python .

```



Or run the main file:

```sh

python __main__.py

```

# Roadmap

* [X] Download images

* [X] Merge to PDF

* [X] Dynamic manga page

* [X] Dynamic css selectors

* [X] Split big pdfs in multiple files.

* [ ] Delete old images

