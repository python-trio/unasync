import os

from unasync import Rule

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TEST_DIR = os.path.join(TEST_DIR, "postprocess")
ASYNC_DIR = os.path.join(TEST_DIR, "async")
SYNC_DIR = os.path.join(TEST_DIR, "sync")
TEST_FILES = sorted(f for f in os.listdir(ASYNC_DIR) if f.endswith(".py"))

class PostProcessRule(Rule):

    def _postprocess_tokens(self, tokens):
        # Replace:
        #     asyncio.current_task()
        # with:
        #     current_thread()

        prev2 = None
        prev1 = None

        for token in tokens:

            if (
                prev2 is not None
                and prev2.src == "asyncio"
                and prev1.src == "."
                and token.src == "current_task"
            ):
                yield token._replace(src="current_thread")

                prev2 = None
                prev1 = None

            elif prev2 is not None:
                yield prev2
                prev2 = prev1
                prev1 = token

            else:
                prev2 = prev1
                prev1 = token

        if prev2 is not None:
            yield prev2
        if prev1 is not None:
            yield prev1


def test_postprocess(tmpdir):
    rule = PostProcessRule(fromdir=ASYNC_DIR, todir=str(tmpdir))

    for source_file in TEST_FILES:
        rule._unasync_file(os.path.join(ASYNC_DIR, source_file))

    for source_file in TEST_FILES:
        with open(os.path.join(SYNC_DIR, source_file)) as f:
            truth = f.read()

        with open(os.path.join(str(tmpdir), source_file)) as f:
            unasynced = f.read()

        assert unasynced == truth
