import logging

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.config.constants import Model
from cbld_edp.config.manager import ConfigManager
from cbld_edp.models.dataset import Dataset
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.validators import Validators


class Catalogue:
	"""
	A class that represents the metadata catalogue that will be integrated.

	:param list[str] sections: Config file sections to integrate.
	:param str title: Datasets catalogue title.
	:param str description: Datasets catalogue description.
	:param str publisher_name: Name of catalogue's publisher.
	:param str homepage: URL where the catalogue is located.
	:param str issued: Date when the catalogue was created.
	:param str id: Catalogue's unique identifier.
	:param str uri: URI built by a URL and catalogue's ID.
	:param list[Dataset] datasets: Collection containing the datasets that will be integrated.
	"""

	def __init__(self, sections):
		"""
		Initializes Catalogue.

		:param list[str] sections: Config file sections to integrate.
		:param bool new: Indicates if the Catalogue to create is a new instance or one instantiated in a previous run
		"""
		logging.debug(msg.CATALOGUE_INSTANTIATING_MODEL_START.format(datamodels=', '.join(sections)))

		self.sections = sections
		self.title = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_TITLE)
		Validators.is_informed(const.CATALOGUE_TITLE, self.title)
		self.description = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_DESCRIPTION)
		Validators.is_informed(const.CATALOGUE_DESCRIPTION, self.description)
		self.publisher_name = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_PUBLISHER_NAME)
		Validators.is_informed(const.CATALOGUE_PUBLISHER_NAME, self.publisher_name)
		self.publisher_uri = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_PUBLISHER_URI)
		Validators.is_informed(const.CATALOGUE_PUBLISHER_URI, self.publisher_uri)
		Validators.is_valid_url(const.CATALOGUE_PUBLISHER_URI, self.publisher_uri)
		self.publisher_type = Helpers.transform_vocabulary(const.CATALOGUE_PUBLISHER_TYPE,
														   ConfigManager.get_value(const.CATALOGUE_SECTION,
																				   const.CATALOGUE_PUBLISHER_TYPE),
														   const.PUBLISHER_TYPE_RELATION)
		self.publisher_homepage = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_PUBLISHER_HOMEPAGE)
		Validators.is_valid_url(const.CATALOGUE_PUBLISHER_HOMEPAGE, self.publisher_homepage)
		self.homepage = ConfigManager.get_value(const.CATALOGUE_SECTION, const.CATALOGUE_HOMEPAGE)
		Validators.is_valid_url(const.CATALOGUE_SECTION, self.homepage)
		uri_host = ConfigManager.get_value(const.MAIN_SECTION, const.URI_HOST)
		uri_structure = ConfigManager.get_value(const.MAIN_SECTION, const.URI_STRUCTURE, const.URI_STRUCTURE_DEFAULT)
		self.uri, self.id = Helpers.generate_uri(uri_host, uri_structure, Model.CATALOGUE)
		self.issued = Helpers.get_issued_date(self.id)

		logging.debug(msg.CATALOGUE_INSTANTIATING_MODEL_FINISHED)

		self.datasets = self.create_datasets(sections)

	@staticmethod
	def create_datasets(sections):
		"""
		Instantiate datasets set by config file. Then it adds them to Catalogue instance.

		:param list[str] sections: Sections' name of the dataset to add to the catalogue.
		:return: Collection of datasets belonging to the catalogue
		:rtype: list[Dataset]
		"""
		datasets = []
		for section in sections:
			dataset = Dataset(section)
			datasets.append(dataset)

		logging.debug(msg.CATALOGUE_DATASETS_CREATED.format(datasets=len(datasets)))
		return datasets
