import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.package import Package
import logging

log = logging.getLogger(__name__)


class RatingPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rating')

    # IPackageController

    def before_view(self, pkg_dict):
        if pkg_dict['type'] == 'dataset':
            package = Package.get(pkg_dict['id'])
            pkg_dict['ratings'] = package.get_average_rating()
        return pkg_dict
