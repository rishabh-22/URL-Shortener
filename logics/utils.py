from hashlib import blake2s

from django.db import IntegrityError

from logics.models import URLMapping


def generate_hash_for_url(count) -> str:
    """
    this method is used to generate a unique hash based on a counter approach.
    :param count:
    :return:
    """
    h = blake2s(digest_size=4)
    res = bytes(str(count), 'utf-8')
    h.update(res)
    return h.hexdigest()


def store_url_to_db(url):
    """
    this method is used to store the url into the database wrt to uniquely generated hash.
    :param url:
    :return:
    """
    counter = get_db_counter()
    url_hash = 'risha.bh/' + generate_hash_for_url(counter)
    try:
        instance = URLMapping.objects.create(url_hash=url_hash, url=url)
        return {'success': True,
                'message': instance.url_hash}
    except IntegrityError:
        return {'success': False,
                'message': "This url already exists in the database, try fetching the hash for the same."}
    except Exception as e:
        print(e)  # to be replaced with logging in prod
        return {'success': False,
                'message': "Some error occurred, please try again later or contact admin."}


def get_db_counter() -> int:
    """
    this function is used to return a counter integer used to generate a unique hash everytime.
    ***
    when the application is set to scaled, this function here can be replaced with a zookeeper to keep track of
    numerous counters instead of relying on just one which could be a single point of failure.
    ***
    :return: int
    """
    return URLMapping.objects.count()
