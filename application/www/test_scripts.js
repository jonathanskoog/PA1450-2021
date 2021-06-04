function set_dropdown(id, dropdown)
{
    var clicked = document.getElementById(id)
    let regionBtn = document.getElementById("dropRegion4");
    let cntryBtn = document.getElementById("dropCountry4")
    if (clicked == regionBtn)
    {  
        document.getElementById("dropdown1").innerHTML = "7 Days"
        document.getElementById("dropdown1").disabled = true;
    }
    else if (clicked == cntryBtn)
    {
        document.getElementById("dropdown1").disabled = false;
    }
    var drop = document.getElementById(dropdown)
    drop.innerHTML = clicked.innerHTML
}

function set_btn_success(id)
{
    var btnGraph = document.getElementById("btnGraph")
    var btnTable = document.getElementById("btnTable")
    var curr = document.getElementById(id)
    btnGraph.classList.remove("btn-primary")
    btnTable.classList.remove("btn-primary")
    btnGraph.classList.add("btn-dark")
    btnTable.classList.add("btn-dark")
    console.log(btnTable.classList)
    if (curr != btnGraph)
    {
        document.getElementById("downloadGraph").src = "";
        document.getElementById("previewGraph").src = "";
    }
    if (curr != btnTable)
    {
        let elem = document.getElementById("divvider")
        console.log(elem)
        if (elem)
        {
            console.log(elem)
            elem.remove()
        }
    }
    document.getElementById(id).classList.remove("btn-dark")
    document.getElementById(id).classList.add("btn-primary")

}

function render_graphic()
{

    var btnGraph = document.getElementById("btnGraph");
    if (btnGraph.classList.contains("btn-primary"))
    {
        render_Graph();
    } else
    {  
        render_Table();
    }
}

function render_Graph()
{
    var country = document.getElementById("Country-filter").value;
    var region = document.getElementById("Region-filter").value;
    var series = document.getElementById("case-filter").value;
    var timespan = document.getElementById("dropdown1").innerText
    var stat_type = document.getElementById("dropdown2").innerHTML
    var displayPer = document.getElementById("dropdown3").innerHTML
    var filter_type = document.getElementById("dropdown4").innerHTML

    let timeMap = timespan_translater(timespan)
    let apiString = get_api_to_call_graph(filter_type, stat_type, displayPer, series, country, timeMap["Days"], timeMap["Months"])
    document.getElementById("previewGraph").src = apiString;
    document.getElementById("downloadGraph").src = apiString;

}

function timespan_translater(span)
{  
    let filter_type = document.getElementById("dropdown4").innerHTML
    let retMap = new Map()
    let days = 0
    let months = 0
    if (filter_type == "Region")
    {
        span = "7 Days";
    }
    switch(span)
    {
        case "Recent":
            days = 1;
            break;
        case "7 Days":
            days = 7;
            break;
        case "Month":
            months = 1;
            break;
        case "3 Months":
            months = 3;
            break;
        case "1 Year":
            months = 12;
            break;
        case "Beginning":
            months = 300;
            break;
    }
    retMap["Days"] = days
    retMap["Months"] = months
    return retMap;
}

function get_api_to_call_graph(filter_type, stat_type, displayPer, series, country, days, months)
{
    let retStr = stat_type +"/"+displayPer+"/"+series+"/"+country;
    let type = filter_type.replace(/\s/g, '');
    if (type == "Country")
    {
        retStr = "/createGraphSeries/" + retStr + "/"+days.toString() +"/"+ months.toString();
    }
    else
    {
        let region = document.getElementById("Region-filter").value;
        retStr = "/casesPerRegion/" + retStr + "/" + region + "/" + days.toString();
    }
    return retStr;
}

function render_Map()
{
}

function render_Table()
{
    let table = document.getElementById("previewTable")
    let newDiv = document.createElement("div")
    newDiv.id = "divvider"
    let jqXHR = $.get("/drawTABLE")
    .done(function(response){
        newDiv.insertAdjacentHTML("beforeend",response)
    })
    table.insertAdjacentElement("beforeend",newDiv)
}