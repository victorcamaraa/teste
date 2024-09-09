## Exercicio 1

Transporte = {NavioNome, NavioTipo, ViagemID, Carga, Porto, DataChegada}

### 1
- NavioNome → NavioTipo
- ViagemID → NavioNome, Carga
- NavioNome, DataChegada → ViagemID, Porto

### 2
{NavioNome, DataChegada}  

### 3
Transporte = {DataChegada, ViagemID, Porto}  
Viagem = {ViagemID, NavioNome, Carga}  
Navio = {NavioNome, NavioTipo}


## Exercicio 2

R (A, B, C, D, E, F, G)

  - A, B → C, D, E, F, G
  - E, F → A
  - A → C

**Está na 3º FN**

## Exercicio 3

Dependências Funcionais observáveis:

PecaNum → Descr, Fabric\
PecaNum, Vendor → FabricEnd, Preco, Desconto\
Descr → Fabric\
\
Relação1(PecaNum, Descr)\
Relação2(Descr, Fabric)\
Relação3(PecaNum, Vendor, FabricEnd, Preco, Desconto)\

## Exercicio FNBC
### 1
PropId, {Municipio, LotNum} e {LotNum, Area}\

### 2
Area → Preco viola a 2ª FN\

### 3
Lote = {PropId, Municipio, LotNum, Area, Imposto}\

### 4
Lote = {PropId, Municipio, LotNum, Area, Imposto} pois area não é candidata\

### 5
Preco = {Area, Preco, Municipio}\
Lote = {PropId, LotNum, Area, Imposto}\

### 6
PropId e {LotNum, Area}
