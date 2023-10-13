$(document).ready(function () {
  console.log("script!")


  // Função para obter parâmetros da URL
  function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
  }

  // Coletar informações do visitante
  var referenciaCampanha = getParameterByName('utm_source'); // Pode ser personalizado para suas campanhas
    // Exibir informações coletadas no console
  console.log("Referência da Campanha: " + referenciaCampanha);



 async function obterEnderecoIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error("Erro ao obter o endereço IP:", error);
        return null;
    }
}

async function main() {
    const enderecoIP = await obterEnderecoIP();
    return enderecoIP;
}

(async () => {
    const ip = await main();
    console.log("Seu endereço IP é:", ip);
})();








  // Obter localização geográfica do visitante
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      console.log("Latitude: " + latitude + ", Longitude: " + longitude);
    });
  } else {
    console.log("Geolocalização não disponível.");
  }





  // Nome do navegador
  const navegador = navigator.userAgent;

  // Versão do navegador
  const versaoNavegador = navigator.appVersion;

  // Sistema operacional
  const sistemaOperacional = navigator.platform;

  // Tipo de dispositivo (desktop, tablet, mobile)
  const tipoDispositivo = /Mobile|Tablet|iPad|iPhone|iPod|Android/.test(navegador) ? 'Mobile' : 'Desktop';

  console.log("Navegador:", navegador);
  console.log("Versão do Navegador:", versaoNavegador);
  console.log("Sistema Operacional:", sistemaOperacional);
  console.log("Tipo de Dispositivo:", tipoDispositivo);


  const referenciaOrigem = document.referrer || "Direto";

  console.log("Referência de Origem:", referenciaOrigem);

  const idiomaPreferido = navigator.language || navigator.userLanguage;

  console.log("Idioma Preferido:", idiomaPreferido);




})