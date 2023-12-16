import re
from collections import OrderedDict
from html import escape
from pathlib import Path

import dateparser
from bs4 import BeautifulSoup


def get_span_start(type, title=None):
    title_ = ' title="' + title + '"' if title is not None else ""
    return '<span class="label ' + type + '"' + title_ + '>'


def get_span_end():
    return '</span>'


def get_rs_start(type):
    return '<rs type="' + type + '">'


def get_rs_end():
    return '</rs>'


def has_space_between_value_and_unit(quantity):
    return quantity['offsetEnd'] < quantity['rawUnit']['offsetStart']


def decorate_text_with_annotations(text, spans, tag="span"):
    """
        Decorate a text using spans, using two style defined by the tag:
            - "span" generated HTML like annotated text
            - "rs" generate XML like annotated text (format SuperMat)
    """
    sorted_spans = list(sorted(spans, key=lambda item: item['offset_start']))
    annotated_text = ""
    start = 0
    for span in sorted_spans:
        type = span['type'].replace("<", "").replace(">", "")
        if 'unit_type' in span and span['unit_type'] is not None:
            type = span['unit_type'].replace(" ", "_")
        annotated_text += escape(text[start: span['offset_start']])
        title = span['quantified'] if 'quantified' in span else None
        annotated_text += get_span_start(type, title) if tag == "span" else get_rs_start(type)
        annotated_text += escape(text[span['offset_start']: span['offset_end']])
        annotated_text += get_span_end() if tag == "span" else get_rs_end()

        start = span['offset_end']
    annotated_text += escape(text[start: len(text)])
    return annotated_text


def get_parsed_value_type(quantity):
    if 'parsedValue' in quantity and 'structure' in quantity['parsedValue']:
        return quantity['parsedValue']['structure']['type']


COLORS = {
    "persName": "blue",
    "s": "green",
    "ref": "red",
    "head": "yellow",
    "formula": "orange",
    "figure": "brown"
}


class GrobidProcessor:
    def __init__(self, grobid_client):
        self.grobid_client = grobid_client

    patterns = [
        r'\d+e\d+'
    ]

    def post_process(self, text):
        output = text.replace('À', '-')
        output = output.replace('¼', '=')
        output = output.replace('þ', '+')
        output = output.replace('Â', 'x')
        output = output.replace('$', '~')
        output = output.replace('−', '-')
        output = output.replace('–', '-')

        for pattern in self.patterns:
            output = re.sub(pattern, lambda match: match.group().replace('e', '-'), output)

        return output

    def process_structure(self, input_path):
        pdf_file, status, text = self.grobid_client.process_pdf("processFulltextDocument",
                                                                input_path,
                                                                consolidate_header=True,
                                                                consolidate_citations=False,
                                                                segment_sentences=True,
                                                                tei_coordinates=True,
                                                                include_raw_citations=False,
                                                                include_raw_affiliations=False,
                                                                generateIDs=True)

        if status != 200:
            return

        output_data = self.parse_grobid_xml(text)

        return output_data

    @staticmethod
    def box_to_dict(box, color=None, type=None):

        item = {"page": box[0], "x": box[1], "y": box[2], "width": box[3], "height": box[4]}
        if color is not None:
            item['color'] = color

        if type:
            item['type'] = type

        return item

    def parse_grobid_xml(self, text):
        soup = BeautifulSoup(text, 'xml')
        all_blocks_with_coordinates = soup.find_all(coords=True)

        coordinates = []
        for paragraph_id, paragraph in enumerate(all_blocks_with_coordinates):
            for box in filter(lambda c: len(c) > 0 and c[0] != "", paragraph['coords'].split(";")):
                coordinates.append(
                    self.box_to_dict(
                        box.split(","),
                        COLORS[paragraph.name] if paragraph.name in COLORS else "grey",
                        type=paragraph.name
                    ),
                )
        return coordinates


def get_children_list_grobid(soup: object, use_paragraphs: object = True, verbose: object = False) -> object:
    children = []

    child_name = "p" if use_paragraphs else "s"
    for child in soup.TEI.children:
        if child.name == 'teiHeader':
            pass
            # children.extend(child.find_all("title", attrs={"level": "a"}, limit=1))
            # children.extend([subchild.find_all(child_name) for subchild in child.find_all("abstract")])
        elif child.name == 'text':
            children.extend([subchild.find_all(child_name) for subchild in child.find_all("body")])
            children.extend([subchild.find_all("figDesc") for subchild in child.find_all("body")])

    if verbose:
        print(str(children))

    return children


def get_children_body(soup: object, verbose: object = False) -> object:
    children = []
    child_name = "s"
    for child in soup.TEI.children:
        if child.name == 'text':
            children.extend([subchild.find_all(child_name) for subchild in child.find_all("body")])

    if verbose:
        print(str(children))

    return children


def get_children_figures(soup: object, use_paragraphs: object = True, verbose: object = False) -> object:
    children = []
    child_name = "p" if use_paragraphs else "s"
    for child in soup.TEI.children:
        if child.name == 'text':
            children.extend([subchild.find_all("figDesc") for subchild in child.find_all("body")])

    if verbose:
        print(str(children))

    return children
