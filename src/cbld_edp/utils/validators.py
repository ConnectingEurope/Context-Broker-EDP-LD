import os
import re

from cbld_edp.errors.config import NotExpectedValueError
from cbld_edp.errors.config import NotInformedFieldError
from cbld_edp.errors.config import WrongFormatError
from cbld_edp.errors.rdf import RDFFileNotFoundError
from cbld_edp.errors.rdf import LastDatasetError


class Validators(object):
	"""
	Utilities class that implements static validators methods to use in the project.
	"""

	@staticmethod
	def is_informed(field, value):
		"""
		Checks if a value is informed. If not, raises an exception.

		:param str field: Name of the field in configuration file
		:param str or list[str] value: Value of the field set in configuration file
		:return: None
		:raises NotInformedFieldError:
		"""
		if not value:
			raise NotInformedFieldError(field)

	@staticmethod
	def is_valid_url(field, value):
		"""
		Checks if a given host is a properly formed URL. If not, raises an exception.

		:param str field: Field name which the host belongs to
		:param str value: Host to check (could be domain, localhost or an IP)
		:return: None
		:raises WrongFormatError:
		"""
		if not value:
			return

		regex = re.compile(
			r'^(?:http|ftp)s?://'
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
			r'localhost|'
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
			r'(?::\d+)?'
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		if re.match(regex, value) is None:
			raise WrongFormatError(field, value)

	@staticmethod
	def is_valid_path(field, value):
		"""
		Checks if a given value is a properly formed path. If not, raises an exception.

		:param str field: Field name which the path belongs to
		:param str value: Path to check
		:return: None
		:raises WrongFormatError:
		"""
		import os
		if not os.path.exists(value):
			raise WrongFormatError(field, value)

	@staticmethod
	def is_expected_value(field, value, choices):
		"""
		Check if a specific value appears inside a collection of possible choices. If not, raises an exception.

		:param str field: Name of the field in configuration file
		:param str value: Value of the field set in configuration file
		:param str or list[str] or dict choices: Available possibilities for the field
		:return: None
		:raises NotExpectedValueError:
		"""
		if value and value not in choices:
			raise NotExpectedValueError(field, value, choices)

	@staticmethod
	def is_file_at_path(path):
		"""
		Check if a file on a given path exists in the filesystem. If not, raises an exception.

		:param str path: Path where the file to check is located
		:return: None
		:raises RDFFileNotFoundError:
		"""
		if os.path.isdir('/'.join(path.split('/')[:-1])):
			if os.path.exists(path):
				return
		raise RDFFileNotFoundError(path)

	@staticmethod
	def is_last_dataset(rdf, namespaces, dataset_tag):
		"""
		Check if there is more than one datasets in a given RDF/XML file. If not, raises an exception.

		:param xml.etree.ElementTree.Element rdf: Parsed RDF file
		:param dict namespaces: Namespaces used by the RDF/XML file
		:param str dataset_tag: Tag identifier for dataset element
		:return: None
		:raises LastDatasetError:
		"""
		if len(rdf.findall(dataset_tag, namespaces=namespaces)) == 1:
			raise LastDatasetError
