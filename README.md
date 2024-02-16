# structure-vision

Streamlit application, visualising the structures extracted by [Grobid](https://github.com/kermitt2/grobid) that include PDF coordinates. 

This application allows you to visualise the following components: 
 - authors
 - affiliations
 - title
 - head of sections
 - paragraphs or sentences
 - callout references in text
 - figures
 - formulas
 - bibliographic references

**Demo**: https://structure-vision.streamlit.app/

![screenshot1.png](docs%2Fscreenshot1.png)

This tool was built as a test application for [streamlit-pdf-viewer](https://github.com/lfoppiano/streamlit-pdf-viewer), a new streamlit component for visualising enhanced PDF documents.

## Getting started

```shell
pip install -r requirements
streamlit run streamlit_app.py
```

## Developer notes

**NOTE**: Till [streamlit-pdf-viewer](https://github.com/lfoppiano/streamlit-pdf-viewer) will not be open to the public, install it in the following way (if you don't have access, you can ask me: lucanoro AT duck.com)

```shell
pip install -e git+https://github.com/lfoppiano/streamlit-pdf-viewer 
```
