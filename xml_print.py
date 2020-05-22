from sys import stdout


def indent_text(text: str, indent: int = 0) -> str:
    """
    Indent some text by certain levels.
    :param text: the text to be indented (may span over multiple lines).
    :param indent: the level to be indented.
    :return: the indented text as a string.
    """
    result = ''
    indent = int(indent)
    for line in str(text).splitlines():
        result += '%s%s\n' % ('\t' * indent, line)
    return result.rstrip()


def print_indented(text: str, indent: int = 0, file=stdout):
    """
    Print indented text into specified file.
    :param text: the text to be printed.
    :param indent: the indent level.
    :param file: the file DESCRIPTOR for receiving the output.
    """
    print(indent_text(str(text), int(indent)), file=file)


def generate_xml_element(tag: str, content: str or list = None, attrs: dict = None, block=False, indent: int = 0):
    tag = str(tag)
    # do nothing without a valid tag
    if not tag:
        return

    attrs = dict(attrs) if attrs else {}

    def list_attrs():
        list_result = ''
        for (key, val) in attrs.items():
            list_result += ' %s="%s"' % (key, val)
        return list_result.strip()
    attrs_str = list_attrs()

    if not content:
        content = None
        block = False
    elif type(content) is list:
        content = None if len(content) == 0 \
            else '\n'.join([item for item in content if item])
        block = bool(content)
    else:
        content = str(content)
        if not content:
            block = False

    indent = int(indent)

    # handle self-closing tags
    # always create inline output
    if not content:
        result = '<%s %s />' % (tag, attrs_str) if attrs_str \
            else ('<%s />' % tag)
        return indent_text(result, indent)

    # handle normal tags
    else:
        tag_open = '<%s %s>' % (tag, attrs_str) if attrs_str \
            else ('<%s>' % tag)
        tag_close = '</%s>' % tag

        # inline output
        if not block:
            content = ' '.join(content.splitlines()).strip()
            result = '%s%s%s' % (tag_open, content, tag_close)
        # block output
        else:
            content_lines = [line for line in content.splitlines() if line]
            content = '\n'.join(content_lines)
            result = '%s\n%s\n%s' % (tag_open, indent_text(content, indent=1), tag_close)

        return indent_text(result, indent)


def generate_xml_comment(content: str, indent: int = 0):
    """
    Generates an XML comment.
    :param content: the content of the comment
    :param indent: indent level
    :return: the generated comment string with markup.
    """
    content = str(content).strip()
    result = '<!-- %s -->' % content
    return indent_text(result, indent)
