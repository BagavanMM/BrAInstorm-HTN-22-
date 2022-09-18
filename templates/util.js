var user = JSON.parse('{{ user | tojson | safe}}');
const brainwave = user.message;

const alpha1 = ['../images/alpha1/alpha1.png', '../images/alpha1/alpha2.png', '../images/alpha1/alpha3.png']
const beta = ['../images/beta/beta.png', '../images/beta/beta1.png']
const delta = ['../images/delta/delta.png', '../images/delta/delta2.png']
const high_beta = ['../images/high-beta/high-beta.png', '../images/high-beta/high-beta1.png', '../images/high-beta/high-beta2.png', '../images/high-beta/high-beta3.png']
const theta = ['../images/theta/theta.png', '../images/theta/theta1.png', '../images/theta/theta2.png']
const low_beta = ['../images/low-beta/low-beta.png','../images/low-beta/low-beta1.png']

const central = [['../images/high-beta/high-beta.png', '../images/high-beta/high-beta1.png', '../images/high-beta/high-beta2.png', '../images/high-beta/high-beta3.png'], ['../images/beta/beta.png', '../images/beta/beta1.png'],
['../images/low-beta/low-beta.png','../images/low-beta/low-beta1.png'], ['../images/alpha1/alpha1.png', '../images/alpha1/alpha2.png', '../images/alpha1/alpha3.png'], ['../images/theta/theta.png', '../images/theta/theta1.png', '../images/theta/theta2.png'],
['../images/delta/delta.png', '../images/delta/delta2.png']]

//  go into central[brainwave], return a random image, set that image to getElbyId in result

function rand (array) {
return Math.floor(Math.random() * array.length)
}

let img = document.createElement("img");
img.src = central[brainwave][rand(central[brainwave])];
let src = document.getElementById("photos");
src.appendChild(img);

console.log(brainwave)
