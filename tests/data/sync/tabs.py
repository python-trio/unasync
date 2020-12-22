# fmt: off
def dummy():
	dummy2()  # This line is indented with a tab that should be preserved
# fmt: on


def dummy2():
    dummy()  # This one uses 4 spaces and these should also be preserved
