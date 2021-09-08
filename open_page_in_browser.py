import webbrowser

url = "joyreactor.cc"
browser_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(browser_path))
webbrowser.get("firefox").open_new(url)