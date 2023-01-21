# ------- API para manejo de alunos de uma academia de Judô usando FastAPI ----- #

# Autor: Gustavo de Oliveira Macedo
# Github: https://github.com/Gustavo-Macedo1
# Versão do projeto: 1.0
# Observação: executar código com webserver uvicorn, conforme orientado na documentação da FastAPI

# -------------------------------------------------------------------------------------------------- #

from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI() #criando objeto de FastAPI

alunos = {
	1: {
		"nome": "Gustavo",
		"idade": 23,
		"graduacao": "Marrom"
	},

	2: {
		"nome": "Bruna",
		"idade": 21,
		"graduacao": "Verde"
	}
}

#Criando classe usando o módulo pydantic com tipos estáticos
class Aluno(BaseModel):
	nome: str	
	idade: int
	graduacao: str

#Criando classe usando o módulo pydantic com tipos opcionais (provenientes da biblioteca Typing)
class AlunoAtualizavel(BaseModel):
	nome: Optional[str]
	idade: Optional[int]
	graduacao: Optional[str]

# ------------- MÉTODOS GET -------------#

@app.get("/")
def index():
	return {"nome", "Primeiro dado"}

@app.get("/get-aluno/{num_aluno}") #mostrando informações do aluno usando Path
def get_aluno(num_aluno: int = Path(None, description="O número do aluno que você quer consultar", gt=0, le=50)):
	return alunos[num_aluno]

@app.get("/get-aluno-by-name") #método query
def get_aluno(*, nome: Optional[str] = None): 
	for aluno in alunos:
		if alunos[aluno]["nome"] == nome:
			return alunos[aluno]
	return {"Info", "Not found"}

@app.get("/get-aluno-by-both/{num_aluno}") #método para juntar query e path:
def get_aluno(*, nome: Optional[str] = None, num_aluno: int = Path(None, description="Número do aluno")): 
	if nome == None:
		return alunos[num_aluno]
	else:
		for aluno in alunos:
				if (alunos[aluno]["nome"] == nome):
					return alunos[aluno]
		return {"Info", "Not found"}

## ------------- MÉTODO POST ---------- ##

#Utilizando a classe com tipos estáticos

@app.post("/criar-aluno/{num_aluno}")
def criar_aluno(num_aluno: int, aluno : Aluno):
	if num_aluno in alunos:
		return {"Erro", f"O aluno {num_aluno} já existe!"}
	else:
		alunos[num_aluno] = aluno
	return alunos[num_aluno]

## ------------- MÉTODO PUT ------------ ##

#Utilizando a classe com tipos opcionais

@app.put("/atualizar-aluno/{num_aluno}")
def update_aluno(num_aluno: int, aluno : AlunoAtualizavel):
	if aluno.nome != None:
		alunos[num_aluno].nome = aluno.nome
	
	if aluno.idade != None:
		alunos[num_aluno].idade = aluno.idade

	if aluno.graduacao != None:
		alunos[num_aluno].graduacao = aluno.graduacao
	
# ------------ MÉTODO DELETE -------------- #

@app.delete("/deletar-aluno/{num_aluno}")
def delete_aluno(num_aluno: int):
	if num_aluno not in alunos:
		return {"Erro":"Esse aluno não existe"}

	del alunos[num_aluno]
	return {"Mensagem":"Aluno deletado com sucesso."}