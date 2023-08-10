# Proxy module - put in /srv/salt/_proxy

import salt.utils.http


__proxyenabled__ = ["proxy_blog"]


GRAINS_CACHE = {}
DETAILS = {}


def __virtual__() -> bool:
    """
    Mandatory function which holds logic to determine if the module can be
    loaded. No special requirements in this case.

    return: bool
    """

    return True


def init(opts) -> None:
    """
    Mandatory function. Every proxy module needs an 'init', though just
    DETAILS['initialized'] = True is sufficient if nothing else needs to be
    done.

    param opts: Salt's opts dictionary
    return: None
    """

    # Pull the URL from pillar
    DETAILS["url"] = opts["proxy"]["url"]

    # Make sure the URL ends with a '/'
    if not DETAILS["url"].endswith("/"):
        DETAILS["url"] += "/"

    DETAILS["initialized"] = True


def initialized() -> bool:
    """
    Since grains are loaded in many different places and some of those
    places occur before the proxy can be initialized, return whether
    init() function has been called.

    return: bool
    """

    return DETAILS.get("initialized", False)


def alive(opts) -> bool:
    """
    This function returns a flag with the connection state.
    It is very useful when the proxy minion establishes the communication
    via a channel that requires a more elaborated keep-alive mechanism, e.g.
    NETCONF over SSH.

    param opts: Salt's opts dictionary
    return: bool
    """

    return True


def grains() -> dict:
    """
    Get the grains from the proxied device. In this case, grain values are
    mocked.

    return: dict
    """

    if not DETAILS.get("grains_cache", {}):
        DETAILS["grains_cache"] = {'os': 'MostProbablyLinux',
                                   'kernel': '0.0000001',
                                   'osversion': '0.01'}
    return DETAILS["grains_cache"]


def grains_refresh() -> dict:
    """
    Refresh the grains from the proxied device.

    return: dict
    """

    DETAILS["grains_cache"] = None
    return grains()


def ping() -> bool:
    """
    Checks if the server is up.

    return: bool
    """

    r = salt.utils.http.query(
        DETAILS["url"] + "posts/1",
        status=True,
        decode_type="json",
        decode=True
        )
    try:
        if r["status"] == 200:
            return True
        else:
            return False
    except Exception:
        return False


def shutdown() -> None:
    """
    Mandatory function which does a clean shut down or closes a connection to
    a controlled device. No specific requirements in this case.

    return: None
    """

    pass


def _get_blog_post(blog_post_id: int = 1) -> dict:
    """
    Get entire blog post, specified by an blog post ID. If no ID value is
    supplied, ID = 1 is assumed.

    param blog_post_id: ID of blog post, default 1
    return: dict
    """

    r = salt.utils.http.query(
        DETAILS["url"] + "posts/" + str(blog_post_id),
        decode_type="json",
        decode=True
        )
    return r["dict"]


def _get_comments(post_id: int) -> dict:
    """
    Get all the comments for a blog post having specified ID value.

    param post_id: ID of blog post
    return: dict
    """

    r = salt.utils.http.query(
        DETAILS["url"] + "posts/" + str(post_id) + "/comments",
        decode_type="json",
        decode=True)
    return r["dict"]


def _get_author_info(author_id: int) -> dict:
    """
    Get information about the author of a blog post having specified ID value.

    param author_id: ID of author
    return: dict
    """

    r = salt.utils.http.query(
        DETAILS["url"] + "users/" + str(author_id),
        decode_type="json",
        decode=True
        )
    return r["dict"]


def show_blog_post(
        blog_post_id: int,
        author: bool = False,
        comments: bool = False
        ) -> dict:
    """
    Build the requested blog post output. Only blog post is shown by default,
    but author info and comments can be included by setting value of
    appropriate function parameters to True.

    param blog_post_id: ID of blog post
    param author: optionally show author info
    param comments: optionally show comments
    return: dict
    """

    output = dict()

    blog_post = _get_blog_post(blog_post_id)
    output["post_id"] = blog_post["id"]
    output["post_title"] = blog_post["title"]
    output["post_text"] = blog_post["body"]

    # Include author info
    if (author):
        author_info = _get_author_info(blog_post["userId"])
        output["author_name"] = author_info["name"]

    # Include comments
    if (comments):
        comms = _get_comments(blog_post["id"])
        output["comments"] = []

        for comm in comms:
            comment = {
                "comment_id": comm["id"],
                "comment_email": comm["email"],
                "comment_title": comm["name"],
                "comment_body": comm["body"]
            }
            output["comments"].append(comment)

    return output
