import sys
import attr
import click


@attr.s(init=False)
class Context(object):

    env = attr.ib()
    verbose = attr.ib()
    app = attr.ib()
    bar_id = attr.ib()

    def log(self, msg, *args):
        """Log msg to stderr."""
        if args:
            msg = msg.format(*args)
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Log msg to stderr if verbose mode enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
