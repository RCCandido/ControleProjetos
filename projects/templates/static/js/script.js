function gera_cor(qtd = 1) {
  var bg_color = []
  var border_color = []
  for (let i = 0; i < qtd; i++){
    let r = Math.random() * 255;
    let g = Math.random() * 255;
    let b = Math.random() * 255;
    bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
    border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
  }

  return [bg_color, border_color];
}

function renderiza_total_usuarios(url) {
  fetch(url, {
    method: 'get',
  }).then(function (result) {
    return result.json()
  }).then(function (data) {
    document.getElementById('total_usuarios').innerHTML = data.total_usuarios
  })
}

function renderiza_total_usuarios_chart() {
  const ctx = document.getElementById('projetos_total_chart').getContext('2d');
  var cores = gera_cor(qtd=3)
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Fev', 'Mar'],
      datasets: [{
        label: "Projetos",
        data: [65, 59, 80],
        backgroundColor: "#CB1EA8",
        borderColor: '#FFF',
        borderWidth: 0.2
      }]
    }
  })
}