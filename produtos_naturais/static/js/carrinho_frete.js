const cepInput = document.getElementById("cep");
const freteForm = document.getElementById("frete-form");
const freteResult = document.getElementById("frete-result");

cepInput.addEventListener("input", function () {
    let valor = this.value.replace(/\D/g, '');

    if (valor.length > 5) {
        valor = valor.slice(0, 5) + '-' + valor.slice(5, 8);
    }

    this.value = valor;
});

freteForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const cep = cepInput.value.replace(/\D/g, '');

    fetch(`/loja/calcular-frete/?cep=${cep}`)
        .then(response => response.json())
        .then(data => {
            if (data.valor_frete) {
                freteResult.innerHTML = `
                    <p><strong>Frete:</strong> ${data.valor_frete} (${data.uf})</p>`;
            } else if (data.erro) {
                freteResult.innerHTML = `<p style="color:red;">${data.erro}</p>`;
            }
        })
        .catch(() => {
            freteResult.innerHTML = `<p style="color:red;">Erro ao calcular o frete.</p>`;
        });
});