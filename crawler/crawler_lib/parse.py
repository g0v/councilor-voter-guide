from itertools import groupby
from scrapy.http import HtmlResponse


def remove_whitespaces(string):
    return ''.join(string.split())


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return ''


def get_extracted(xpath):
    return take_first(xpath.extract())


def get_text_nodes(node):
    return node.xpath('.//text()').extract()


def get_inner_text(node, separator='\n', remove_white=False):
    text = separator.join(get_inner_text_lines(node))
    if remove_white:
        text = remove_whitespaces(text)

    return text


def get_inner_text_lines(node):
    text_or_break = [child for child in node.xpath('.//text()|.//br').extract()]
    lines = [
        ''.join(group).strip()
        for k, group in groupby(text_or_break, lambda x: x != '<br>')
        if k
    ]

    return lines


def get_decoded_response(response, encoding, on_decode_error='replace'):
    new_body = response.body.decode(encoding, on_decode_error)
    new_response = HtmlResponse(url=response.url,
                                headers=response.headers,
                                flags=response.flags,
                                request=response.request,
                                body=new_body,
                                encoding='utf8')

    return new_response
