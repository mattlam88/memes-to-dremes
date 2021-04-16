from datetime import datetime
from typing import Any, Dict, List, Tuple

import tweepy as tp


class TwitterChannel:
    """
    Class is used to fetch historic twitter feed data
    """

    # region Properties

    @property
    def api(self):
        return self._api

    # endregion

    # region Constructor

    def __init__(self, api):
        self._api = api

    # endregion

    def get_user_info(self, twitter_handle: str) -> Tuple[str, str, str]:
        """
        Given a twitter handle, returns additional information about the twitter account holder.

        :param twitter_handle: The account's twitter handle.
        :return: The account's unique id, name, and screen name.
        """

        user = self.api.get_user(twitter_handle)

        return user.id_str, user.name, user.screen_name

    def get_user_tweets(self, username: str, start_date: datetime) -> List[Dict[str, Any]]:
        tweets: List[Dict[str, Any]] = list()

        for status in tp.Cursor(self.api.user_timeline, id=username, include_retweets=False).items():

            if status.created_at > start_date:
                if status.in_reply_to_status_id is None:
                    tweets.append(status._json)
                elif status.in_reply_to_screen_name == username and status.user.screen_name == username:
                    tweets.append(status._json)
            else:
                break

        return tweets
