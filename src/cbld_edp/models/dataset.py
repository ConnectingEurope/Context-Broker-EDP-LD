import logging

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.config.constants import Model
from cbld_edp.config.manager import ConfigManager
from cbld_edp.models.resource import Resource
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.validators import Validators


class Dataset:
	"""
	A class that represents a single instance of a dataset of those that will be integrated.

	:param str section: Section in the config file where it belongs
	:param str service: FIWARE Service which the Data Models for this dataset belong to
	:param str service_path: FIWARE Service Path where the Data Models of this dataset are located in their service
	:param str type: Type name of the Data Model/entity
	:param str title: The dataset title
	:param str description: Dataset description
	:param str contact_point: Email address of dataset's publisher
	:param list[str] keywords: Collection of keywords
	:param str publisher_name: Name of the organization publishing the dataset
	:param list[str] themes: Categories that apply to this dataset's Data Model
	:param str access_rights: Literal that indicates dataset's openness
	:param str periodicity: Literal that indicates dataset's update frequency
	:param str spatial: Path to a GeoJSON file containing the polygon area where this datasets applies
	:param str landing_page: Web-page URL with information about the dataset
	:param list[str] allocations: Collection of different ways to generate the resources
	:param str issued: Date when the dataset was created
	:param str id: Dataset's unique identifier
	:param str uri: URI built by a URL and dataset's ID
	:param list[Resource] resources: Collection containing the resources that belong to the dataset
	"""

	def __init__(self, section):
		"""
		Initializes Dataset.

		:param str section: Config file section the dataset belongs
		"""
		logging.debug(msg.DATASET_INSTANTIATING_MODEL_START.format(datamodel=section))

		self.section = section
		Validators.is_expected_value(const.DATAMODEL_SECTION, section, ConfigManager.get_datamodels())
		self.service = ConfigManager.get_value(section, const.DATAMODEL_FIWARE_SERVICE)
		self.service_path = ConfigManager.get_value(section, const.DATAMODEL_FIWARE_SERVICE_PATH)
		self.type = ConfigManager.get_value(section, const.DATAMODEL_TYPE)
		Validators.is_informed(const.DATAMODEL_TYPE, self.type)
		self.title = ConfigManager.get_value(section, const.DATASET_TITLE)
		Validators.is_informed(const.DATASET_TITLE, self.title)
		self.description = ConfigManager.get_value(section, const.DATASET_DESCRIPTION)
		Validators.is_informed(const.DATASET_DESCRIPTION, self.description)
		self.contact_point = ConfigManager.get_value(section, const.DATASET_CONTACT_POINT)
		self.keywords = ConfigManager.get_value(section, const.DATASET_KEYWORDS).split('%')
		if len(self.keywords) > 1:
			Validators.is_informed(const.DATASET_KEYWORDS, self.keywords)
		self.publisher_name = ConfigManager.get_value(section, const.DATASET_PUBLISHER_NAME)
		self.publisher_uri = ConfigManager.get_value(section, const.DATASET_PUBLISHER_URI)
		Validators.is_valid_url(const.DATASET_PUBLISHER_URI, self.publisher_uri)
		self.publisher_type = Helpers.transform_vocabulary(const.DATASET_PUBLISHER_TYPE,
														   ConfigManager.get_value(section,
																				   const.DATASET_PUBLISHER_TYPE),
														   const.PUBLISHER_TYPE_RELATION)
		self.publisher_homepage = ConfigManager.get_value(section, const.DATASET_PUBLISHER_HOMEPAGE)
		Validators.is_valid_url(const.DATASET_PUBLISHER_HOMEPAGE, self.publisher_homepage)
		self.themes = Helpers.transform_themes(ConfigManager.get_value(section, const.DATASET_THEMES).split())
		self.access_rights = Helpers.transform_vocabulary(const.DATASET_ACCESS_RIGHTS,
														  ConfigManager.get_value(section, const.DATASET_ACCESS_RIGHTS),
														  const.DATASET_ACCESS_RIGHTS_RELATION)
		self.periodicity = Helpers.transform_vocabulary(const.DATASET_PERIODICITY,
														ConfigManager.get_value(section, const.DATASET_PERIODICITY),
														const.DATASET_FREQUENCY_RELATION)
		self.spatial = ConfigManager.get_value(section, const.DATASET_SPATIAL)
		if self.spatial:
			Validators.is_valid_path(const.DATASET_SPATIAL, self.spatial)
		self.spatial = Helpers.get_spatial_polygon(self.spatial)
		self.landing_page = ConfigManager.get_value(section, const.DATASET_LANDING_PAGE)
		self.allocations = ConfigManager.get_value(section, const.DATASET_ALLOCATION).split()
		self.id = ConfigManager.get_dataset_id(section)
		uri_host = ConfigManager.get_value(const.MAIN_SECTION, const.URI_HOST)
		uri_structure = ConfigManager.get_value(const.MAIN_SECTION, const.URI_STRUCTURE, const.URI_STRUCTURE_DEFAULT)
		self.uri, self.id = Helpers.generate_uri(uri_host, uri_structure, Model.DATASET, self.id if self.id else None)
		logging.debug(msg.DATASET_SAVING_ID.format(datamodel=section, id=self.id))
		ConfigManager.save_dataset_id(section, self.id)
		self.issued = Helpers.get_issued_date(self.id) if self.id else ''

		self.resources = self.create_resources()

		logging.debug(msg.DATASET_INSTANTIATING_MODEL_FINISHED)

	def create_resources(self):
		"""
		Instantiate resources set by config file. Then it adds them to Dataset instance.

		:return: Collection of resources belonging to a dataset
		:rtype: list[Resources]
		"""
		if self.type in const.DATAMODELS.keys():
			datamodels = const.DATAMODELS[self.type]
		else:
			datamodels = const.DATAMODELS_DEFAULT
			datamodels['models'] = [self.type]

		resources = []
		for allocation in self.allocations:
			Validators.is_expected_value(const.DATASET_ALLOCATION, allocation, datamodels['allocation'])
			resources += Resource.create_resources(self, datamodels['models'], allocation)

		logging.debug(msg.DATASET_RESOURCES_CREATED.format(resources=len(resources), datamodel=self.section))
		return resources
