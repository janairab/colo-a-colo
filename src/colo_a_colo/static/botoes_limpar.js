/* Obtém todos os botões de limpar */
const botoesLimpar = document.querySelectorAll("[data-limpar]");

/* Percorre os botões para configurar a limpeza */
botoesLimpar.forEach(function(botao) {

    /* Executa a limpeza quando o botão é clicado */
    botao.addEventListener("click", function() {

        /* Obtém o identificador do campo correspondente */
        const identificador = botao.dataset.limpar;

        /* Localiza o campo que será limpo */
        const campo = document.getElementById(identificador);

        /* Verifica se o campo foi encontrado */
        if (campo) {

            /* Apaga o conteúdo do campo */
            campo.value = "";

            /* Atualiza os eventos do campo */
            campo.dispatchEvent(new Event("input", { bubbles: true }));
            campo.dispatchEvent(new Event("change", { bubbles: true }));
        }
    });
});
