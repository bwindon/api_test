const headers = new Headers({ "Access-Control-Allow-Origin": "*" });

async function fetchData(){
    const url = 'http://localhost:8000/spotify/test/';
    const response = await fetch(url, {headers: headers});
    // wait until request has been completed
    const datapoints = await response.json();
    // check
    console.log(datapoints);
    return datapoints;
    }



function testMethod(){
    document.getElementById("demo2").innerHTML = 'This is the test method validation';
    }


