const headers = new Headers({ "Access-Control-Allow-Origin": "*" });


function updateChart(){
    async function fetchData(){
    const url = 'http://localhost:8000/strava/test/';
    const response = await fetch(url, {headers: headers});
    // wait until request has been completed
    const datapoints = await response.json();
    // check
    console.log(datapoints);
    return datapoints;
    };


    fetchData().then(datapoints => {
      const start = datapoints[0].map(function(index){
        return index.start_date_local;
        })

      const distance = datapoints[0].map(function(index){
        return index.distance;
        })

      const speed = datapoints[0].map(function(index){
        return index.average_speed;
        })

      document.getElementById("demo").innerHTML = 'this is demo - ID';
      console.log(start);
      console.log(distance);
      console.log(speed);
      myChart.config.data.labels = start;
      myChart.config.data.datasets[0].data = distance;
      //myChart.config.data.datasets[0].data = speed;


      myChart.update();
    });
};


const labels = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
];

const data = {
  labels: labels,
  datasets: [
  {
    label: 'Distance',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 1000, 5, 2, 20, 1000, 45],

  },
  {
  label: 'Average speed',
    backgroundColor: 'rgb(0, 0, 0)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 1000, 45]
  }
]
};

const config = {
  type: 'bar',
  data: data,
  options: {},
};

const myChart = new Chart(
  document.getElementById('myChart'),
  config
);