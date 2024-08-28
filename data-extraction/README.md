Para executar os scripts é aconselhavel criar um ambiente virtual, de forma que os pacotes necessários não interfiram com os pacotes do seu sistema. Para isso:

`python3 -m venv venv`

`source venv/bin/activate`

`pip install --no-deps -r requirements.txt`

`python3 scripts/dengue.py`