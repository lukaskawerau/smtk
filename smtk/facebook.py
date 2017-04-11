import facepy
from smtk.utils import helpers
import datetime


class CollectFacebook():
    """Sets up a facebook collection.

    Inherit from on_comment, on_post, on_profile, on_reaction, on_start
    to handle stream of data returned by a running collection.
    """

    def __init__(self, auth=None):
        # TODO authentication
        self.auth = helpers.facebook_auth(auth=auth)
        self.graph = facepy.GraphAPI(self.auth)

    def on_comment(self):
        """Called when comment is found"""
        comments = db['comment']
        comment = comments.find_one(comment_id=comment_data['id'])
        today = datetime.datetime.today()

        if not comment:
            fields = [
                'comment_count',
                'created_time',
                'like_count',
                'message'
            ]

            data = {
                'post_id': post_id,
                'comment_id': comment_data['id'],
                'first_scraped': today

            }

            if parent:
                data['parent_id'] = parent

            author_id = None
            if 'from' in comment_data and 'id' in comment_data['from']:
                data['author_id'] = comment_data['from']['id']
                author_id = data['author_id']
                on_profile(db, comment_data['from'])

            for f in fields:
                if f in comment_data:
                    data[f] = comment_data[f]

            comments.insert(data, ensure=True)
        pass

    def on_post(self):
        """Called when post is found"""
        pass

    def on_profile(self):
        """Called when profile is found"""
        pass

    def on_reaction(self):
        """Called when reaction is found"""
        pass

    def on_start(self):
        """Called when collection is started

        Inherit from CollectTwitter class to override to create """
        # verify credentials
        pass

    def get_comments(self, db=None, post_id=None, after=None, parent=None, max_comments=5000):
        """
        Accepts a list of post IDs.
        Calls `on_comment` for each comment returned.
        :param max_comments: the maximum number of comments that should be gathered. Works in reverse chronological order: the newest max_comments comments are downloaded. Default is 5000.
        """
        limit = 100

        kwargs = {
            'path': '/' + str(post_id) + '/comments',
            'limit': limit
        }

        if after:
            kwargs['after'] = after

        try:
            post_data = self.graph.get(**kwargs)
            post_comments = post_data['data']

            for comment in post_comments:
                on_comment(db, comment, post_id, parent=parent)

                if not parent:
                    i += 1
                    if i % 100 == 0:
                        print('Finished ' + str(i) + ' comments')

                    if i > max_comments:
                        return

                if not parent and 'comment_count' in comment and \
                        comment['comment_count'] > 0:
                    get_comments(graph, db, comment['id'], parent=comment['id'])

            if len(post_comments) == limit:
                _after = post_data['paging']['cursors']['after']

                time.sleep(1)
                get_comments(graph, db, post_id, i=i, after=_after, parent=parent)
        except Exception as e:
            print(e)
            pass

        pass

    def get_posts(self, db=None, page_id=None, max_posts=None, date_range=None):
        """
        :param page_id: the Facebook page id from which posts should be downloaded.
        :param max_posts: the maximum number of posts that should be downloaded. Works backwards in time: the newest X number of posts will be returned.
        :param date_range: accepts a tuple of dates. Only posts published between these dates will be downloaded.

        Calls `on_post` for each post returned.
        """
        kwargs = {
            'path': '/' + str(page_id) + '/posts',
            'limit': max_posts,
            'page': True
        }

        post_data_pages = self.graph.get(**kwargs)

        return post_data_pages

        # for post_data in post_data_pages:
        #     posts_data = post_data['data']

        #     for post in posts_data:
        #         print(post)
        # pass

    def get_reactions(self):
        # accept list of post IDs
        # calls on_reaction for each post ID
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_reactions.py
        pass
