# Como usar este projeto

## Instalação rápida

Clone o repositório e entre na pasta do projeto:

```bash
git clone github.com/BabiDoo/resume-buddy
cd resume-buddy
```

Crie e ative o ambiente virtual:

```bash
#Criar venv
python -m venv venv

# Ativar venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Configuração da API

* Crie uma chave de API para usar o **Gemini**: [Obter chave](https://aistudio.google.com/app/apikey)
* Adicione a chave no arquivo `.env` com o nome:

```env
LANGEXTRACT_API_KEY=your_api_key_here
```

---

## Preparação dos arquivos

* **Se você tem um arquivo PDF**:

  1. Converta-o para `.txt`
  2. Rode:

     ```bash
     py to_txt.py
     py -X utf8 run_resume_extract.py
     ```

* **Se o arquivo já é `.txt`**:
  Basta rodar:

  ```bash
  py -X utf8 run_resume_extract.py
  ```

---

## Execução

* Aguarde os resultados no terminal (pode levar até **10 minutos**, dependendo do arquivo).
* Os dados gerados serão salvos em um arquivo `.md` contendo o **resumo do arquivo `.txt`**.

---

## Ideia do Projeto

O objetivo principal é que o **agente ajude a criar resumos de anotações e arquivos**, facilitando a organização e revisão dos conteúdos.