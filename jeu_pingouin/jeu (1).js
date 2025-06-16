const pingouin =document.getElementById('pingouin');
const eau = document.getElementById('eau');


document.addEventListener('keydown',function(event){
  // La position verticale du haut du pingouin.
  // On utilisez parseInt pour passer de la chaîne "123px" au nombre 123.
  let top=parseInt(pingouin.style.top);
  if(event.code ==="ArrowUp"  ){top-=30;}
  if(event.code ==="ArrowDown"){top+=30;}
  // Éviter que le pingouin ne sorte de l'eau
  if(top<0     ){top=0;}
  if(top>450-60){top=450-60;}
  // Mettre à jour la position
  pingouin.style.top=top+'px';
});

window.setInterval(function(){
    const poisson=document.createElement('img');
    poisson.src='poisson.svg';
    poisson.className='poisson';
    eau.append(poisson);
    poisson.style.top=(Math.random()*(450-18))+'px';
    window.getComputedStyle(poisson).top;
    poisson.style.left=0;
    window.setTimeout(function(){
        poisson.remove();
    },2000);
  },500);
  