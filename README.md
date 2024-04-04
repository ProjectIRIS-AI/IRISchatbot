# IRIS ChatBot

## Overview
She will learn from user inputs and responses with the closes match in her [knowledge base](https://github.com/ProjectIRIS-AI/Knowledgebase/). She finds the closes match using [difflib](https://docs.python.org/3/library/difflib.html/) and replies with them. The user will be prompted to teach her a response if no close match is found. She will then store her newly learned response in her [knowledge base](https://github.com/ProjectIRIS-AI/Knowledgebase/).

## Tools Utilised
- [Python](https://www.python.org/) (Built on Python 3.11.8)
- [difflib](https://docs.python.org/3/library/difflib.html/)
- [JSON](https://www.json.org/)
<br><br>
- [pyttsx3](https://pypi.org/project/pyttsx3/)

## File Structure
In order for her to work correctly, the file structure should be as shown below.
```
Root
├── IRISchatbot
│   └── main.py
└── Knowledgebase
    ├── Alpha.json
    └── Beta.json
```
For knowledge bases, visit [this repository](https://github.com/ProjectIRIS-AI/Knowledgebase).

## Test Files
```
Root
└── IRISchatbot
    ├── main.py
    └── test
        ├──typewritter.py
        └── texttospeech.py
```
#
28 March 2024

N34R
#