from pathlib import Path
from typing import Any

from ward import test

import twitter_utils.twitter_page
from mock_browser import mock_browser_session, output_directory
from twitter_utils.tweets_between import parse_args, tweets_between_workflow


@test("Should check if tweets are fetched and written for the given date range")
def test_verify_tweets_written_between_date_range(
    output_directory: str = output_directory(), mock_browser_session: Any = mock_browser_session()
) -> None:
    twitter_utils.twitter_page.DELAY = 0
    parsed_args = parse_args(
        [
            "--account",
            "jack",
            "--since",
            "2020-02-01",
            "--until",
            "2020-02-02",
            "--output-directory",
            ".temp",
        ]
    )
    context = parsed_args.__dict__
    context["browser_session"] = mock_browser_session

    tweets_between_workflow(context)

    assert (
        mock_browser_session.current().url_requested
        == "https://twitter.com/search?q=(from%3Ajack)%20until%3A2020-02-02%20since%3A2020-02-01&src=typed_query"
    )
    files_in_output_folder = Path(output_directory).joinpath("raw-tweets", "jack").glob("*.html")
    assert len(list(files_in_output_folder)) == 1
