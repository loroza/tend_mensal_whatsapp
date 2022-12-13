Olá tudo bom?

Este projeto tem como seu principal objetivo reportar a venda em grupos do Whatsapp. Com os códigos em python ele consegue criar um visual, em que os integrantes do grupo consigam ter acesso fácil aos seguintes atributos:

- Meta de venda
- Venda bruta
- Venda líquida
- Devolução
- % de devolução
- Venda para pessoa jurídica
- Quantidade de clientes de pessoa jurídica
- % de devolução da pessoa jurídica
- Venda para pessoa física
- Quantidade de clientes de pessoa física
- % de devolução da pessoa física
- % da venda em relação a meta diária
- % da venda em relação a meta mensal
- Projeção para o fim do mês


<div aling="center">
<img src="https://user-images.githubusercontent.com/115322315/207349282-11b40df8-c954-4df4-837f-226f8eafb0c9.png" />
</div>


Cada coluna contida na imagem acima é calculada da seguinte forma:

⇨ Meta de venda [Meta]:

    A meta de venda é composta pela meta mensal diluída em seus respectivos dias durante o mês.
    Sendo assim:
        Meta de sábado ⇨ Meta de sábado * Quantidade de sábados do mês
            ⮱ É atrelada aos sábados do mês.

        Meta diária ⇨ ( Meta mensal - Meta de sábado ) / Quantidade de dias úteis do mês
            ⮱ É atrelada aos dias úteis do mês.

    Obs.:
        Dias proporcionais ⇨ Existem algumas anomalias que podem afetar a venda em geral, com isso, pode ser
        que ocorra o fracionamento da meta daquele dia.
            Exemplo:

            A meta diária é R$ 1.000.000,00.
            No dia 21/07/2026 teve uma partida do Brasil em uma disputa de Copa do Mundo.
            O comercial reuniu-se e resolver aplicar uma meta proporcional a 70% da meta diária nesse dia.
            Desta forma a meta daquele dia passa de R$ 1.000.000,00 para R$ 700.000,00.


⇨ Venda bruta [Venda SIAC]:

    A venda bruta é calculada mediante uma série de filtros necessários para trazer um número de venda mais
    real possível. Sendo assim, nesse número não poderá estar contido as requisições, pedidos para
    uso interno, pedidos de transferência, pedidos de teste e/ou pedidos de devolução.


⇨ Venda líquida [Venda Líquida]:

    A venda líquida é calculada mediante o número de venda bruta e devolução.
        Venda líquida ⇨ Venda SIAC - Devolução


⇨ Devolução [Devolução]:

    A devolução também é calculada mediante uma série de filtros para eliminar outras situações calculadas com
    a mesma base de dados. Portanto, deverá ser desconsiderado as notas denegadas, notas de transferência,
    notas de teste, notas de devolução, notas canceladas e/ou notas com naturezas específicas.


⇨ % de devolução [% Dev]:

    A taxa de devolução se trata de uma coluna calculada mediante o número de devolução e venda bruta.
        % de devolução ⇨ Devolução / Venda SIAC