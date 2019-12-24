// ajax function that retrieves all items from the houses table in the database
function getAllHousesAjax(){
    host = window.location.origin
    $.ajax({
        "url": host+"/houses",
        "method": "GET",
        "data": "",
        "dataType": "JSON",
        "success":function(result){
            for (house of result){
                addHouseToTable(house);
            }
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error)
        }
    });
}

// ajax function that creates a house and places it in the relevant table
function createHouseAjax(house){
    host = window.location.origin
    console.log(JSON.stringify(house)); //output to console
    $.ajax({
        "url": host+"/houses",
        "method":"POST",
        "data":JSON.stringify(house),
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success":function(result){
            house.id = result.id

        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

// ajax function that updates an existing house in the database
function updateHouseAjax(house){
    host = window.location.origin
    console.log(JSON.stringify(house)); //output to console
    $.ajax({
        "url": host+"/houses/"+encodeURI(house.id),
        "method":"PUT",
        "data":JSON.stringify(house),
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success":function(result){
            
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

// ajax function that deletes an existing house in the database
function deleteHouseAjax(id){
    host = window.location.origin
    $.ajax({
        "url": host+"/houses/"+encodeURI(id),
        "method":"DELETE",
        "data":"",
        "dataType": "JSON",
        contentType: "application/json; charset=utf-8",
        "success":function(result){   
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

// ajax function that retrieves all items from the areas table in the database
function getAllAreasAjax(){
    host = window.location.origin
    $.ajax({
        "url": host+"/areas",
        "method": "GET",
        "data": "",
        "dataType": "JSON",
        "success":function(result){
            for (area of result){
                addAreaToTable(area);
            }
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error)
        }
    });
}