"""
Boot script para ESP32 - Configuração inicial
"""
# Este arquivo é executado uma vez na inicialização do ESP32

import gc
import webrepl

# Habilita coleta de lixo automática
gc.enable()

# Inicializa o WebREPL (descomentado para facilitar o desenvolvimento)
# webrepl.start()

print("Boot script executado com sucesso")