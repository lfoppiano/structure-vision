# structure-vision

**Work in progress**

Streamlit application, visualising the structures extracted by [Grobid](https://github.com/kermitt2/grobid) that include PDF coordinates. 

This application allows to visualise the following components: 
 - paragraphs or sentences
 - head of sections
 - authors
 - bibliographic references
 - callout references in text
 - figures
 - formulas

https://structure-vision.streamlit.app/

![screenshot1.png](docs%2Fscreenshot1.png)

This is just a test application for [streamlit-pdf-viewer](https://github.com/lfoppiano/streamlit-pdf-viewer): a new streamlit component for visualising enhanced PDF documents.

At the moment a [special grobid version](https://github.com/kermitt2/grobid/pull/1068) is required. 

## Getting started

```shell
pip install -r requirements
```

**NOTE
**: Till this component will not be released, install it in the following way (if you don't have access, you can ask me lucanoro AT duck.com)

```shell
pip install -e git+https://github.com/lfoppiano/streamlit-pdf-viewer 
```
