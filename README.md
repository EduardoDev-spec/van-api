# 🚐 App Van

Sistema desenvolvido para facilitar o gerenciamento de transporte universitário por van, centralizando o cadastro de alunos, controle de presença e pagamentos em um único aplicativo.

## 📌 Sobre o projeto

O **App Van** surgiu com o objetivo de substituir processos manuais realizados atualmente pelo responsável pela van, como:

- Controle de quais alunos irão utilizar a van em determinado dia;
- Controle de pagamentos;
- Confirmação de pagamentos através de comprovantes;
- Gerenciamento de novos alunos;
- Controle de alunos ativos e pendentes.

A proposta é permitir que o aluno realize essas operações diretamente pelo aplicativo, enquanto o responsável pela van possui um painel administrativo para acompanhar todas as informações.

---

# 🎯 Objetivos

### Para os alunos

- Criar uma conta;
- Aguardar a aprovação do responsável pela van;
- Informar se utilizará a van em determinado dia;
- Consultar sua situação;
- Visualizar mensalidades;
- Realizar pagamentos;
- Consultar histórico de pagamentos e presença.

### Para o administrador

- Gerenciar alunos;
- Aprovar novos cadastros;
- Bloquear ou remover alunos;
- Visualizar quem utilizará a van no dia;
- Acompanhar pagamentos;
- Visualizar pagamentos pendentes e atrasados;
- Consultar históricos;
- Configurar informações da van.

---

# 🏗️ Arquitetura

O projeto será dividido principalmente em:

```text
App Van
│
├── Backend
│   ├── API
│   ├── Banco de dados
│   ├── Autenticação
│   ├── Regras de negócio
│   └── Integração de pagamentos
│
├── Aplicativo do aluno
│
└── Painel administrativo