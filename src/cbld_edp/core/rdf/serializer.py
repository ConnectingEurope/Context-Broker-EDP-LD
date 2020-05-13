import copy
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.errors.rdf import DatasetNotFoundError
from cbld_edp.errors.rdf import RDFFileNotFoundError
from cbld_edp.errors.rdf import RDFParserError
from cbld_edp.errors.rdf import WritingRDFError
from cbld_edp.models.catalogue import Catalogue
from cbld_edp.models.dataset import Dataset
from cbld_edp.models.resource import Resource
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.validators import Validators


class Serializer:
	"""
	The Serializer class provides methods to transform the models defined in the application to a well-formatted RDF/XML file.
	This transformation is done having DCAT-AP 1.1 version in mind. The metadata present in result file will be, at
	best, like the already defined in template.xml file.

	:param dict[str] namespaces: Namespaces needed for the building of the RDF/XML file
	"""
	namespaces = {}

	@staticmethod
	def serialize_rdf_create(catalogue):
		"""
		Serializes an entire catalogue (its datasets and resources and itself) into an RDF/XML format file.

		:param Catalogue catalogue: Catalogue model instance
		:return: Tree representing serialized RDF/XML
		:rtype: ET.ElementTree
		"""
		logging.info(msg.SERIALIZER_RDF_CREATION_START)
		tree = Serializer._load_tree(Helpers.get_rdf_template_path())
		rdf = tree.getroot()

		Serializer.serialize_catalogue(rdf, catalogue)

		logging.info(msg.SERIALIZER_DATASETS_SERIALIZE_START)
		for dataset in catalogue.datasets:
			Serializer.serialize_dataset(rdf, dataset)
		logging.info(msg.SERIALIZER_DATASETS_SERIALIZE_FINISHED)

		logging.info(msg.SERIALIZER_RESOURCES_SERIALIZE_START)
		for dataset in catalogue.datasets:
			for resource in dataset.resources:
				Serializer.serialize_resource(rdf, resource)
		logging.info(msg.SERIALIZER_RESOURCES_SERIALIZE_FINISHED)

		logging.info(msg.SERIALIZER_PUBLISHERS_SERIALIZE_START)
		publishers = [
			(catalogue.publisher_uri, catalogue.publisher_name, catalogue.publisher_type, catalogue.publisher_homepage)]
		for dataset in catalogue.datasets:
			publishers.append(
				(dataset.publisher_uri, dataset.publisher_name, dataset.publisher_type, dataset.publisher_homepage))
		publishers = set(publishers)
		for publisher in publishers:
			Serializer.serialize_publishers(rdf, publisher[0], publisher[1], publisher[2], publisher[3])
		logging.info(msg.SERIALIZER_PUBLISHERS_SERIALIZE_FINISHED)

		Serializer._remove_template_nodes(rdf)

		logging.info(msg.SERIALIZER_RDF_CREATION_FINISHED)
		return tree

	@staticmethod
	def serialize_rdf_update(dataset, rdf_local_tree=None):
		"""
		Updates the serialized RDF adding a new dataset (and its resources) into a new RDF/XML file.

		:param Dataset dataset: Dataset model instance
		:param ET.ElementTree rdf_local_tree: Tree representing locally stored serialized RDF/XML
		:return: Tree representing the updated RDF/XML file
		:rtype: ET.ElementTree
		"""
		logging.info(msg.SERIALIZER_RDF_UPDATE_START.format(dataset=dataset.section))

		if not rdf_local_tree:
			rdf_local_tree = Serializer._load_tree(Helpers.get_rdf_path())
		rdf_local_root = rdf_local_tree.getroot()

		rdf_template = Serializer._load_tree(Helpers.get_rdf_template_path()).getroot()

		Serializer._update_dataset_node(rdf_template, rdf_local_root, dataset)

		Serializer._update_catalogue_date(rdf_local_root, rdf_template)
		Serializer._remove_template_nodes(rdf_template)

		for descendant in rdf_template.findall('*'):
			rdf_local_root.append(descendant)

		catalogue_rdf = rdf_local_root.find(const.RDF_CATALOGUE, namespaces=Serializer.namespaces)
		xpath = const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_CATALOGUE_DATASET,
												 attribute=const.RDF_ATTRIBUTE_RESOURCE, value=dataset.uri)
		if catalogue_rdf.find(xpath, namespaces=Serializer.namespaces) is None:
			logging.info(msg.SERIALIZER_RDF_UPDATE_NEW_DATASET.format(dataset=dataset.section))
			Serializer._set_value(catalogue_rdf, const.RDF_CATALOGUE_DATASET, dataset.uri,
								  attribute=const.RDF_ATTRIBUTE_RESOURCE, duplicate=True)
		else:
			Serializer._remove_dataset_node(dataset.section, rdf_local_root, dataset.id, False, updating=True)

		logging.info(msg.SERIALIZER_RDF_UPDATE_FINISHED.format(dataset=dataset.section))
		return rdf_local_tree

	@staticmethod
	def serialize_rdf_remove(dataset_section, dataset_uri, rdf_local_tree=None):
		"""
		Updates the serialized RDF removing a dataset (and its resources) from an RDF/XML file.

		:param str dataset_section: Name of the section in config file which the dataset belongs to
		:param str dataset_uri: URI of the dataset
		:param ET.ElementTree or None rdf_local_tree: Tree representing locally stored serialized RDF/XML
		:return: Tree representing the updated RDF/XML file
		:rtype: ET.ElementTree
		"""
		logging.info(msg.SERIALIZER_RDF_REMOVE_START.format(dataset=dataset_section))

		if not rdf_local_tree:
			rdf_local_tree = Serializer._load_tree(Helpers.get_rdf_path())
		local_rdf_root = rdf_local_tree.getroot()

		Serializer._remove_dataset_node(dataset_section, local_rdf_root, dataset_uri, remove_from_catalogue=True)

		rdf_template = Serializer._load_tree(Helpers.get_rdf_template_path()).getroot()
		Serializer._update_catalogue_date(local_rdf_root, rdf_template)

		logging.info(msg.SERIALIZER_RDF_REMOVE_FINISHED.format(dataset=dataset_section))
		return rdf_local_tree

	@staticmethod
	def serialize_catalogue(rdf, catalogue):
		"""
		Serializes an instanced catalogue model into its RDF/XML representation.

		:param ET.Element rdf: Root element of RDF/XML
		:param Catalogue catalogue: Catalogue model instance
		:return: XML element representing serialized catalogue
		:rtype: ET.Element
		"""
		logging.info(msg.SERIALIZER_CATALOGUE_SERIALIZE_START.format(datamodels=', '.join(catalogue.sections)))

		catalogue_rdf = Serializer._clone_node(rdf, const.RDF_CATALOGUE)

		Serializer._set_node_attribute(catalogue_rdf, const.RDF_ATTRIBUTE_ABOUT, catalogue.uri)
		Serializer._set_value(catalogue_rdf, const.RDF_TITLE, catalogue.title)
		Serializer._set_value(catalogue_rdf, const.RDF_DESCRIPTION, catalogue.description)
		Serializer._set_value(catalogue_rdf, const.RDF_HOMEPAGE, catalogue.homepage,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE, remove=True)
		Serializer._set_value(catalogue_rdf, const.RDF_ISSUED, Helpers.format_datetime(datetime.utcnow()))
		Serializer._remove_node(catalogue_rdf, const.RDF_MODIFIED)
		Serializer._set_value(catalogue_rdf, const.RDF_PUBLISHER, catalogue.publisher_uri, const.RDF_ATTRIBUTE_RESOURCE)
		uris = [dataset.uri for dataset in catalogue.datasets]
		Serializer._set_multiple_values(catalogue_rdf, const.RDF_CATALOGUE_DATASET, uris,
										attribute=const.RDF_ATTRIBUTE_RESOURCE)

		rdf.append(catalogue_rdf)

		logging.debug(msg.SERIALIZER_CATALOGUE_SERIALIZE_FINISHED)
		return catalogue_rdf

	@staticmethod
	def serialize_dataset(rdf, dataset, updated=False):
		"""
		Serializes an instanced dataset model into its RDF/XML representation.

		:param ET.Element rdf: Root element of RDF/XML
		:param Dataset dataset: Dataset model instance
		:param bool updated: If it is a new or an updated dataset
		:return: XML element representing serialized dataset
		:rtype: ET.Element
		"""
		logging.info(msg.SERIALIZER_DATASET_SERIALIZE_START.format(datamodel=dataset.section))
		dataset_rdf = Serializer._clone_node(rdf, const.RDF_DATASET)

		Serializer._set_node_attribute(dataset_rdf, const.RDF_ATTRIBUTE_ABOUT, dataset.uri)
		Serializer._set_value(dataset_rdf, const.RDF_TITLE, dataset.title)
		Serializer._set_value(dataset_rdf, const.RDF_DESCRIPTION, dataset.description)
		Serializer._set_multiple_values(dataset_rdf, const.RDF_KEYWORD, dataset.keywords)
		Serializer._set_value(dataset_rdf, const.RDF_PUBLISHER, dataset.publisher_uri, const.RDF_ATTRIBUTE_RESOURCE)
		Serializer._set_multiple_values(dataset_rdf, const.RDF_THEME, dataset.themes,
										attribute=const.RDF_ATTRIBUTE_RESOURCE)
		if dataset.contact_point:
			Serializer._set_value(dataset_rdf, const.RDF_ELEMENT_XPATH.format(element=const.RDF_CONTACT_POINT_NAME),
								  dataset.publisher_name)
			Serializer._set_value(dataset_rdf, const.RDF_ELEMENT_XPATH.format(element=const.RDF_CONTACT_POINT_EMAIL),
								  'mailto:{email}'.format(email=dataset.contact_point),
								  attribute=const.RDF_ATTRIBUTE_RESOURCE)
		else:
			Serializer._remove_node(dataset_rdf, const.RDF_CONTACT_POINT)
		Serializer._set_value(dataset_rdf, const.RDF_PERIODICITY, dataset.periodicity,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE, remove=True)
		Serializer._set_value(dataset_rdf, const.RDF_IDENTIFIER, dataset.id)
		Serializer._set_value(dataset_rdf, const.RDF_ISSUED, Helpers.get_issued_date(dataset.id))
		if updated:
			Serializer._set_value(dataset_rdf, const.RDF_MODIFIED, Helpers.format_datetime(datetime.utcnow()))
		else:
			Serializer._remove_node(dataset_rdf, const.RDF_MODIFIED)
		Serializer._set_value(dataset_rdf, const.RDF_RIGHTS, dataset.access_rights,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE, remove=True)
		Serializer._set_value(dataset_rdf, const.RDF_LANDING_PAGE, dataset.landing_page,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE, remove=True)
		if dataset.spatial:
			geometry_nodes = dataset_rdf.findall(const.RDF_ELEMENT_XPATH.format(element=const.RDF_SPATIAL_GEOMETRY),
												 Serializer.namespaces)
			for i, node in enumerate(geometry_nodes):
				node.text = dataset.spatial[i]
		else:
			Serializer._remove_node(dataset_rdf, const.RDF_SPATIAL)
		uris = [resource.uri for resource in dataset.resources]
		Serializer._set_multiple_values(dataset_rdf, const.RDF_DATASET_RESOURCE, uris,
										attribute=const.RDF_ATTRIBUTE_RESOURCE)

		rdf.append(dataset_rdf)

		logging.debug(msg.SERIALIZER_DATASET_SERIALIZE_FINISHED.format(datamodel=dataset.section))
		return dataset_rdf

	@staticmethod
	def serialize_resource(rdf, resource):
		"""
		Serializes an instanced resource model into its RDF/XML representation.

		:param ET.Element rdf: Root element of RDF/XML
		:param Resource resource: Resource model instance
		:return: XML element representing serialized resource
		:rtype: ET.Element
		"""
		logging.debug(msg.SERIALIZER_RESOURCE_SERIALIZE_START)

		resource_rdf = Serializer._clone_node(rdf, const.RDF_RESOURCE)
		Serializer._set_node_attribute(resource_rdf, const.RDF_ATTRIBUTE_ABOUT, resource.uri)
		Serializer._set_value(resource_rdf, const.RDF_ACCESS_URL, resource.url, attribute=const.RDF_ATTRIBUTE_RESOURCE)
		Serializer._set_value(resource_rdf, const.RDF_DESCRIPTION, resource.description)
		Serializer._set_value(resource_rdf, const.RDF_TITLE, resource.title)
		Serializer._set_value(resource_rdf, const.RDF_DOWNLOAD_URL, resource.url,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE)
		Serializer._set_value(resource_rdf, const.RDF_LICENSE, resource.license, attribute=const.RDF_ATTRIBUTE_RESOURCE,
							  remove=True)

		rdf.append(resource_rdf)

		logging.debug(msg.SERIALIZER_RESOURCE_SERIALIZE_FINISHED)
		return resource_rdf

	@staticmethod
	def serialize_publishers(rdf, publisher_uri, publisher_name, publisher_type, publisher_homepage):
		"""
		Serializes a publisher to a Organization node in an RDF/XML file.

		:param ET.Element rdf: Root node of RDF file
		:param str publisher_uri: URI used to reference dataset's publisher
		:param str publisher_name: Name given to dataset's publisher
		:param str publisher_type: URI indicating which kind of publisher is it
		:param str publisher_homepage: Homepage of the publisher
		:return: XML element representing serialized publisher
		:rtype: ET.Element
		"""
		logging.debug(msg.SERIALIZER_PUBLISHER_SERIALIZE_START.format(name=publisher_name))

		publisher_rdf = Serializer._clone_node(rdf, const.RDF_ORGANIZATION)
		Serializer._set_node_attribute(publisher_rdf, const.RDF_ATTRIBUTE_ABOUT, publisher_uri)
		Serializer._set_value(publisher_rdf, const.RDF_ORGANIZATION_NAME, publisher_name)
		Serializer._set_value(publisher_rdf, const.RDF_TYPE, publisher_type, attribute=const.RDF_ATTRIBUTE_RESOURCE,
							  remove=True)
		Serializer._set_value(publisher_rdf, const.RDF_HOMEPAGE, publisher_homepage,
							  attribute=const.RDF_ATTRIBUTE_RESOURCE, remove=True)

		rdf.append(publisher_rdf)

		logging.debug(msg.SERIALIZER_PUBLISHER_SERIALIZE_FINISHED.format(name=publisher_name))
		return publisher_rdf

	@staticmethod
	def write_rdf(rdf):
		"""
		Writes the RDF into a file locally based on constants.

		:param ET.ElementTree rdf: Tree containing RDF catalogue
		:return: None
		:raises WritingRDFError:
		"""
		root_str = ET.tostring(rdf.getroot()).decode('utf8')
		root_str = re.sub('(>|&gt;)(\t|\n|\r|\s)*(<|&lt;)', '\g<1>\g<3>', root_str)
		rdf_str = minidom.parseString(root_str).toprettyxml(indent='\t', encoding='utf-8')
		try:
			with open(Helpers.get_rdf_path(), 'w+') as file:
				file.write(rdf_str.decode('utf8'))
		except:
			raise WritingRDFError(Helpers.get_rdf_path())

	@staticmethod
	def _set_value(parent, node_name, value, attribute=None, duplicate=False, remove=False):
		"""
		Sets a provided value to a specific node depending on if it goes as a text or as an attribute.
		This manages too the possibility of duplicate the node or remove it based on what is needed.

		:param ET.Element parent: Parent node of the node to modify
		:param str node_name: Name of the node to modify
		:param str value: Value to set to specified node
		:param str or None attribute: Indicates the attribute that will be set with the value provided
		:param bool duplicate: If the node has to be cloned and set later
		:param bool remove: If the node must be removed if the value is invalid
		:return: None
		"""
		if remove and not value:
			Serializer._remove_node(parent, node_name)
			return

		element = parent.find(node_name, namespaces=Serializer.namespaces)
		if duplicate:
			element = Serializer._clone_node(parent, node_name)

		if attribute:
			Serializer._set_node_attribute(element, attribute, value)
		else:
			Serializer._set_node_text(element, value)

		if duplicate:
			parent.append(element)

	@staticmethod
	def _set_multiple_values(parent, node_name, values, attribute=None):
		"""
		Sets a provided collection of values to a specific node.
		This node will be cloned from an existing one and then set with the corresponding value.

		:param ET.Element parent: Parent node of the nodes to modify
		:param str node_name: Name of the node to clone and modify
		:param list[str] values: Values to set in different nodes
		:param str or None attribute: Indicates the attribute that will be set with the value provided
		:return: None
		"""
		for value in values:
			Serializer._set_value(parent, node_name, value, attribute=attribute, duplicate=True)
		Serializer._remove_node(parent, node_name)

	@staticmethod
	def _set_node_text(element, value):
		"""
		To a given element, sets its text value to the provided.

		:param ET.Element element: Node to modify
		:param str value: Text value assigned to the element
		:return: None
		"""
		element.text = value

	@staticmethod
	def _set_node_attribute(element, attribute, value):
		"""
		To a given element, sets the value provided to the attribute informed.

		:param ET.Element element: Node to modify
		:param str attribute: Attribute that will be written (contains its name and namespace)
		:param str value: Text value assigned to element's attribute
		:return: None
		"""
		element.set(Serializer._transform_attribute(attribute), value)

	@staticmethod
	def _remove_node(parent, name):
		"""
		Removes the first appearance of a node matching the filter provided.

		:param ET.Element parent: Parent node of the node to remove
		:param str name: Name of the node to remove
		:return: None
		"""
		node = parent.find(name, namespaces=Serializer.namespaces)
		parent.remove(node)

	@staticmethod
	def _clone_node(parent, name):
		"""
		Makes a copy of specified node.

		:param ET.Element parent: Parent node of the node to clone
		:param str name: Name of the node to clone
		:return: Copy of the node specified
		:rtype: ET.Element
		"""
		node = parent.find(name, namespaces=Serializer.namespaces)
		return copy.deepcopy(node)

	@staticmethod
	def _transform_attribute(attribute):
		"""
		Given an attribute, it transforms it to a format usable for ElementTree library.

		:param str attribute: XML attribute in namespace:attribute format
		:return: Attribute in {namespace-uri}attribute format
		:rtype: str
		"""
		prefix, suffix = attribute.split(':')
		uri = Serializer.namespaces[prefix]
		return '{{{uri}}}{suffix}'.format(uri=uri, suffix=suffix)

	@staticmethod
	def _load_tree(xml_path):
		"""
		Loads the ElementTree object from a XML

		:param str xml_path: Path to RDF/XML file.
		:return: Parsed XML file
		:rtype: ET.ElementTree
		"""
		logging.debug(msg.SERIALIZER_LOAD_TREE.format(path=xml_path))

		Validators.is_file_at_path(xml_path)
		Serializer.namespaces = Serializer._get_rdf_namespaces(xml_path)
		Serializer._register_namespaces(Serializer.namespaces)
		try:
			return ET.parse(xml_path)
		except ET.ParseError:
			raise RDFParserError(xml_path)
		except FileNotFoundError:
			raise RDFFileNotFoundError(xml_path)

	@staticmethod
	def _update_dataset_node(rdf_template, rdf_local, dataset):
		"""
		Adds a new dataset and every child depending on it.

		:param ET.Element rdf_template: Root node of RDF template file
		:param ET.Element rdf_local: Root node of RDF local file
		:param Dataset dataset: Dataset to add to the RDF
		:return: None
		"""
		logging.debug(msg.SERIALIZER_UPDATE_DATASET_NODE.format(datamodel=dataset.section))

		Serializer.serialize_dataset(rdf_template, dataset, updated=True)
		for resource in dataset.resources:
			Serializer.serialize_resource(rdf_template, resource)

		if not Serializer._dataset_publisher_node_appearances(rdf_local, dataset.publisher_uri):
			Serializer.serialize_publishers(rdf_template, dataset.publisher_uri, dataset.publisher_name,
											dataset.publisher_type, dataset.publisher_homepage)

	@staticmethod
	def _remove_dataset_node(datamodel, rdf, uuid, remove_from_catalogue, updating=False):
		"""
		Removes a dataset and every node referenced by it from an actual RDF/XML file.

		:param str datamodel: Data Model trying to remove
		:param ET.Element rdf: Root node of already generated RDF file
		:param str uuid: Dataset's identifier
		:param bool remove_from_catalogue: Boolean that indicates if the reference to this dataset in Catalogue node must be removed too
		:param bool updating: Boolean that indicates if this method is called during RDF updating
		:return: None
		:raises DatasetNotFoundError:
		"""
		logging.debug(msg.SERIALIZER_REMOVE_DATASET_NODE.format(datamodel=datamodel))

		from cbld_edp.config.constants import Model
		from cbld_edp.config.manager import ConfigManager
		uri_host = ConfigManager.get_value(const.MAIN_SECTION, const.URI_HOST)
		uri_structure = ConfigManager.get_value(const.MAIN_SECTION, const.URI_STRUCTURE, const.URI_STRUCTURE_DEFAULT)
		uri = Helpers.generate_uri(uri_host, uri_structure, Model.DATASET, uuid)[0]

		dataset = rdf.find(
			const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_DATASET, attribute=const.RDF_ATTRIBUTE_ABOUT, value=uri),
			namespaces=Serializer.namespaces)
		if dataset is None:
			if updating:
				logging.debug(msg.SERIALIZER_REMOVE_DATASET_NODE_NOT_PRESENT)
				return
			else:
				raise DatasetNotFoundError(datamodel)

		Validators.is_last_dataset(rdf, Serializer.namespaces, const.RDF_DATASET)

		dataset_resources = dataset.findall(const.RDF_DATASET_RESOURCE, namespaces=Serializer.namespaces)
		for dataset_resource in dataset_resources:
			attribute = dataset_resource.attrib[Serializer._transform_attribute(const.RDF_ATTRIBUTE_RESOURCE)]
			resource = rdf.find(
				const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_RESOURCE, attribute=const.RDF_ATTRIBUTE_ABOUT,
												 value=attribute), namespaces=Serializer.namespaces)
			rdf.remove(resource)

		publisher = dataset.find(const.RDF_PUBLISHER, namespaces=Serializer.namespaces)
		publisher_uri = publisher.attrib[Serializer._transform_attribute(const.RDF_ATTRIBUTE_RESOURCE)]
		if Serializer._dataset_publisher_node_appearances(rdf, publisher_uri) == 1:
			publisher = dataset.find(const.RDF_PUBLISHER, namespaces=Serializer.namespaces)
			publisher_uri = publisher.attrib[Serializer._transform_attribute(const.RDF_ATTRIBUTE_RESOURCE)]
			organization = rdf.find(
				const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_ORGANIZATION, attribute=const.RDF_ATTRIBUTE_ABOUT,
												 value=publisher_uri), namespaces=Serializer.namespaces)
			rdf.remove(organization)

		rdf.remove(dataset)

		if remove_from_catalogue:
			catalogue = rdf.find(const.RDF_CATALOGUE, Serializer.namespaces)
			dataset = catalogue.find(const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_CATALOGUE_DATASET,
																	  attribute=const.RDF_ATTRIBUTE_RESOURCE,
																	  value=uri), namespaces=Serializer.namespaces)
			catalogue.remove(dataset)

	@staticmethod
	def _update_catalogue_date(rdf, rdf_template):
		"""
		Updates the modified date of the catalogue to the current one.

		:param ET.Element rdf: Root node of already generated RDF file
		:param ET.Element rdf_template: Root node of RDF template file
		:return: None
		"""
		catalogue = rdf_template.find(const.RDF_CATALOGUE, namespaces=Serializer.namespaces)
		template_modified_node = Serializer._clone_node(catalogue, const.RDF_MODIFIED)

		catalogue = rdf.find(const.RDF_CATALOGUE, namespaces=Serializer.namespaces)
		local_modified_node = catalogue.find(const.RDF_MODIFIED, namespaces=Serializer.namespaces)
		date = Helpers.format_datetime(datetime.utcnow())
		if local_modified_node is not None:
			logging.debug(msg.SERIALIZER_CATALOGUE_DATE_NOT_EXISTS.format(date=date))
			Serializer._set_node_text(local_modified_node, date)
		else:
			logging.debug(msg.SERIALIZER_CATALOGUE_DATE_ALREADY_EXISTS.format(date=date))
			Serializer._set_node_text(template_modified_node, date)
			catalogue.append(template_modified_node)

	@staticmethod
	def _dataset_publisher_node_appearances(rdf, uri):
		"""
		Counts how many times a publisher node from a specific dataset is referenced in entire RDF file.

		:param ET.Element rdf: Root node of already generated RDF file
		:param str uri: URI of the publisher node
		:return: Number of times dataset's publisher node is referenced
		"""
		publisher_attribute_xpath = const.RDF_ATTRIBUTE_XPATH.format(element=const.RDF_PUBLISHER,
																	 attribute=const.RDF_ATTRIBUTE_RESOURCE, value=uri)
		publisher_parent_xpath = const.RDF_ELEMENT_XPATH.format(element=const.RDF_DATASET)

		publishers_xpath = '{element}/{attribute}'.format(element=publisher_parent_xpath,
														  attribute=publisher_attribute_xpath)
		publisher_nodes = rdf.findall(publishers_xpath, namespaces=Serializer.namespaces)

		logging.debug(msg.SERIALIZER_PUBLISHER_NODE_APPEARANCES.format(times=len(publisher_nodes)))
		return len(publisher_nodes)

	@staticmethod
	def _remove_template_nodes(rdf):
		"""
		Removes from the RDF supplied template's original nodes.

		:param ET.Element rdf: Informed template RDF
		:return: None
		"""
		Serializer._remove_node(rdf, const.RDF_CATALOGUE)
		Serializer._remove_node(rdf, const.RDF_DATASET)
		Serializer._remove_node(rdf, const.RDF_RESOURCE)
		Serializer._remove_node(rdf, const.RDF_ORGANIZATION)

	@staticmethod
	def _register_namespaces(namespaces):
		"""
		Registers the namespaces contained in the RDF file in the ElementTree module imported.

		:param dict[str] namespaces: Path to RDF/XML file
		:return: None
		"""
		for namespace in namespaces:
			ET.register_namespace(namespace, namespaces[namespace])

	@staticmethod
	def _get_rdf_namespaces(rdf_file_path):
		"""
		Reads an RDF/XML file and obtains the namespaces present in it.

		:param str rdf_file_path: Path to RDF/XML file
		:return: A dictionary containing the different namespaces
		:rtype: dict[str]
		"""
		try:
			with open(rdf_file_path) as rdf:
				raw_rdf = rdf.read()
		except FileNotFoundError:
			raise RDFFileNotFoundError(rdf_file_path)

		matches = re.findall(r'xmlns:(\w+)=\"([\w./:#-]+)\"', raw_rdf)
		namespaces = {}
		for match in matches:
			namespaces[match[0]] = match[1]
		return namespaces
