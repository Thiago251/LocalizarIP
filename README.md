# IP Tracker - Matrix Style 🟢

Localizador de IP robusto com interface gráfica no estilo Matrix, desenvolvido em Python.

## 🚀 Características

- ✅ Interface gráfica estilo Matrix (verde sobre preto)
- ✅ Animações de texto em tempo real
- ✅ Rastreamento do seu IP público ou de um IP específico
- ✅ **6 APIs com sistema de fallback automático** (máxima confiabilidade)
- ✅ Informações detalhadas de geolocalização
- ✅ Exportação de resultados para arquivo TXT
- ✅ Validação robusta de endereços IP
- ✅ Tratamento de erros completo
- ✅ Link direto para Google Maps com coordenadas

## 📋 Requisitos

- Python 3.7 ou superior
- Bibliotecas: `requests`, `tkinter` (já incluído no Python)

## 🔧 Instalação

1. Certifique-se de ter o Python instalado
2. Instale a biblioteca requests:
\`\`\`bash
pip install requests
\`\`\`

## ▶️ Como Usar

Execute o script:
\`\`\`bash
python scripts/ip_tracker_matrix.py
\`\`\`

### Opções:

1. **Rastrear meu IP atual**: Detecta automaticamente seu IP público
2. **Rastrear um IP específico**: Digite o IP que deseja investigar

### Funcionalidades:

- **Iniciar Rastreamento**: Começa o processo de rastreamento
- **Exportar para TXT**: Salva todos os resultados em um arquivo de texto
- **Limpar**: Limpa a tela para um novo rastreamento

## 📊 Informações Fornecidas

- Sistema operacional e informações do computador
- IP público
- Cidade, região e país
- Coordenadas geográficas (latitude/longitude)
- Timezone e UTC offset
- ISP e organização
- ASN (Autonomous System Number)
- CEP/Código Postal
- Moeda e idiomas
- Link direto para Google Maps
- E muito mais!

## 🔒 APIs Utilizadas

O script utiliza **6 APIs diferentes** com sistema de fallback em cascata para garantir máxima confiabilidade:

1. **ipapi.co** - API principal com informações detalhadas (1.000 req/dia)
2. **ipwhois.app** - Fallback secundário (10.000 req/mês)
3. **ipinfo.io** - Terceiro fallback (50.000 req/mês)
4. **freeipapi.com** - Quarto fallback (ilimitado)
5. **ip2location.io** - Quinto fallback (30.000 req/mês)

**Resultado**: Praticamente impossível falhar! Se uma API estiver fora do ar, o sistema automaticamente tenta a próxima.

## 🎨 Estilo Matrix

- Fundo preto (#000000)
- Texto verde Matrix (#00FF00)
- Animações de digitação em tempo real
- Efeitos visuais inspirados no filme Matrix

## 👨‍💻 Desenvolvedor

**Thiago Oliveira**

Versão Python melhorada com interface gráfica

## 📝 Melhorias em Relação à Versão PowerShell

- ✅ Interface gráfica intuitiva
- ✅ Animações visuais
- ✅ Melhor tratamento de erros
- ✅ **6 APIs de fallback robustas** (vs 2 na versão original)
- ✅ Validação robusta de IP
- ✅ Exportação facilitada
- ✅ Multiplataforma (Windows, Linux, macOS)
- ✅ Não bloqueia a interface durante o rastreamento
- ✅ Parsers customizados para cada API
- ✅ Mais informações detalhadas (moeda, idiomas, etc.)
