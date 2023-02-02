function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function httpPostAsync(url, data, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if (xmlHttp.readyState == 4 && xmlHttp.status == 201)
        callback(xmlHttp.responseText);
    }
    xmlHttp.open("POST", url, true); // true for asynchronous
    xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlHttp.send(JSON.stringify(data));
}

function sendGrammarCallback(responseText) {
    // Check response is ready or not
    console.log("Data creation response received!");

    // update hypotheses table
    dataDiv = document.getElementById('test');
    sentences = JSON.parse(responseText)[1]
    let text = "<table border='1'>"
    for (let x in sentences) {
        text += "<tr><td>" + sentences[x].sentence + "</td></tr>";
    }
    text += "</table>"
    dataDiv.innerHTML = text;

    // TODO: show parser tree
}

$(document).ready(function(){
    // initialize xhr to null
    sentences = null

    $('#send').click(function(){
        // DataToSend = document.getElementById('tgrm').value;
        httpPostAsync("http://localhost:6969/users", 
                    document.getElementById('tgrm').value,
                    sendGrammarCallback)
    })

    $('#test_btn').click(function(){
        console.log(sentences)
    })
});

