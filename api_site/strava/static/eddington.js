// Create data source

async function fetchData(){
    const url = 'http://localhost:8000/strava/test/';
    const response = await fetch(url, {headers: []});
    // wait until request has been completed
    const datapoints = await response.json();
    return datapoints;
};


// Append activity arrays (not using since embedded in updateChart)
function appendActivities(){
    fetchData().then(datapoints => {
    const length = datapoints.length +1;
    let activities = [];
    for (let i = 0; i < length; i++) {
        console.log(i);
        activities = activities.concat(datapoints[i]);
    };

    activities.sort((a, b) =>{
    return new Date(a.start_date_local) - new Date(b.start_date_local); // descending
    //return new Date(b.order_date) - new Date(a.order_date); // ascending
    })
    console.log(activities);
    //return activities;

    let object1 = activities[1200];
    console.log(object1);
    console.log(Object.keys(object1));
    });
}



function eddington() {
    // get activities

    fetchData().then(datapoints_z => {
      const length = datapoints_z.length;
      let x = length - 1;
      let activities = [];
        for (let i = 0; i < length; i++) {
            activities = activities.concat(datapoints_z[i]);
        };

    // get longest run
    longest_run = Math.max.apply(Math,activities.map(function(object) {return object.distance;}))
    document.getElementById("longest_run").innerHTML = "Longest run = " + longest_run + " kms";
    let num_segments =Math.round(longest_run/1000);

    // create eddington array - edd_array
    var edd_array = [];
    var edd_array_valid_objects = [];
        for (let i = 0; i < num_segments; i++) {
            let count_1 = activities.filter(item => item.distance > (num_segments - i) * 1000);
            let num_runs = count_1.length;
            edd_distance = num_segments - i;
            if (num_runs > edd_distance) {
                edd_check = true;
            }
            else {
                edd_check = false;
            }
            edd_array[i] = {"num_runs": num_runs, "edd_distance": edd_distance, "edd_check": edd_check};
        };


    // get list of valid eddington objects to calculate edd number.
    // edd number is longest valid object
    edd_array_valid_objects = Object.values(edd_array).filter(item => item.edd_check === true);

    // get longest valid eddington objects
    edd_number = Math.max.apply(Math,edd_array_valid_objects.map(function(object) {return object.edd_distance;}))
    document.getElementById("eddington_number").innerHTML = "Eddington number = " + edd_number;

    // create chartJS object
    const data = {
      labels: edd_array.map(row => row.edd_distance),
      datasets: [
          {
            yAxisID: 'A',
            label: 'Distance',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: edd_array.map(row => row.edd_distance),
          },

          {
            yAxisID: 'B',
            label: 'Count',
            backgroundColor: 'rgb(0, 0, 0)',
            borderColor: 'rgb(255, 99, 132)',
            data: edd_array.map(row => row.num_runs),
          },
        ],
}

    console.log(data);
    const config = {
      type: 'bar',
      data: data,
      options: {
        scales: {
            A: {
                position: 'left',
                min: 0,
                max: 50,

            },
            B: {
                position: 'right',
                //type: 'logarithmic',
                //scaleOverride : true,
                min: 0,
                max: 50,
                //ticks: {stepSize: 5},
            }
        }
      },
    };

    const myChart = new Chart(
      document.getElementById('myChart'),
      config
    );
  });
}


