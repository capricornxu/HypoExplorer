// Get Request
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

// Post Request
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

// display a tree 
function displayTree(tree) {
    if (!tree.subtrees || tree.subtrees.length == 0) {
        return '<li><code>' + tree.root + '</code></li>';
    }
    var builder = [];
    if(tree.root == 'root'){
        builder.push('<ul class="tree">');
        builder.push('<li><code>');
        builder.push(tree.root);
        builder.push('</code>');
        builder.push('<ul>');
        for (var i in tree.subtrees) {
            builder.push(displayTree(tree.subtrees[i]))
        }
    }
    else{
        builder.push('<li><code>');
        builder.push(tree.root);
        builder.push('</code>');
        builder.push('<ul>');
        for (var i in tree.subtrees) {
            builder.push(displayTree(tree.subtrees[i]))
        }
        builder.push('</ul>')
        builder.push('</li>')
    }

    return builder.join('');
}

// Grammar Callback
function sendGrammarCallback(responseText) {
    // Check response is ready or not
    console.log("Data creation response received!");
    response_data = JSON.parse(responseText)

    // update hypotheses table
    dataDiv = document.getElementById('hypo_table');
    sentences = response_data[1]
    let text = "<table border='1'>"
    for (let x in sentences) {
        if (sentences[x].evaluation == 1){
            text += "<tr><td>" + "<span style='color:blue'>" + "True " + sentences[x].sentence + "</span>" + "</td></tr>";
        }else if (sentences[x].evaluation == 0){
            text += "<tr><td>" + "<span style='color:red'>" + "False " + sentences[x].sentence + "</span>" + "</td></tr>";
        }else{
            text += "<tr><td>" + "<span style='color:green'>" + "Null " + sentences[x].sentence + "</span>" + "</td></tr>";
        }

        // text += "<tr><td>" + sentences[x].sentence + "</td></tr>";
    }
    text += "</table>"
    dataDiv.innerHTML = text;

    // show parser tree
    tree = response_data[0][1]
    console.log(tree)
    $('#tree').empty();
    $('#tree').append(displayTree(tree) + '</ul></div></br>');
    displayTree(tree)
    console.log("tree displayed!")

    // update sentence
    deterministic_sent = response_data[0][0]
    document.getElementById('sentence').value = deterministic_sent
}

// main entrance here
$(document).ready(function(){
    // initialize xhr to null
    sentences = null

    $('#send').click(function(){
        // DataToSend = document.getElementById('tgrm').value;
        httpPostAsync("http://localhost:6969/users", 
                    document.getElementById('tgrm').value,
                    sendGrammarCallback)
    })
});

