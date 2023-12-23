from bs4 import BeautifulSoup

COLORS = {
    "persName": "rgba(0, 0, 255, 1)",  # Blue
    "s": "rgba(0, 128, 0, 1)",  # Green
    "p": "rgba(0, 100, 0, 1)",  # Dark Green
    "ref": "rgba(255, 255, 0, 1)",  # ??
    "biblStruct": "rgba(139, 0, 0, 1)",  # Dark Red
    "head": "rgba(139, 139, 0, 1)",  # Dark Yellow
    "formula": "rgba(255, 165, 0, 1)",  # Orange
    "figure": "rgba(165, 42, 42, 1)",  # Brown
    "title": "rgba(255, 0, 0, 1)",  # Red
    "affiliation": "rgba(255, 165, 0, 1)"  # red-orengi
}


def get_color(name, param):
    color = COLORS[name] if name in COLORS else "rgba(128, 128, 128, 1.0)"
    if param:
        color = color.replace("1)", "0.4)")

    return color


class GrobidProcessor:
    def __init__(self, grobid_client):
        self.grobid_client = grobid_client

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

        coordinates = self.get_coordinates(text)

        return coordinates

    @staticmethod
    def box_to_dict(box, color=None, type=None):

        item = {"page": box[0], "x": box[1], "y": box[2], "width": box[3], "height": box[4]}
        if color is not None:
            item['color'] = color

        if type:
            item['type'] = type

        return item

    def get_coordinates(self, text):
        soup = BeautifulSoup(text, 'xml')
        all_blocks_with_coordinates = soup.find_all(coords=True)

        # if use_sentences:
        #     all_blocks_with_coordinates = filter(lambda b: b.name != "p", all_blocks_with_coordinates)

        coordinates = []
        count = 0
        for block_id, block in enumerate(all_blocks_with_coordinates):
            for box in filter(lambda c: len(c) > 0 and c[0] != "", block['coords'].split(";")):
                coordinates.append(
                    self.box_to_dict(
                        box.split(","),
                        get_color(block.name, count % 2 == 0),
                        type=block.name
                    ),
                )
            count += 1
        return coordinates
