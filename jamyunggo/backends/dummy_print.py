from config import config


def notify(module_name, title, text=None, url=None, name=None):
    if not config["DUMMY"]["ENABLED"]:
        return False
    print("MODULE_NAME:", module_name)
    if name:
        print("NAME:", name)
    print("TITLE:", title)
    if url:
        print("URL:", url)

    if text:
        print("TEXT:", text)

    return True
