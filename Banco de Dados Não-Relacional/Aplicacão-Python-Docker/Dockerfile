# Multi-stage Dockerfile para Gerador de Referências

FROM python:3.11-slim AS builder

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências em uma camada separada
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage final
FROM python:3.11-slim

WORKDIR /app

# Copiar apenas o necessário da stage builder
COPY --from=builder /root/.local /root/.local

# Copiar aplicação
COPY reference_generator.py .
COPY app.py .
COPY templates/ templates/

# Definir PATH para usar binários do usuário
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py

# Criar diretório para outputs
RUN mkdir -p /app/outputs

# Expor porta
EXPOSE 5000

# Comando padrão
CMD ["python", "app.py"]
