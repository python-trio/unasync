# fmt: off
async def dummy():
	await dummy2()  # This line is indented with a tab that should be preserved
# fmt: on


async def dummy2():
    await dummy()  # This one uses 4 spaces and these should also be preserved
