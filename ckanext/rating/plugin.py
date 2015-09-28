import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.package import Package
from ckan.logic.action import get
import logging

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def package_show(context, data_dict):
    package_dict = get.package_show(context, data_dict)
    package = Package.get(package_dict['id'])
    package_dict['rating'] = package.get_average_rating()
    return package_dict


class RatingPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)

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

    # IActions

    def get_actions(self):
        return {'package_show': package_show}
