# Guia de Resolução de Problemas - Treina+

## ❌ Problemas Comuns e Soluções

### 1. Erro de Redis Connection
```
ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.
```
**Solução**: O projeto foi simplificado para não usar Redis em desenvolvimento. Use a versão local:
```bash
source venv/bin/activate
python manage.py runserver
```

### 2. Erro "Address already in use"
```
ERROR: for redis Cannot start service redis: failed to bind host port
```
**Solução**: Pare todos os containers e use a versão local:
```bash
docker-compose down
source venv/bin/activate  
python manage.py runserver
```

### 3. Problemas com Docker
Se houver conflitos de porta ou problemas com Docker:
```bash
# Parar todos os containers
docker-compose down

# Remover containers órfãos
docker system prune -a

# Use a versão local em vez do Docker
python -m venv venv
source venv/bin/activate
pip install -r requirements_simple.txt
python manage.py runserver
```

### 4. Erro de ImportError com dependências
Se houver erros com bibliotecas como `django-redis`, `mptt`, etc:
```bash
# Use o requirements simplificado
pip install -r requirements_simple.txt
```

### 5. Problemas com Migrações
```bash
# Remover banco atual e recriar
rm -f db.sqlite3

# Recriar migrações (quando implementar modelos completos)
python manage.py makemigrations
python manage.py migrate
```

## ✅ Configuração Funcionando

**Status Atual**: O projeto está funcionando com:
- ✅ Django 4.2.7
- ✅ SQLite (desenvolvimento)
- ✅ Interface elegante e responsiva
- ✅ Templates base implementados
- ✅ Estrutura de apps modularizada

**Para executar**:
```bash
cd "/home/geovani/Documentos/Gigio/Treina+"
source venv/bin/activate
python manage.py runserver 127.0.0.1:8001
```

**Acesse**: http://localhost:8001

## 🚀 Próximos Passos

1. Implementar modelos completos
2. Criar migrações
3. Adicionar funcionalidades do carrinho
4. Implementar sistema de usuários
5. Adicionar produtos reais

## 💡 Dicas

- Para desenvolvimento, use sempre a versão local (sem Docker)
- Docker é recomendado apenas para produção
- O projeto foi simplificado para máxima compatibilidade
- Todas as dependências complexas foram removidas temporariamente
