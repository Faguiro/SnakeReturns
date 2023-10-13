// Data: 18/12/2022
//Fabiano Guimarães da Rocha
// Aplicação com JavaScript puro: Como desenvolver uma pokedex
//https://www.linkedin.com/in/faguiro/

$(document).ready(function(){let e=e=>`https://pokeapi.co/api/v2/pokemon/${e}`,t=e=>e.reduce((e,{name:t,id:s,types:l})=>{let a=l.map(e=>e.type.name);return e+`<li class="card  ${a[0]} hide">
      <h2 class="card-title">${s}.${t}</h2>
      <img class="card-image" alt="${t}"
      src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${s}.png">
      <p class="card-subtitle">${a.join(" | ")}</p><div class="sharethis-inline-reaction-buttons"></div>
      </li>`},""),s=e=>{let t=document.querySelector("[data-js='pokedex']");t.innerHTML=e},l=Array(150).fill().map((t,s)=>fetch(e(s+1)).then(e=>e.json()));Promise.all(l).then(t).then(s);let a=document.querySelector(".form-control");document.querySelector(".sugestoes"),a.addEventListener("keydown",({target:e})=>{let t=e.value;t.length&&function e(t){let s=[],l=document.getElementsByClassName("card-title");for(i=0;i<l.length;i++)l[i].innerHTML.toLowerCase().includes(t.toLowerCase())?(s.push(l[i].innerHTML),$(l[i]).parent().removeClass("hide")):$(l[i]).parent().addClass("hide");return console.log(s),s.filter(e=>{let s=e.toLowerCase(),l=t.toLowerCase();return s.includes(l)})}(t)}),$(".button-all").click(function(e){"Todos"===$(this).text()?$(this).text("Limpar"):$(this).text("Todos");let t=document.querySelectorAll(".card");console.log(t.length),e.preventDefault();for(let s=0;s<t.length;s++)t[s].classList.contains("active")?(t[s].classList.remove("active"),t[s].classList.add("hide")):(t[s].classList.add("active"),t[s].classList.remove("hide"))})});

//No refactoring
/* const fetchPokemon = () => { const getPokemonUrl = id => `https://pokeapi.co/api/v2/pokemon/${id}` const pokemonPromises = [] for (let i = 1; i <= 150; i++) { pokemonPromises.push(fetch(getPokemonUrl(i)).then(response => response.json())) } Promise.all(pokemonPromises) .then(pokemons => { const lisPokemons = pokemons.reduce((accumulator, pokemon) => { const types= pokemon.types.map(typeInfo => typeInfo.type.name) accumulator += `<li class="card  ${types[0]}"> <h2 class="card-title">${pokemon.id}.${pokemon.name}</h2> <img class="card-image" alt="${pokemon.name}" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id}.png"> <p class="card-subtitle">${types.join(' | ')}</p> </li>` return accumulator }, '') const ul = document.querySelector("[data-js='pokedex']") ul.innerHTML = lisPokemons }) } fetchPokemon() */
