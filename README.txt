# Instale as dependencias

pip install -r requirements.txt

# Execute com

python -m uvicorn app.main:app

# Existe uma rota de documentação automatica com swagger
http://localhost:8000/docs

# datetime iso format sta no formato:
YYYY-DD-MMThh:mm:ss.mmm. (ano-dia-mesThora-minuto-segundo-milisegundo)

ex:
27 de setembro de 2022 as 18 (6 da noite) -> iso -> 2022-09-27T18:00:00.000.