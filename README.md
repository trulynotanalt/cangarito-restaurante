## Version 1.1

#### Proposta
O projeto Cangarito propõe uma aplicação web para um
restaurante nordestino chamado “Cangarito” que permite aos seus
clientes pedirem os pratos do restaurante de maneira não presencial a
partir de um sistema de cadastro e login dos clientes, separando os
pedidos e históricos por cada usuário. Além disso, a aplicação também
permite exibir informações sobre o restaurante e eventos que ocorrem
nele.

#### O que foi feito:
- Estruturação de entidades no Banco de Dados com SQLALchemy
- CRUD completo das entidades necessárias
- Adição do Flask-Login para autenticação e proteção de rotas
- Implementação de Hash de Senhas em todo o projeto

#### Problema

Durante o desenvolvimento do projeto, identificamos a
necessidade de reestruturar a forma como os dados eram armazenados
e como as operações de CRUD eram implementadas. A solução
utilizada no início era baseada apenas na biblioteca sqlite3 o que
dificultava a manutenção do código e o gerenciamento das entidades.
Além disso, a aplicação ainda não utilizava strings de consulta para o
envio de parâmetros nas requisições HTTP de pesquisa, requisito
necessário para atender às especificações do projeto.

#### Justificativa

Como proposta do nosso professor de implementar SQLAlchemy
para o CRUD do nosso projeto, decidimos estruturar o nosso banco de
dados que antes funcionava apenas com sqlite3 e passamos a utilizar
essa nova biblioteca como ORM. Além disso, nós necessitavamos
utilizar também strings de consulta.

### Integrantes:

#### Pedro Henrique Medeiros dos Santos

Responsável por fazer o CRUD das entidades com o Banco de
Dados por meio do SQL Alchemy. Além disso, realizou a criação dessas
entidades como classes.

#### Jeizon Gomes da Silva Filho
Implementou flask-login nas rotas necessárias e também
implementou protegeu as rotas que eram necessárias. Implementou, também, hash de senhas para segurança.

#### João Victor Noberto Tomaz Santana
Implementou as strings de consulta e realizou a junção de
commits e correção de bugs entre os códigos dos demais integrantes.

#### JOAO PEDRO DE OLIVEIRA SILVA
Realizou o commit de release e os organizou.
