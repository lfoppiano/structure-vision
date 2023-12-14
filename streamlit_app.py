import os
from hashlib import blake2b
from tempfile import NamedTemporaryFile

import dotenv
from grobid_client.grobid_client import GrobidClient
from streamlit_pdf_viewer import pdf_viewer

from grobid.grobid_processor import GrobidProcessor

dotenv.load_dotenv(override=True)

import streamlit as st

if 'doc_id' not in st.session_state:
    st.session_state['doc_id'] = None

if 'hash' not in st.session_state:
    st.session_state['hash'] = None

if 'git_rev' not in st.session_state:
    st.session_state['git_rev'] = "unknown"
    if os.path.exists("revision.txt"):
        with open("revision.txt", 'r') as fr:
            from_file = fr.read()
            st.session_state['git_rev'] = from_file if len(from_file) > 0 else "unknown"

if 'uploaded' not in st.session_state:
    st.session_state['uploaded'] = False

if 'binary' not in st.session_state:
    st.session_state['binary'] = None

if 'annotations' not in st.session_state:
    st.session_state['annotations'] = None

st.set_page_config(
    page_title="Grobid structure viewer",
    page_icon="",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/lfoppiano/pdf-struct',
        'Report a bug': "https://github.com/lfoppiano/pdf-struct/issues",
        'About': "View the structures extracted by Grobid."
    }
)


def new_file():
    st.session_state['doc_id'] = None
    st.session_state['uploaded'] = True


@st.cache_resource
def init_grobid():
    grobid_client = GrobidClient(
        grobid_server=os.environ["GROBID_URL"],
        batch_size=1000,
        coordinates=["s", "persName", "biblStruct", "figure", "formula", "head", "note", "title", "ref"],
        sleep_time=5,
        timeout=60,
        check_server=True
    )
    grobid_processor = GrobidProcessor(grobid_client)

    return grobid_processor

init_grobid()

def get_file_hash(fname):
    hash_md5 = blake2b()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


st.title("Document structures visualiser")
st.subheader("Upload a scientific article in PDF, and see the structures that are extracted by grobid .")

uploaded_file = st.file_uploader("Upload an article",
                                 type=("pdf", "txt"),
                                 on_change=new_file,
                                 help="The full-text is extracted using Grobid. ")

with st.sidebar:
    st.header("Documentation")
    st.markdown("https://github.com/lfoppiano/pdfstruct")
    st.markdown(
        """Upload a scientific article as PDF document and see the structures that are extracted by Grobid""")

    if st.session_state['git_rev'] != "unknown":
        st.markdown("**Revision number**: [" + st.session_state[
            'git_rev'] + "](https://github.com/lfoppiano/document-qa/commit/" + st.session_state['git_rev'] + ")")

if uploaded_file:
    with st.spinner('Reading file, calling Grobid...'):
        binary = uploaded_file.getvalue()
        tmp_file = NamedTemporaryFile()
        tmp_file.write(bytearray(binary))
        st.session_state['binary'] = binary
        st.session_state['annotations'] = annotations = init_grobid().process_structure(tmp_file.name)
        pdf_viewer(input=binary, annotations=annotations)
