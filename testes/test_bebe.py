from colo_a_colo.domain.bebe import Bebe

# Teste com mais anos
bebe1 = Bebe("João", "Masculino", "2015-10-02")

# Teste com o mês com 31 dias
bebe2 = Bebe("Hope", "Feminino", "2024-01-31")

bebe3 = Bebe("Matias", "Masculino", "2026-03-25")

# Mostrar a idade
print(bebe1.calcular_idade())
print(bebe2.calcular_idade())
print(bebe3.calcular_idade())

# Mostrar os dados do bebé
print(bebe1)
print(bebe2)
print(bebe3)