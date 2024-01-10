from models.assets import Asset


class Template:
    def __init__(self, head: str, nav: str, footer: str, title_prefix: str):
        self.header = head
        self.nav = nav
        self.footer = footer
        self.title_prefix = title_prefix


class Site:
    def __init__(self, title, icon: Asset, html: Asset,
                 css_assets: list[Asset], nav_elements: list[[str, str]], scripts: list[Asset]):
        self.title = title
        self.icon = icon
        self.html = html
        self.css_assets = css_assets
        self.nav_elements = nav_elements
        self.scripts = scripts
