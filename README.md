# Arquitetura De Computadores
## Trabalho da diciplina SSC0114-Arquitetura De Computadores
Implementação de um simulador do algoritmo de Tomasulo
### Pré Requisitos
Instalação da biblioteca [wkPython](https://wxpython.org/)
### Formatação do Arquivo de Entrada
O formato do arquivo de entrada deve seguir o padrão, na primeira linha o número de unidades funcionais desejadas. Nas linhas consecutivas o nome da unidade funcional seguido das operações que a unidade funcional processa seguido de suas latências, os elementos devem ser separados por ponto e vírgula e as latências separadas por vírgula conforme o exemplo: Nome Da Unidade;Operação 1,Latência Da Operação 1;Operação 2,Latência Da Operação 2; etc. Observa-se que para cada unidade funcional deve-se definir as Operações e as latências, sendo possível que unidades diferentes tenham latências diferentes para operações diferentes. Todas as latências devem ser números inteiros maiores do que zero. Não deve-se colocar ponto e vírgula no final da linha.
Após as unidades funcionais deve-se colocar o código a ser simulado, com uma instrução por linha. Os registradores utilizados são identificados por uma letra seguida de um número, para os registradores inteiros utilizou-se a letra r e para os registradores de ponto flutuante utilizou-se a letra d. Todos os registradores são inicializados com os valores que os identificam vezes o valor 10, assim como as posições de memória são inicializadas com os respectivos endereços. Linhas a mais no final do arquivo serão interpretadas como instruções, e poderão gerar o não reconhecimento do arquivo. O formato do arquivo não é sensível a letras maiúsculas e minúsculas.
    As seguintes instruções e operações foram definidas:
add: operação de soma dos dois registradores inteiros passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: add,r1,r2,r3
add.d: operação de soma dos dois registradores de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: add.d,d1,d2,d3
addi: operação de soma do registrador e do valor imediato inteiro passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: addi,r1,r2,Imediato
addi.d: operação de soma do registrador e do valor imediato de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: addi.d,d1,d2,Imediato
sub: operação de subtração dos dois registradores inteiros passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: sub,r1,r2,r3
sub.d: operação de subtração dos dois registradores de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: sub.d,d1,d2,d3
subi: operação de subtração do registrador e do valor imediato inteiro passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: subi,r1,r2,Imediato
subi.d: operação de subtração do registrador e do valor imediato de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: subi.d,d1,d2,Imediato
mult: operação de multiplicação dos dois registradores inteiros passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: mult,r1,r2,r3
mult.d: operação de multiplicação dos dois registradores de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: mult.d,d1,d2,d3
multi: operação de multiplicação do registrador e do valor imediato inteiro passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: multi,r1,r2,Imediato
multi.d: operação de multiplicação do registrador e do valor imediato de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: multi.d,d1,d2,Imediato
div: operação de divisão dos dois registradores inteiros passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: div,r1,r2,r3
div.d: operação de divisão dos dois registradores de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: div.d,d1,d2,d3
divi: operação de divisão do registrador e do valor imediato inteiro passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: divi,r1,r2,Imediato
divi.d: operação de divisão do registrador e do valor imediato de ponto flutuante passados por último, armazenando o resultado no primeiro registrador passado. Formato da instrução: divi.d,d1,d2,Imediato
lw: operação de load de um valor inteiro da memória, armazenando-o no primeiro registrador passado, o conteúdo da memória no endereço contido no último registrador passado incrementado do valor imediato passado. Formato da instrução: lw,r1,Imediato,r2
ld.d: operação de load de um valor de ponto flutuante da memória, armazenando-o no primeiro registrador passado, o conteúdo da memória no endereço contido no último registrador passado incrementado do valor imediato passado. Formato da instrução: ld.d,d1,Imediato,r2
sw: operação de store de um valor inteiro na memória, armazenando o conteúdo do primeiro registrador passado, no endereço contido no último registrador passado incrementado do valor imediato passado. Formato da instrução: sw,r1,Imediato,r2
sd.d: operação de store de um valor de ponto flutuante na memória, armazenando o conteúdo do primeiro registrador passado, no endereço contido no último registrador passado incrementado do valor imediato passado. Formato da instrução: sd.d,d1,Imediato,r2
    Para as operações de load e store o registrador com o endereço da instrução deve ser inteiro. Para todas as demais operações não pode-se misturar registradores inteiros com registradores de ponto flutuante.
