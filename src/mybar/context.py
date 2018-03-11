import sys
import attr
import click


@attr.s(init=False)
class Context(object):

    app = attr.ib()
    bar_name = attr.ib()

    def log(self, msg, *args):
        """Log msg to stderr."""
        if args:
            msg = msg.format(*args)
        click.echo(msg, file=sys.stderr)


pass_context = click.make_pass_decorator(Context, ensure=True)
