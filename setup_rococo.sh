#!/bin/bash
# Rococo Testnet Configuration Script
# Este script configura el acceso a Rococo testnet

echo "🔧 Configurando Rococo Testnet Access..."
echo ""

# 1. Verificar que se tiene nodejs (necesario para polkadot.js)
echo "1️⃣  Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js no encontrado. Necesario para polkadot.js"
    echo "   Instalar: brew install node"
else
    echo "✅ Node.js: $(node --version)"
fi

echo ""

# 2. Información sobre Rococo
echo "2️⃣  Rococo Testnet Info:"
echo "   RPC: wss://rococo-contracts-rpc.polkadot.io"
echo "   Chain: Rococo (Polkadot Testnet)"
echo "   Type: Contracts (WASM Smart Contracts)"
echo ""

# 3. Faucet
echo "3️⃣  ROC Token Faucet:"
echo "   URL: https://faucet.polkadot.io"
echo "   Steps:"
echo "   1. Go to https://faucet.polkadot.io"
echo "   2. Select 'Rococo' from dropdown"
echo "   3. Paste your address (starts with '1...')"
echo "   4. Click 'Claim'"
echo "   5. Wait ~1 min for tokens"
echo ""

# 4. Python packages
echo "4️⃣  Instalando paquetes Python necesarios..."
pip list | grep -q "substrate-interface" || echo "   py-substrate-interface: No instalado"
pip list | grep -q "polkadot" || echo "   polkadot-py: No instalado"

echo ""
echo "✅ Configuración completada"
echo ""
echo "Próximos pasos:"
echo "1. Obtener ROC tokens del faucet (arriba)"
echo "2. Instalar pip packages: pip install py-substrate-interface"
echo "3. Actualizar escrow.py con función deploy_to_rococo()"
echo ""
