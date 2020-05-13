import logging

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.api.builder import APIBuilder
from cbld_edp.config.constants import Model, Allocation
from cbld_edp.config.manager import ConfigManager
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.validators import Validators


class Resource:
	"""
	A class that represents a single instance of a resources of those that will be integrated.

	:param str section: Section in the config file where it belongs
	:param str license: URL to license information
	:param str rights: Simple text rights information
	:param str title: The resource title
	:param str url: URL for accessing to context data
	:param str uri: URI built by a URL and resource's ID
	"""

	def __init__(self, section):
		"""
		Initializes Resource.

		:param str section: Config file section the resource belongs
		"""
		logging.debug(msg.RESOURCE_INSTANTIATING_MODEL_START.format(datamodel=section))

		self.section = section
		self.license = ConfigManager.get_value(self.section, const.RESOURCE_LICENSE)
		uri_host = ConfigManager.get_value(const.MAIN_SECTION, const.URI_HOST)
		uri_structure = ConfigManager.get_value(const.MAIN_SECTION, const.URI_STRUCTURE, const.URI_STRUCTURE_DEFAULT)
		self.uri = Helpers.generate_uri(uri_host, uri_structure, Model.RESOURCE)[0]
		self.description = msg.RESOURCE_DESCRIPTION
		self.title = ''
		self.url = ''

		logging.debug(msg.RESOURCE_INSTANTIATING_MODEL_FINISHED)

	@staticmethod
	def create_resources(dataset, datamodels, allocation):
		"""
		Creates a collection of resources based on the configuration set.

		:param Dataset dataset: Parent of the resources created
		:param list[str] datamodels: Collection of the Data Models to take into account in the generation
		:param str allocation: Literal that indicates how the filter will be done
		:return: Collection of instantiated resources
		:rtype: list[Resource]
		"""
		logging.debug(msg.RESOURCE_CREATE_RESOURCES.format(allocation=allocation, datamodels=', '.join(datamodels)))

		resources = []
		for datamodel in datamodels:
			if allocation == Allocation.CATEGORY.value:
				resources.append(Resource.create_resource_by_category(dataset, datamodel))
			elif allocation == Allocation.LOCATION.value:
				locations = ConfigManager.get_value(dataset.section, const.RESOURCE_LOCATIONS).split('%')
				Validators.is_informed(const.RESOURCE_LOCATIONS, locations)
				for location in locations:
					resources.append(Resource.create_resource_by_location(dataset, datamodel, location.strip()))

		return resources

	@staticmethod
	def create_resource_by_category(dataset, category):
		"""
		Creates a resource based on a filter by category.

		:param Dataset dataset: The dataset owning the resource to instantiate.
		:param str category: Data Model by which the URL will filter.
		:return: Instantiated dataset.
		:rtype: Resource
		"""
		resource = Resource(dataset.section)
		resource.title = Helpers.split_uppercase(category)
		filters = {'entity': category}
		resource.url = APIBuilder.build_resource_url(dataset.service, dataset.service_path, **filters)
		logging.debug(msg.RESOURCE_CREATE_RESOURCE_ENTITY.format(name=resource.title, datamodel=category))
		return resource

	@staticmethod
	def create_resource_by_location(dataset, category, location):
		"""
		Creates a resource based on a filter by location.

		:param Dataset dataset: The dataset owning the resource to instantiate.
		:param str category: Data Model by which the URL will filter.
		:param str location: Geographical area by which the URL will filter.
		:return: Instantiated dataset.
		:rtype: Resource
		"""
		datamodel = Helpers.split_uppercase(category)
		resource = Resource(dataset.section)
		resource.title = msg.RESOURCE_TITLE_LOCATION.format(datamodel=datamodel, location=location)
		filters = {'entity': category, 'location': location}
		resource.url = APIBuilder.build_resource_url(dataset.service, dataset.service_path, **filters)
		logging.debug(
			msg.RESOURCE_CREATE_RESOURCE_LOCATION.format(name=resource.title, datamodel=category, location=location))
		logging.debug(resource.url)
		return resource
