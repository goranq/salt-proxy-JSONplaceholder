# JSONPlaceholder Salt Proxy

This [Salt proxy module](https://docs.saltstack.com/en/master/topics/proxyminion/index.html) can be used to query (dummy) JSON data from [JSONPlaceholder](https://jsonplaceholder.typicode.com). It was created as part of the learning process and it should be treated as such (use it at your own risk).

### Setup

1. Install Salt according to [The Salt install guide](https://docs.saltproject.io/salt/install-guide/en/latest/). For simplicity, it is assumed that Salt master and minion are on the same machine.
2. Copy contents of `srv` folder in this project to `/srv` folder on your Salt machine.

### Usage

- display a blog post:

  ```bash
  sudo salt proxy_blog proxy_blog.show_blog_post <blog_post_id>
  ```

- display a blog post, including its author's name:

  ```bash
  sudo salt proxy_blog proxy_blog.show_blog_post <blog_post_id> author=True
  ```

- display a blog post, including its author's name and all comments that are associated to the post:

  ```bash
  sudo salt proxy_blog proxy_blog.show_blog_post <blog_post_id> author=True comments=True
  ```

Check out `proxy_blog.asiinema`, it shows usage samples in form of [asciinema](https://asciinema.org/) recording.
