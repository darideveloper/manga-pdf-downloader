import os
import sys
import psutil
from time import sleep

import PyChromeDevTools

class ChromDevWrapper ():
    
    def __init__ (self, chrome_path, port:int=9222, proxy_host:str="", proxy_port:str="", start_chrome:bool=True, start_killing:bool=True):    
        """ Open chrome and conhect using PyChromeDevTools

        Args:
            port (int): port or chrome running in debug mode
            proxy_host (str, optional): Proxy ip. Defaults to "".
            proxy_port (str, optional): Proxy port. Defaults to "".
            start_chrome (bool, optional): Open new chrome instance. Defaults to True.
            start_killing (bool, optional): Kill (true) all chrome windows before start. Defaults to True.
        """
        
        if start_killing:
            self.quit ()
            
        if start_chrome:
                        
            command = f'"{chrome_path}" --remote-debugging-port={port} --remote-allow-origins=*'
            if proxy_host != "" and proxy_port != "":
                # Start chrome with proxies
                command += f' --proxy-server={proxy_host}:{proxy_port}'
                
            os.popen (command)
                
            sleep (5)
        
        self.base_wait_time = 2
        
        try:
            self.chrome = PyChromeDevTools.ChromeInterface(port=port)
        except:
            print ("Chrome is not open. Please open chrome with the custom shorcut and try again.")
            sys.exit (1)
            
        self.chrome.Network.enable()
        self.chrome.Page.enable()
        
        
    def count_elems (self, selector:str):
        """ Count elemencts who match with specific css selector

        Args:
            selector (str): css selector
        """
        
        response = self.chrome.Runtime.evaluate (expression=f"document.querySelectorAll('{selector}').length")
        try:
            return response[0]['result']["result"]["value"]
        except:
            return 0
    
    def set_page (self, page:str):
        """ Navigate to specific page

        Args:
            page (str): url to navigate
        """
        
        self.chrome.Page.navigate(url=page)
        self.chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        sleep (self.base_wait_time)
        
    def delete_cookies (self):
        """ Delete all cookies in chrome
        """
        
        self.chrome.Network.clearBrowserCookies()
        sleep (self.base_wait_time)  
    
    def set_cookies (self, cookies:list):
        """ Set cookies in chrome

        Args:
            cookies (list): cookies to set with name, value, domain, path, 
                secure, httpOnly and sameSite
        """
        
        for cookie in cookies:
            try:
                self.chrome.Network.setCookie(
                    name=cookie["name"], 
                    value=cookie["value"], 
                    domain=cookie["domain"], 
                    path=cookie["path"], 
                    secure=cookie["secure"], 
                    httpOnly=cookie["httpOnly"], 
                    sameSite=cookie["sameSite"]
                )
            except:
                pass
                
        sleep (self.base_wait_time)
            
    def send_data_js (self, selector:str, data:str):
        """ Send data to specific input, with js

        Args:
            selector (str): css selector
            data (str): data to send
        """
                        
        self.chrome.Runtime.evaluate (expression=f"document.querySelector('{selector}').value = '{data}'")
        sleep (self.base_wait_time)
        
    def send_data (self, selector:str, data:str):
        """ Send data to specific input using chrome api

        Args:
            selector (str): css selector
            data (str): data to send
        """
        
        # Get input
        dom = self.chrome.DOM.getDocument()
        element = self.chrome.DOM.getDocument()[0]["result"]["root"]["nodeId"]
        result = self.chrome.DOM.querySelector(nodeId=element, selector=selector)
        node_id = result[0]["result"]["nodeId"]
        
        # Focus on the input text box
        self.chrome.DOM.focus(nodeId=node_id)
        
        # Type text
        for char in data:
            self.chrome.Input.dispatchKeyEvent (type="char", text=char, unmodifiedText=char)
        sleep (self.base_wait_time)
                
    def click (self, selector:str):
        """ Click on specific element

        Args:
            selector (str): css selector
        """
        
        self.chrome.Runtime.evaluate (expression=f"document.querySelector('{selector}').click()")
        sleep (self.base_wait_time)
        
    def get_text (self, selector:str):
        """ Get text of visible element

        Args:
            selector (str): css selector
        """
        
        response = self.chrome.Runtime.evaluate (expression=f"document.querySelector ('{selector}').textContent")
        try: 
            return response[0]['result']["result"]["value"].strip()
        except:
            return ""
        
    def get_attrib (self, selector:str, attrib:str):
        """ Get specific attribute from visible element

        Args:
            selector (str): css selector
            attrib (str): attribute to get
        """
        
        response = self.chrome.Runtime.evaluate (expression=f"document.querySelector ('{selector}').getAttribute ('{attrib}')")
        try: 
            return response[0]['result']["result"]["value"].strip()
        except:
            return ""
        
    def get_attribs (self, selector:str, attrib:str):
        """ Get specific attribute from visible elements

        Args:
            selector (str): css selector
            attrib (str): attribute to get
        """
        
        script = 'values = [];'
        script += f'console.log(document.querySelectorAll ("{selector}").forEach(elem => values.push(elem.getAttribute("{attrib}"))));'
        script += 'values;'
        response = self.chrome.Runtime.evaluate (expression=script, returnByValue=True)
        
        values = []
        try:
            values = list(map(lambda value: value.strip(), response[0]['result']["result"]["value"]))
        except:
            pass
        return values
        
    def quit (self, kill_chrome:bool=True):
        """ Close chrome and conexion   

        Args:
            kill_chrome (bool, optional): Kill (true) all chrome windows. Defaults to True.
        """
        
        if kill_chrome:
            for process in psutil.process_iter(['pid', 'name']):
                if 'chrome' in process.info['name']:
                    try:
                        process.kill()
                    except:
                        pass
                    
    def execute_script (self, script:str):
        """ Run js script and get returns

        Args:
            script (str): _description_
        """
        
        response = self.chrome.Runtime.evaluate (expression=script)
        sleep (self.base_wait_time)
        if response[0]['result']["result"]["type"] == "undefined":
            return None
        return response[0]['result']["result"]["value"]