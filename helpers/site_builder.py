import copy
import models.site_builder
from models.site_builder import *


class SiteBuilder:
    def __init__(self, template: Template):
        self.template = template

    def build(self, site: models.site_builder.Site) -> models.site_builder.Site:
        """
        Build a site
        :param site: Preconfigured site with the main-content
        :return: Built site with all content
        """

        new_site = copy.deepcopy(site)  # copy for changes not to be applied to the original site variable
        new_site.html = models.assets.Asset(value=
                                            "<!DOCTYPE html><html>" + self.template.header.__str__() + "<body>" +
                                            self.template.nav.__str__() + site.html.value.__str__() +
                                            self.template.footer.__str__() + "</body></html>"
                                            )

        return new_site
