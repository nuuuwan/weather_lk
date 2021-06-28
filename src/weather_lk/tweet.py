"""Tweet."""


from utils import twitter


def _tweet():
    tweet_text = ''
    status_image_files = None
    profile_image_file = None
    banner_image_file = None

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=status_image_files,
        update_user_profile=True,
        profile_image_file=profile_image_file,
        banner_image_file=banner_image_file,
    )


if __name__ == '__main__':
    _tweet()
