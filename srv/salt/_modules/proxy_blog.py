# Execution module - put in /srv/salt/_modules

def show_blog_post(blog_post_id, author=False, comments=False):
    return __proxy__['proxy_blog.show_blog_post'](blog_post_id, author, comments)
