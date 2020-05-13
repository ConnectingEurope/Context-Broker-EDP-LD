import os

import click

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.core.edp import EDP
from cbld_edp.utils.helpers import Helpers


class CommandsHelpSorter(click.Group):
	def __init__(self, *args, **kwargs):
		self.help_priorities = {}
		super(CommandsHelpSorter, self).__init__(*args, **kwargs)

	def get_help(self, ctx):
		self.list_commands = self.list_commands_for_help
		return super(CommandsHelpSorter, self).get_help(ctx)

	def list_commands_for_help(self, ctx):
		commands = super(CommandsHelpSorter, self).list_commands(ctx)
		return (c[1] for c in sorted(
			(self.help_priorities.get(command, 1), command)
			for command in commands))

	def command(self, *args, **kwargs):
		help_priority = kwargs.pop('help_priority', 1)
		help_priorities = self.help_priorities

		def decorator(f):
			cmd = super(CommandsHelpSorter, self).command(*args, **kwargs)(f)
			help_priorities[cmd.name] = help_priority
			return cmd

		return decorator


class MultiValueCommandOption(click.Option):
	def __init__(self, *args, **kwargs):
		self.save_other_options = kwargs.pop('save_other_options', True)
		nargs = kwargs.pop('nargs', -1)
		assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
		super(MultiValueCommandOption, self).__init__(*args, **kwargs)
		self._previous_parser_process = None
		self._eat_all_parser = None

	def add_to_parser(self, parser, ctx):

		def parser_process(value, state):
			done = False
			value = [value]
			if self.save_other_options:
				while state.rargs and not done:
					for prefix in self._eat_all_parser.prefixes:
						if state.rargs[0].startswith(prefix):
							done = True
					if not done:
						value.append(state.rargs.pop(0))
			else:
				value += state.rargs
				state.rargs[:] = []
			value = tuple(value)

			self._previous_parser_process(value, state)

		retval = super(MultiValueCommandOption, self).add_to_parser(parser, ctx)
		for name in self.opts:
			our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
			if our_parser:
				self._eat_all_parser = our_parser
				self._previous_parser_process = our_parser.process
				our_parser.process = parser_process
				break
		return retval


@click.group(cls=CommandsHelpSorter)
@click.option('--config', '-c', type=click.Path(), default=const.CONFIG_FILE_DEFAULT_PATH,
			  help=msg.COMMANDS_HELP_CONFIG_FILE)
@click.pass_context
def cli(ctx, config):
	"""
	This application integrates the context data of the CEF Context Broker Linked Data version (CB-LD) with the
	European Data Portal (EDP).
	It makes an RDF graph formatted as an XML document from the Data Models specified by the user. For these Data Models
	the integration will create a catalogue, as many datasets as Data Models provided by the command and the
	distributions (resources) based on the configuration file too for each of the previous datasets.

	CBLD-EDP application works with a server that manages the proxy API used for distributions' URLs. This API will
	provide the user with an URL showing the RDF file once it is created.

	This integration is compatible with NGSI-LD specification.

	The available commands allow the user to create a new RDF, update and/or remove existing datasets or add new ones.
	The user can also create the configuration file from scratch.

	Use cbld-edp COMMAND --help for more details about each command.
	"""
	ctx.obj = {'config': config}


@cli.command(name='integrate', help_priority=1)
@click.option('--datamodels', '-d', default=const.DEFAULT_DATAMODEL_OPTION_COMMAND, show_default=True, required=True,
			  help=msg.COMMANDS_HELP_DATAMODELS.format(command='integrate',
			                                           option=const.DEFAULT_DATAMODEL_OPTION_COMMAND),
			  cls=MultiValueCommandOption)
@click.option('--overwrite', '-o', is_flag=True, help=msg.COMMANDS_HELP_OVERWRITE)
@click.pass_context
def integrate(ctx, datamodels, overwrite):
	"""
	Integrates new RDF.

	Integrates the Data Models given as parameters and generates a new RDF/XML file with the resultant datasets and
	distributions.

	If the RDF file already exists, a confirmation will be prompted (ignored in case of adding the --overwrite flag).
	"""
	edp = EDP(ctx.obj['config'])

	if type(datamodels) is str:
		datamodels = (datamodels,)

	if overwrite:
		edp.integrate(datamodels)
	elif os.path.exists(Helpers.get_rdf_path()):
		if click.confirm(msg.COMMANDS_INTEGRATE_PROMPT):
			edp.integrate(datamodels)
	else:
		edp.integrate(datamodels)


@cli.command(name='modify', help_priority=2)
@click.option('--datamodels', '-d', required=True,
			  help=msg.COMMANDS_HELP_DATAMODELS.format(command='modify', option=const.DEFAULT_DATAMODEL_OPTION_COMMAND),
			  cls=MultiValueCommandOption)
@click.pass_context
def modify(ctx, datamodels):
	"""
	Modifies integrated RDF.

	Modifies the previously integrated RDF/XML file adding or updating the Data Models given as parameters.

	The RDF file will be replaced by the new one after the execution.
	"""
	edp = EDP(ctx.obj['config'])
	edp.modify(datamodels)


@cli.command(name='delete', help_priority=3)
@click.option('--datamodels', '-d',
			  help=msg.COMMANDS_HELP_DATAMODELS.format(command='delete', option=const.DEFAULT_DATAMODEL_OPTION_COMMAND),
			  cls=MultiValueCommandOption)
@click.pass_context
def delete(ctx, datamodels):
	"""
	Deletes Data Models from RDF.

	Removes Data Models given as parameters from the already generated RDF/XML file. The Data Model to delete has to be
	integrated before trying to remove it.

	The RDF file will be replaced by the new one after the execution.
	"""
	edp = EDP(ctx.obj['config'])
	edp.delete(datamodels)


@cli.command(name='new_config', help_priority=4)
@click.option('--overwrite', '-o', is_flag=True, help=msg.COMMANDS_HELP_OVERWRITE)
@click.pass_context
def new_config(ctx, overwrite):
	"""
	Creates a configuration file from template.

	It generates an empty configuration file from a template into given path. In case the user does not specify the
	path using --config or -c option, the file will be written in the default location: /etc/cb_edp.ini

	If the configuration file already exists, a confirmation will be prompted (ignored in case of adding --overwrite flag).
	"""
	path = ctx.obj['config']
	if overwrite:
		EDP.generate_config_file(path)
	elif os.path.exists(path):
		if click.confirm(msg.COMMANDS_NEW_CONFIG_PROMPT):
			EDP.generate_config_file(path)
	else:
		EDP.generate_config_file(path)


@cli.command(name='show_integrated', help_priority=5)
def show_integrated_datamodels():
	"""
	Shows already integrated Data Models.

	Prints which are the Data Models present in the RDF/XML. It is necessary to launch the integration at least once to
	get some output here.
	"""
	datamodels = EDP.get_integrated_datamodels()
	if not len(datamodels):
		click.echo(msg.COMMANDS_SHOW_INTEGRATED_DATAMODELS_EMPTY)
	else:
		click.echo(msg.COMMANDS_SHOW_INTEGRATED_DATAMODELS)
		for datamodel in datamodels:
			click.echo('\t' + datamodel)
	click.echo()


if __name__ == '__main__':
	cli(obj={})
