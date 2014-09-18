from itertools import groupby


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


def get_inner_text(node, separator='\n'):
    return separator.join(get_inner_text_lines(node))



def get_inner_text_lines(node):
    text_or_break = [child for child in node.xpath('.//text()|.//br').extract()]
    lines = [
        ''.join(group).strip()
        for k, group in groupby(text_or_break, lambda x: x != '<br>')
        if k
    ]

    return lines
