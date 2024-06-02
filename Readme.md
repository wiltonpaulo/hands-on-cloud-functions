# CLOUD SOLUTION ARCHITECT
## Aula Prática: Implementação de controle de requests em lambda utilizando python

Para seguirmos com este processo, a próxima etapa é uma vídeo-aula que você preparará para nós, e nos apresentará ao vivo em uma data e horário que você puder, numa chamada de vídeo. O que acha? Serão 20 minutos de aula prática, pois nosso formato de aula é Hands on, gostaríamos de assistir uma aula sua nesse modelo!

### Parte 1 - Apresentação
+20 Anos de carreira na área de TI  
Graduado em Sistemas de Informação com especializações em Gestão de TI, Engenharia e Arquitetura de Software, Ciência de Dados e Inteligência Artificial.  
Já trabalhei no UOL, HP, Vivo, Oi, Embraer, Banco BV, Bionexo. Para o exterior trabalhei pela Broadwing e atualmente na o9Solutions empresa de IA.

### Parte 2 - O que é uma função lambda?
AWS Lambda é um serviço serverless AWS que permite executar código em resposta a eventos sem gerenciar servidores.  
Você carrega seu código e configura os eventos que disparam sua execução, como:
- Alterações em um bucket S3
- Tabela do DynamoDB
- Solicitações HTTP via API Gateway

Lambda escala automaticamente os recursos necessários e você paga apenas pelo tempo de execução, o que pode reduzir muito os custos.  
Permite a integração com diversos serviços da AWS e suporte a Python, Node.js, Java, e mais.

### Parte 3 - Criar repositório do Git
1. Vá ao [github.com](https://github.com) >> New >> hands-on-cloud-functions
2. Copie o código e configure o email
   ```bash
   git config --global user.email "seuemail"
   ```

### Parte 4 - Setup do Python local
#### Instalar pacote requests
```bash
pyenv install 3.12.3 (Não instalo)
python3 -m venv python
source python/bin/activate
python3 -m pip install requests
```

### Parte 5 - Explicar o conceito de Layers
- [Documentação AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/python-layers.html)
  ```bash
  mkdir layer; cd layer
  mkdir python
  cp -a ../python/lib python
  zip -r python.zip python
  ```

### Parte 6 - Criar código lambda copiando deste git
- [Código de exemplo AWS Lambda](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/layer-python/function)
  ```bash
  mkdir lambda_function; cd lambda_function
  code lambda_function.py
  zip -g function.zip lambda_function.py
  ```

### Parte 7 - Abra o site e vá em lambda
1. Autenticação na AWS
   - [AWS Console](https://wpsbw.signin.aws.amazon.com/console)

2. Crie uma nova layer usando o arquivo que está em `./layers/python.zip`
3. Crie uma nova function e faça upload do arquivo `function.zip`

### Parte 8 - Execute a Função, Teste, Mostre os logs e finalize.

### Parte 9 - Linha de comando aws cli
#### Pegar a role previamente criada:
```bash
aws iam list-roles | jq | grep -i lambda-execution-role
```

#### Criar a layer com o pacote requests
```bash
cd layer
aws lambda publish-layer-version --layer-name python-requests-layer \
    --zip-file fileb://python.zip \
    --compatible-runtimes python3.12 \
    --compatible-architectures "x86_64"
```

#### Criar função com a role
```bash
cd ../lambda_function
aws lambda create-function --function-name python_function_with_layer \
   --runtime python3.12 \
   --architectures "x86_64" \
   --handler lambda_function.lambda_handler \
   --role arn:aws:iam::171292458739:role/lambda-execution-role \
   --zip-file fileb://function.zip
```

#### Atualiza a função com a role
```bash
aws lambda list-layers --query "Layers[*].LayerArn" --output json | jq -r '.[0]'
aws lambda update-function-configuration --function-name python_function_with_layer \
    --cli-binary-format raw-in-base64-out \
    --layers "arn:aws:lambda:us-east-1:171292458739:layer:python-requests-layer:1"
```

#### Invoca a função
```bash
aws lambda invoke --function-name python_function_with_layer \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "key": "value" }' response.json
```

### Código de teste
```python
import json
import requests

def lambda_handler(event, context):
    url = "https://api.pipedream.com/v1/sources/dc_BVuJZL8/event_summaries"
    headers = {
        "Authorization": "Bearer 2f0042ebb922139b5b7d3cda4539b5ae"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'error': 'Failed to retrieve data'})
        }
```

#### Atualiza a function
```bash
cd ../lambda_function
aws lambda update-function-code --function-name python_function_with_layer \
   --zip-file fileb://function.zip
```