MoinMoin plugin: ListBlogPosts
===============================

ListBlogPosts is a MoinMoin plugin that adds MoinMoin post listing feature in a blog style.

Installation
------------

  1. Copy `ListBlogPosts.py` to your MoinMoin's `data/plugin/action` directory.

Usage
-----

  1. Prepare the top page for your blog.
    * e.g. `/Blog`
  2. Write some blog posts under `BLOG_PATH/YYYY-MM-DD`.
    * e.g. `/Blog/2017-04-01`
  3. Place `<<ListBlogPosts()>>` action on your blog top page.
  4. That's it!

Available macro options:

  * `base_page_name`: specify blog top page name
    (other than which the macro is on.)
  * `omit_posts`: omit posts older than specified value
    (default is 0, which means do not omit posts)
  * `reverse`: reverse result order
        (default is True: newer fist)
  * `include_body`: specify number of lines for which body is included
        (0 means do not include body; bullet style listing)

Copyright and License
---------------------

(C) 2017 WATANABE Takuma <takumaw@sfo.kuramae.ne.jp>

License: GPL v2.
