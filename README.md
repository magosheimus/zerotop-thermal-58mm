# 🖨️ ZeroTop Thermal 58mm

App desktop minimalista que remove automaticamente a margem superior indesejada, fazendo a impressão começar sempre no topo e evitando desperdício de papel.

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Licença](https://img.shields.io/badge/licença-MIT-orange)

<img width="1009" height="742" alt="image" src="https://github.com/user-attachments/assets/b591aa3b-01e1-4ce7-bbf0-881553872b51" />


## 🎯 Problema 

Impressoras térmicas frequentemente centralizam o conteúdo verticalmente, criando grandes espaços em branco no início da impressão e desperdiçando papel. Este aplicativo detecta e remove automaticamente essas margens, forçando a impressão a começar no topo absoluto do papel.

### Objetivo:
- Eficiência e redução de desperdício
- Simplicidade e controle direto
- Interface leve e funcional

## ✨ Funcionalidades

- **Interface Vintage Windows 95/98**: Design retrô nostálgico
- **Auto Top Fix**: Remove automaticamente margem branca superior
- **Preview em Tempo Real**: Visualize exatamente como ficará a impressão
- **Ajuste de Largura Automático**: Redimensiona para 58mm (384px)
- **Offset Manual**: Controle fino da posição vertical (em mm)
- **Drag & Drop**: Arraste imagens diretamente para o preview
- **Múltiplos Formatos**: Suporte para PNG, JPG, JPEG, BMP
- **Conversão Monocromática**: Otimizado para impressão térmica
- **Múltiplas Cópias**: Imprima várias cópias de uma vez
- **Histórico de Imagens**: Acesso rápido às últimas imagens usadas


## 📋 Requisitos

- Windows 10+
- Python 3.8+
- Impressora térmica 58mm (ESC/POS compatível)
- Driver da impressora instalado

## 🚀 Instalação e Uso


### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/zerotop-thermal-58mm.git
cd zerotop-thermal-58mm
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o aplicativo

```bash
python main.py
```

### 4. (Opcional) Criar executável standalone

Se preferir um arquivo .exe:

```bash
python build_exe.py
```

O executável será criado em `dist/ZeroTop Thermal 58mm.exe`

## Como Usar:

1. Clique em Abrir ou arraste a imagem
2. (Opcional) Ajustar offset / cópias
3. Visualizar preview
4. Imprimir


## 🛠️ Tecnologias Utilizadas

- Python
- Tkinter + TkinterDnD2
- Pillow (imagem)
- pywin32 (impressora)
- PyInstaller (executável)

## 🌱 Autor

Projeto independente desenvolvido a partir de uma necessidade prática no uso diário de impressoras térmicas.

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**


