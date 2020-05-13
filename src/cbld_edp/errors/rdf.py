import cbld_edp.config.messages as msg


class WritingRDFError(Exception):
	def __init__(self, path, message=None):
		"""
		This exception is raised when an error writing the RDF file occurs.

		:param str or None path: Path where the RDF file is located
		:param str or None message: Custom exception message
		"""
		default_message = msg.WRITING_RDF_ERROR.format(path=path)
		super(WritingRDFError, self).__init__(message if message else default_message)


class RDFFileNotFoundError(Exception):
	def __init__(self, path, message=None):
		"""
		This exception is raised when the solution is trying to load an RDF but it cannot find it.

		:param str or None path: Path where the RDF file is located
		:param str or None message: Custom exception message
		"""
		default_message = msg.RDF_FILE_NOT_FOUND_ERROR.format(path=path)
		super(RDFFileNotFoundError, self).__init__(message if message else default_message)


class RDFParserError(Exception):
	def __init__(self, path, message=None):
		"""
		This exception is raised when there is a problem parsing an RDF file to a XML tree.

		:param str or None path: Path where the RDF file is located
		:param str or None message: Custom exception message
		"""
		default_message = msg.RDF_PARSING_ERROR.format(path=path)
		super(RDFParserError, self).__init__(message if message else default_message)


class DatasetNotFoundError(Exception):
	def __init__(self, datamodel, message=None):
		"""
		This exception is raised when trying to remove a dataset from an RDF and it does not exists.

		:param str or None datamodel: Name of the Data Model trying to remoce
		:param str or None message: Custom exception message
		"""
		default_message = msg.DATASET_NOT_FOUND_ERROR.format(datamodel=datamodel)
		super(DatasetNotFoundError, self).__init__(message if message else default_message)


class LastDatasetError(Exception):
	def __init__(self, message=None):
		"""
		This exception is raised when trying to remove a dataset from an RDF when this is the last one remaining.

		:param str or None message: Custom exception message
		"""
		default_message = msg.LAST_DATASET_ERROR
		super(LastDatasetError, self).__init__(message if message else default_message)
