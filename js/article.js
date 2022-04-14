function update_ListArticle(data) {
    var row = d3.select("#listArticle")                      // data ready
        .html("")
        .selectAll("div")
        .data(data)
        .enter().append("div")
        .attr("class", function (d) { return ("articleOff"); })
        .text(function (d) { return JSON.stringify(d).replaceAll(',',', ') })
        .on("click", function (d) {
            d3.select(".articleOn").classed("articleOn", false)
            this.classList.add("articleOn")
            __zz.onArticle = d.info_further
            $('#summaryArticle').html(JSON.stringify(d).replaceAll(',',', '))




            // this.setAttribute("class", "articleOn")
            // if (this.innerText == '[+/') {
            //     this.innerText = '[-/';
            //     this.setAttribute("class", "aticleOff")
            //     spa.tagNeg.push(d)                            // push in
            // } else {
            //     this.innerText = '[+/';
            //     this.setAttribute("class", "tagSignP")
            //     spa.tagNeg = spa.tagNeg.filter(e => e !== d); //in, move out
            // }
            // reChart0()
        }).on({
            "mouseover": function (d) { parcoords.highlight([d]) },
            "mouseout": parcoords.unhighlight
        });
}

function update_ListSC(data) {
    var row = d3.select("#listArticle")                      // data ready
        .html("")
        .selectAll("div")
        .data(data)
        .enter().append("div")
        .attr("class", function (d) { return ("articleOff"); })
        .text(function (d) { return d.title })
        .on("click", function (d) {
            d3.select(".articleOn").classed("articleOn", false)
            this.classList.add("articleOn")
            __zz.onArticle = d.title
            $('#summaryArticle').html('<b>' + d.title + '</b><br><hr>' +d.paragraphs.join('<br>') + '<br><hr>' + d.notes)
        }).on({
            "mouseover": function (d) { parcoords.highlight([d]) },
            "mouseout": parcoords.unhighlight
        });
}