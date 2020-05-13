import logging
import sys
from datetime import datetime
from shutil import copyfile

import requests

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.config.manager import ConfigManager
from cbld_edp.errors.rdf import LastDatasetError
from cbld_edp.models.catalogue import Catalogue
from cbld_edp.models.dataset import Dataset
from cbld_edp.core.rdf.serializer import Serializer
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.helpers import Validators
from cbld_edp.utils.loggers import config_logging

class EDP(object):
	"""
	Solution's core class. It provides de necessary methods to perform the features provided to the user.
	"""

	def __init__(self, file_path):
		"""
		Instantiate the EDP core class.

		:param str file_path: Path to the configuration file
		"""
		try:
			config_logging()

			logging.debug(msg.EDP_INITIALIZING)
			logging.debug(msg.EDP_READING_CONFIG.format(path=file_path))
			ConfigManager.set_config_path(file_path)

			Validators.is_informed(const.URI_STRUCTURE, ConfigManager.get_value(const.MAIN_SECTION, const.URI_STRUCTURE))
			Validators.is_informed(const.URI_HOST, ConfigManager.get_value(const.MAIN_SECTION, const.URI_HOST))
			integration_api = ConfigManager.get_value(const.MAIN_SECTION, const.INTEGRATION_API)
			Validators.is_informed(const.INTEGRATION_API, integration_api)
			Validators.is_valid_url(const.INTEGRATION_API, integration_api)
			Validators.is_informed(const.MAIN_SECTION, ConfigManager.get_value(const.MAIN_SECTION, const.INTEGRATION_ORION))

			integration_api = integration_api.strip('/')
			logging.debug(msg.EDP_CHECK_API_STATUS.format(host=integration_api))
			response = requests.get('{host}/{route}'.format(host=integration_api, route=const.API_URL_STATUS))
			if response.status_code != 200:
				logging.warning(msg.EDP_API_STATUS_DOWN.format(host=integration_api))
		except ValueError:
			import click
			click.echo(msg.EDP_ERROR_INSTANTIATING_LOGGER.format(
				date=datetime.strftime(datetime.now(), const.SIMPLE_DATE_FORMAT), script=__name__))
			sys.exit()
		except Exception as error:
			logging.error(error)
			sys.exit()

	def integrate(self, datamodels):
		"""
		Core function that integrates a new RDF file with a collection of Data Models.
		It removes every previously stored dataset ID. Then, it checks if the param passed is the Data Models'
		collection or 'all' value (to integrate every Data Model in config file). At last, it serializes the Data Models
		passed by and writes the entire new RDF into the filesystem.

		:param tuple datamodels: Data Models that will be added to the RDF file
		:return: None
		"""
		logging.info(msg.EDP_INTEGRATION_START.format(datamodels=', '.join(datamodels)))

		try:
			already_integrated = ConfigManager.get_integrated_datasets()
			for dataset in already_integrated:
				ConfigManager.remove_dataset_id(dataset)
			datamodels = EDP.check_datamodels_parameter(datamodels, False)
			catalogue = Catalogue(datamodels)
			rdf = Serializer.serialize_rdf_create(catalogue)
			Serializer.write_rdf(rdf)
			logging.info(msg.EDP_INTEGRATION_FINISHED_OK)
		except Exception as error:
			logging.error(error)
			logging.info(msg.EDP_INTEGRATION_FINISHED_KO)

	def modify(self, datamodels):
		"""
		Core function that modifies an existing RDF file with new Data Models or upgrades of already existing ones.
		It checks if the param passed is the Data Models' collection or 'all' value (to work with every Data Model in
		config file). Then it modifies the current RDF file with the new datasets and writes the new version of the RDF
		into the filesystem.

		:param tuple datamodels: Data Models that will be added to or modified in the RDF file
		:return: None
		"""
		logging.info(msg.EDP_MODIFICATION_START.format(datamodels=', '.join(datamodels)))

		try:
			rdf = None
			datamodels = EDP.check_datamodels_parameter(datamodels, False)
			for datamodel in datamodels:
				dataset = Dataset(datamodel)
				rdf = Serializer.serialize_rdf_update(dataset, rdf)
			Serializer.write_rdf(rdf)
			logging.info(msg.EDP_MODIFICATION_FINISHED_OK)
		except Exception as error:
			logging.error(error)
			logging.info(msg.EDP_MODIFICATION_FINISHED_KO)

	def delete(self, datamodels):
		"""
		Core function that removes from an existing RDF file datasets from the specified Data Models.
		It checks if the param passed is the Data Models' collection or 'all' value (to work with every Data Model in
		config file). Then it removes the datasets from current RDF file and writes it into the filesystem. In case that
		the Data Model to remove is the last one in the RDF, it deletes the entire file.

		:param tuple datamodels: Data Models that will be removed from the RDF file
		:return: None
		"""

		try:
			logging.info(msg.EDP_DELETE_START.format(datamodels=', '.join(datamodels)))
			rdf = None
			datamodels = EDP.check_datamodels_parameter(datamodels, True)
			for dataset in datamodels:
				rdf = Serializer.serialize_rdf_remove(dataset, ConfigManager.get_dataset_id(dataset), rdf)
				ConfigManager.remove_dataset_id(dataset)
			Serializer.write_rdf(rdf)
			logging.info(msg.EDP_DELETE_FINISHED_OK)
		except LastDatasetError as error:
			logging.warning(error)
			for dataset in ConfigManager.get_integrated_datasets():
				ConfigManager.remove_dataset_id(dataset)
			import os
			os.remove(Helpers.get_rdf_path())
			logging.info(msg.EDP_DELETE_FINISHED_OK)
		except Exception as error:
			logging.error(error)
			logging.info(msg.EDP_DELETE_FINISHED_KO)

	@staticmethod
	def generate_config_file(path):
		"""
		Core function that creates a new configuration as a copy of the template.

		:param str path: Path where the config file will be written
		:return: None
		"""
		try:
			config_logging()
			copyfile(Helpers.get_config_file_template_path(), path)
			logging.info(msg.EDP_CONFIG_FILE_GENERATION.format(path=path))
		except ValueError:
			import click
			click.echo(msg.EDP_ERROR_INSTANTIATING_LOGGER.format(
				date=datetime.strftime(datetime.now(), const.SIMPLE_DATE_FORMAT), script=__name__))
		except Exception:
			logging.error(msg.EDP_CONFIG_FILE_GENERATION_FAILED)

	@staticmethod
	def check_datamodels_parameter(parameter, integrated):
		"""
		Core function that checks datamodels parameter value. If the first value of the tuple is equal to 'all' (default
		value), it searches in config file for every Data Model section to return them. If not, it returns the parameter
		as the user set it.

		:param tuple parameter: Tuple of strings containing the Data Model informed by the user
		:param bool integrated: If the Data Models searched are those already integrated or not
		:return: Collection of Data Models to work with
		:rtype: list[str]
		"""
		if parameter[0] == const.DEFAULT_DATAMODEL_OPTION_COMMAND:
			return ConfigManager.get_integrated_datasets() if integrated else ConfigManager.get_datamodels()
		return list(parameter)

	@staticmethod
	def get_integrated_datamodels():
		"""
		Core function that returns the collection of Data Models (sections from config file) that are currently included
		in the RDF/XML file.

		:return: Collection of Data Models integrated
		:rtype: list[str]
		"""
		return ConfigManager.get_integrated_datasets()
