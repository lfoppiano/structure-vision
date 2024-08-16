# structure-vision

Streamlit application, visualising the structures extracted by [Grobid](https://github.com/kermitt2/grobid) that include PDF coordinates. 
It uses the Streamlit component [streamlit-pdf-viewer](https://github.com/lfoppiano/streamlit-pdf-viewer) we've been developing. 

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

In addition, the sidebar contains other options, mostly for testing the various 

**Demo**: https://structure-vision.streamlit.app/

![screenshot1.png](docs%2Fscreenshot1.png)

This tool was built as a test application for [streamlit-pdf-viewer](https://github.com/lfoppiano/streamlit-pdf-viewer), a new streamlit component for visualising enhanced PDF documents.

## Getting started

```shell
pip install -r requirements
streamlit run streamlit_app.py
```

## Developer notes

To install the Streamlit PDF viewer via github: 

```shell
pip install -e git+https://github.com/lfoppiano/streamlit-pdf-viewer 
```
