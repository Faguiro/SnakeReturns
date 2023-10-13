let informacoes = {};
informacoes.startTime = new Date();

async function obterEnderecoIP() {
  try {
    const response = await fetch('https://api.ipify.org?format=json');
    const data = await response.json();
    informacoes.enderecoIP = data.ip;
  } catch (error) {
    //console.error("Erro ao obter o endereço IP:", error);
    informacoes.enderecoIP = null;
  }
}

  // Obter localização geográfica do visitante
  function localizacao(){
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {

          var latitude = position.coords.latitude;
          var longitude = position.coords.longitude;
          informacoes.latitude=latitude;
          informacoes.longitude=longitude;


         // console.log("Latitude: " + latitude + ", Longitude: " + longitude);
        });
      } else {
        console.log("Geolocalização não disponível.");
      }
  }


function obterInformacoesNavegador() {
  informacoes.navegador = navigator.userAgent;
  informacoes.versaoNavegador = navigator.appVersion;
  informacoes.sistemaOperacional = navigator.platform;
  informacoes.tipoDispositivo = /Mobile|Tablet|iPad|iPhone|iPod|Android/.test(informacoes.navegador) ? 'Mobile' : 'Desktop';
}

function obterReferenciaOrigem() {
  informacoes.referenciaOrigem = document.referrer || "Direto";
}

function obterIdiomaPreferido() {
  informacoes.idiomaPreferido = navigator.language || navigator.userLanguage;
}

function calcularTempoPermanencia() {
  const endTime = new Date();
  //console.log("startTime:", informacoes.startTime)

  const timeDifference = endTime - informacoes.startTime;
  informacoes.tempoPermanencia = timeDifference / 1000;
}


function setCookie(name, value, days) {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = name + '=' + encodeURIComponent(value) + ';expires=' + expires.toUTCString();
}

document.addEventListener("DOMContentLoaded", function () {


  obterEnderecoIP();
  localizacao();
  obterInformacoesNavegador();
  obterReferenciaOrigem();
  obterIdiomaPreferido();

  //console.log("Informações obtidas até o momento:", informacoes);
  setCookie('informacoes', JSON.stringify(informacoes), 7);
});


setInterval(async function () {

  obterInformacoesNavegador();
  obterEnderecoIP();
  localizacao();
  obterReferenciaOrigem();
  obterIdiomaPreferido();
  calcularTempoPermanencia()
  //console.log("Informações obtidas até o momento:", informacoes);
  setCookie('informacoes', JSON.stringify(informacoes), 7);



const rotaReceberDados = '/receber-dados'; // Atualize a porta conforme necessário
const requestOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(informacoes)
};

try {
    const response = await fetch(rotaReceberDados, requestOptions);
    const data = await response.json();
    //console.log(data.message);
} catch (error) {
    console.error("Erro ao enviar os dados:", error);
}


}, 10000);



 $(document).ready(function () {
		document.getElementById('atualizar-form').addEventListener('submit', async function (event) {
			event.preventDefault();

			const nome = document.getElementById('nome').value;
			const email = document.getElementById('email').value;

			const formData = new FormData();
			formData.append('nome', nome);
			formData.append('email', email);
			formData.append('id', informacoes.enderecoIP);
			console.log(formData);

			try {
				const response = await fetch('/atualizar-nome-email', {
					method: 'POST',
					body: formData
				});

				if (response.ok) {
					alert('Nome e email atualizados com sucesso!');
				} else {
					alert('Erro ao atualizar nome e email.');
				}
			} catch (error) {
				console.error('Erro:', error);
			}
		});
	});



window.addEventListener('beforeunload', async function (event) {
    calcularTempoPermanencia();

    const rotaReceberDados = '/receber-dados'; // Atualize a porta conforme necessário
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(informacoes)
    };

    try {
        const response = await fetch(rotaReceberDados, requestOptions);
        const data = await response.json();
       // console.log(data);
    } catch (error) {
        console.error("Erro ao enviar os dados:", error);
    }

    // Mensagem exibida ao usuário (pode não funcionar em todos os navegadores)
    event.returnValue = 'Seus dados estão sendo enviados. Tem certeza de que deseja sair?';
});