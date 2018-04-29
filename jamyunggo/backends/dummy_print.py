def notify(module_name, title, text=None, url=None):

    print("MODULE_NAME:", module_name)
    print("TITLE:", title)
    if url:
        print("URL:", url)

    if text:
        print("TEXT:", text)

    return True
