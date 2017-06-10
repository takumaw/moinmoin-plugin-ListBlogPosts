# -*- coding: utf-8 -*-
"""
    MoinMoin - ListBlogPosts macro
    @copyright: 2017 WATANABE Takuma <takumaw@sfo.kuramae.ne.jp>
"""

import re

import MoinMoin
import MoinMoin.Page
import MoinMoin.action
import MoinMoin.action.cache
import MoinMoin.caching
import MoinMoin.parser.text_moin_wiki
import MoinMoin.search
import MoinMoin.web.contexts
import MoinMoin.web.request
import MoinMoin.wikiutil

__version__ = "0.1.0"

macro_name = __name__.split('.')[-1]
Dependencies = ["pages"]


def macro_ListBlogPosts(macro, base_page_name, omit_posts,
                        reverse, include_body):
    """
    lists blog posts
    @param base_page_name: base page name for your blog
    @param omit_posts: omit posts older than specified value
        (default is 0, which means do not omit posts)
    @param reverse: reverse result order
        (default is True: newer fist)
    @param include_body: specify True or number of lines from body
        to include in listing
        (default is 0: never includes body; bullet style listing)
    """

    _ = macro._
    request = macro.request

    if not base_page_name:
        base_page_name = request.page.page_name

    # Parse arguments
    if omit_posts:
        try:
            omit_posts = int(omit_posts)
        except ValueError:
            return u"Please specify omit_posts in a number."
    else:
        omit_posts = 0

    if include_body in ["True", "False", None]:
        include_body = True if include_body else False
    else:
        try:
            include_body = int(include_body)
        except ValueError:
            return u"Please specify include_body in a number."

    if reverse in ["True", "False"]:
        reverse = False if reverse == "False" else True
    else:
        reverse = True

    # List blog posts
    blog_post_pages_query = "^%s/[0-9]+-[0-9]+-[0-9]+" % base_page_name
    blog_post_pages_search_results = _get_pages_by_query(
        request, blog_post_pages_query, sort=True, reverse=reverse)
    if omit_posts:
        if reverse:
            blog_post_pages_search_results = blog_post_pages_search_results[
                :omit_posts]
        else:
            blog_post_pages_search_results = blog_post_pages_search_results[
                -omit_posts:]
    else:
        blog_post_pages_search_results = blog_post_pages_search_results[:]

    result = []

    if not include_body:
        result.append(macro.request.formatter.bullet_list(True))
    else:
        # result.append(macro.request.formatter.rule())
        pass

    for blog_post_pages_search_result in blog_post_pages_search_results:
        blog_post_page = MoinMoin.Page.Page(
            request, blog_post_pages_search_result.page_name)

        blog_post_date = blog_post_pages_search_result.page_name.split("/")[-1]

        blog_post_titles = re.findall(
            u"^= (.+) =$", blog_post_page.get_raw_body(), re.MULTILINE)

        if include_body:
            result.append(macro.request.formatter.heading(True, 1))
            result.append(
                macro.request.formatter.url(
                    True,
                    href=blog_post_page.url(macro.request, escape=0))
            )
            result.append(blog_post_date)
            result.append(macro.request.formatter.url(False))
            result.append(macro.request.formatter.heading(False, 1))

            result.append(
                _get_page_as_html(request, blog_post_page, include_body))
        else:
            result.append(macro.request.formatter.listitem(True))
            result.append(
                macro.request.formatter.url(
                    True,
                    href=blog_post_page.url(macro.request, escape=0))
            )
            result.append(blog_post_date)
            result.append(macro.request.formatter.url(False))
            if blog_post_titles:
                result.append(macro.request.formatter.bullet_list(True))
            for blog_post_title in blog_post_titles:
                result.append(macro.request.formatter.listitem(True))
                result.append(blog_post_title)
                result.append(macro.request.formatter.listitem(False))
            if blog_post_titles:
                result.append(macro.request.formatter.bullet_list(False))
            result.append(macro.request.formatter.listitem(False))

    if not include_body:
        result.append(macro.request.formatter.bullet_list(False))
    else:
        # result.append(macro.request.formatter.rule())
        pass

    return u"".join(result)


def _get_pages_by_query(request, query, sort=False, reverse=False):
    query_object = MoinMoin.search.QueryParser(regex=True).parse_query(query)
    search_result = MoinMoin.search.searchPages(request, query_object)
    search_result_hits = search_result.hits

    if sort:
        search_result_hits.sort(key=lambda pg: pg.page_name, reverse=reverse)

    return search_result_hits


def _get_page_as_html(request, page, lines=0):
    page_name = page.page_name
    raw_body = page.get_raw_body()
    pseudo_request = MoinMoin.web.contexts.ScriptContext()
    pseudo_request.formatter.page = MoinMoin.Page.Page(
        pseudo_request, page_name)

    if type(lines) is int:
        raw_body = u"\n".join(raw_body.splitlines()[:lines])
    
    html_body = MoinMoin.wikiutil.renderText(
        pseudo_request, MoinMoin.parser.text_moin_wiki.Parser, raw_body)

    return html_body
