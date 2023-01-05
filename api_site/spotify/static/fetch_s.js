

async function fetchData(){
    const url = 'http://localhost:8000/spotify/test/';
    const response = await fetch(url, {headers: headers});
    // wait until request has been completed
    const datapoints = await response.json();
    // check
    console.log(datapoints);
    return datapoints;
    }

function newAlbums(){fetchData().then(datapoints => {
    const items = Object.keys(datapoints.albums.items);
        console.log(items);
        for (item of items){
            console.log(item);}

    const item_values = Object.values(datapoints.albums.items);
        for (item_value of item_values){
            console.log(item_value.name);
            document.write("<p>" + item_value.name + "</p>");
    }
})


    document.getElementById("demo2").innerHTML = 'This is new albums function';
    }

