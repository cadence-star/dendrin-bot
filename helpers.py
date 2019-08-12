from traceback import print_exception
from sys import stderr


async def handle_default(ctx, error):
    print_exception(type(error), error, error.__traceback__, file=stderr)
    await ctx.send(error)
