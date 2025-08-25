# Treina+ - E-commerce de Equipamentos Esportivos

Um e-commerce elegante e moderno para venda de equipamentos esportivos, desenvolvido com Django e Docker.

## 🚀 Funcionalidades

- **Catálogo de Produtos**: Sistema completo de produtos com categorias hierárquicas, marcas e variantes
- **Carrinho de Compras**: Funcionalidade completa de carrinho com persistência
- **Sistema de Usuários**: Registro, login e gerenciamento de contas
- **Checkout**: Processo de finalização com integração de pagamentos
- **Painel Administrativo**: Interface completa para gestão do e-commerce
- **Design Responsivo**: Interface elegante e luxuosa inspirada em grandes varejistas

## 🛠 Tecnologias Utilizadas

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **Processamento Assíncrono**: Celery
- **Containerização**: Docker & Docker Compose
- **Armazenamento**: AWS S3 (opcional)

## 📦 Instalação e Configuração

### Método Simples (Recomendado para desenvolvimento)

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/treinamais.git
cd treinamais
```

2. **Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
```

3. **Instale as dependências essenciais**
```bash
pip install -r requirements_simple.txt
```

4. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver 127.0.0.1:8001
```

5. **Acesse o projeto**
- URL: http://localhost:8001

5. **Acesse a aplicação**
- Site: http://localhost:8000
- Admin: http://localhost:8000/admin (após criar superuser)

### Método Docker (Para produção)

1. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

2. **Construa e inicie os contêineres**
```bash
docker-compose up -d --build
```

## 🏗 Estrutura do Projeto

```
treinamais/
├── apps/
│   ├── accounts/          # Gerenciamento de usuários
│   ├── cart/              # Carrinho de compras
│   ├── core/              # Funcionalidades centrais
│   ├── orders/            # Sistema de pedidos
│   └── products/          # Catálogo de produtos
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos
├── media/                 # Upload de arquivos
├── treinamais/           # Configurações do projeto
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker
└── requirements.txt      # Dependências Python
```

## 🎨 Design e UX

O projeto foi desenvolvido com foco na experiência do usuário, apresentando:

- **Design Luxuoso**: Interface elegante com gradientes e sombras suaves
- **Tipografia Premium**: Combinação de fonts Inter e Playfair Display
- **Animações Fluidas**: Transições suaves e micro-interações
- **Responsividade**: Totalmente adaptado para todos os dispositivos
- **Performance**: Otimizado para carregamento rápido

## 🔧 Comandos Úteis

### Desenvolvimento Local
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Criar migrações (quando implementar os modelos completos)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

### Docker (Produção)
```bash
# Executar testes
docker-compose exec web python manage.py test

# Criar nova migração
docker-compose exec web python manage.py makemigrations

# Executar shell Django
docker-compose exec web python manage.py shell

# Ver logs
docker-compose logs -f web
```

## 🚀 Deploy

### Heroku
```bash
# Configurar Heroku
heroku create treinamais
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### AWS / DigitalOcean
Consulte a documentação específica de cada provedor para deploy com Docker.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Contato

- **Desenvolvedor**: Seu Nome
- **Email**: seu.email@example.com
- **LinkedIn**: [seu-perfil](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- Bootstrap Team pelo framework CSS
- Django Team pelo framework web
- Unsplash pelos recursos visuais
- Comunidade open source pelas bibliotecas utilizadas
