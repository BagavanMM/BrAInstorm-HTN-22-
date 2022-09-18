var user = JSON.parse('{{ user | tojson | safe}}');
const brainwave = user.message;

const alpha1 = ['../images/alpha1/alpha1.png', '../images/alpha1/alpha2.png', '../images/alpha1/alpha3.png']
const beta = ['../images/beta/beta.png', '../images/beta/beta1.png']
const delta = ['../images/delta/delta.png', '../images/delta/delta2.png']
const high_beta = ['../images/high-beta/high-beta.png', '../images/high-beta/high-beta1.png', '../images/high-beta/high-beta2.png', '../images/high-beta/high-beta3.png']
const theta = ['../images/theta/theta.png', '../images/theta/theta1.png', '../images/theta/theta2.png']
const low_beta = ['../images/low-beta/low-beta.png','../images/low-beta/low-beta1.png']

function rand (arr) {
    return arr[Math.floor(Math.random) * arr.length]
}


console.log(brainwave)
return rand (brainwave)
