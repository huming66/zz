var __zz = {
  csv0: './data/dataInGR.csv',
  csv: './data/index.csv',
  json: './data/sc.json',
  config_hm : {
    // keyHide: ['QC', 'info_further', 'job(s)','team(s)','rank','owner','added_by','source']
    // keyHide: ['paragraphs', 'notes','title']
    keyHide: ['标题', '作者','内容']
  }

}
function refresh_pc(filtered = 0) {
    d3.select("#vizPC").html("")
    d3.csv(__zz.csv, function (data) {      // to set "" to undifined for showing invalid value
    // d3.json(__zz.json, function (data) {      // to set "" to undifined for showing invalid value
      // for combined-column
      // var cmbColumns = Object.keys(data[0]).filter(v => v.slice(-3) == '(s)')
      // if (cmbColumns.length>0) {
      //   cmbColumns.forEach(col => {
      //     data = brkColumn(data, col)
      //   }) 
      // }
      data = data.slice(0,100)
      // data.forEach(v => {
      //   if (v.title) return
      //   v.title = v.paragraphs[0].replaceAll('。','')
      // })
      var treeData_filter = [  
        {id: 'string_', type:'group',text:'Column in string',children:[]},
        {id: 'number_', type:'group',text:'Column in number',children:[]}
      ]
      Object.keys(data[0]).forEach((col,i) => {  
        var dType = (parseFloat(data[0][col]) == data[0][col] && (data[0][col] != null)) ? 'num' : 'str'
        if (dType == 'str') {
          var uniqueV = [ ...new Set(data.map(d => d[col]))]
          treeData_filter[0].children.push(
            {
              id: col,
              type: 'column',
              text: col,
              children : uniqueV.map(v=> {return {id: col+ '||' + v, type:'value', text: v}})                                        
            }
          )
        } else {
          if(col=="#") col="_#"
          treeData_filter[1].children.push({id: col, type:'column', text: col})
        }
      })                      // treegrid data
      // ========= to create a jstree to replace "#_side_1" & "#_side_2" =====
      $('#tree_filter').jstree({
        'core': {
          'data': treeData_filter
        },
        "themes": {
          "theme": "default",
          "dots": true,
          "icons": true
        },
        "types": {
          "default": {
          },
          "column": {
            "icon": "glyphicon glyphicon-th-large"
          },
          "value": {
            "icon": "glyphicon glyphicon-th-list"
          }
        },
        "plugins": ["search", "state", "types", "_sort", "checkbox"],
        "search": {
          "case_insensitive": true,
          "show_only_matches": true
        }
      });
  
      $('#tree_filter').on('changed.jstree', function (e, data) {
        var keySelect = data.selected.filter(k => data.instance.get_node(k).type == 'column')
        keySelect = keySelect.map(v => v=='_#'? '#' : v)
        var valFilter0 = data.selected.filter(k => data.instance.get_node(k).type == 'value')
        keySelect = [...keySelect, ...valFilter0.map(v => v.split('||')[0])]
        __zz.config_hm.keyHide = key0.filter(k => !keySelect.includes(k))
        var valFilter1 = {}
        valFilter0.forEach(f => {
          [k,v] = f.split('||')
          if (valFilter1[k]) {
            valFilter1[k].push(v)
          } else {
            valFilter1[k] = [v]
          }
        })
        valFilter = Object.keys(valFilter1).map(k => [k, valFilter1[k]])
      }) 
      // ===END=== to create a jstree to replace "#_side_1" & "#_side_2" =====
      key0 = d3.keys(data[0]);
      var color = function (d) { return d3.scale.category10()(d.Scenario_ID); };  //var colors = d3.scale.category10()
      d3.select("#clrBy").html('')  // color_by drop-down
      d3.select("#clrBy")
        .selectAll("option")
        .data(key0)
        .enter().append("option")
        .text(function (d) { return d; })
        .attr("value", function (d, i) { return d; });
  
      function updateLabel1(dimension) {
        d3.select("#labelDetail").text(dimension);
      }
  
      if (filtered != 0) {              // filtered data only, 20200327
        data = data.filter(d => {
          var in0 = true
          Object.keys(filtered).forEach(k1 => {
            if (parcoords.dimensions()[k1].type == "string") {
              in0 = in0 && filtered[k1].includes(d[k1])
            } else if (parcoords.dimensions()[k1].type == "number") {
              in0 = in0 && (filtered[k1][0] <= d[k1]) && (filtered[k1][1] >= d[k1])
            }
          })
          return in0
        });
      } 
      parcoords = d3.parcoords(__zz.config_hm)("#vizPC")  //hmhm: pass the config_hm
        .data(data)
        .hideAxis(__zz.config_hm.keyHide)
        .color('green')
        .alpha(0.90)
        .composite("darken")
        .margin({ top: 50, left: 80, bottom: 80, right: 30 })
        .mode("queue")
        .render()
        .brushMode("1D-axes-multi");  // enable brushing: 1D-axes 1D-axes-multi 2D-strums
      parcoords.svg.selectAll("text")
        .style("font", "10px sans-serif");
      parcoords.svg.selectAll("text.label")
        .style("font-weight", "bold");
      parcoords.svg.selectAll("text.label")
        .style("font-size", "10px");
      // d3.selectAll('g.dimension g.axis text.label').attr("transform","translate(-0, -20) rotate(25*0)") 

      // hm: =========grid/list interactions / updating	
      parcoords.on('brushend', function (d) {                     //hm: update after brushing
        parcoords.render();
      })
      parcoords.on('brush', function (d) {                         //hm: update during brushing
        // parcoords.render();	
        //hm: data grid	
        __zz.brushed = parcoords.brushed()
        // update_ListArticle(parcoords.brushed())
        update_ListSC(parcoords.brushed())        
      })
    })
  };
// for breaking miltiple comma-seperated values "value1,value2 ..." into miltiple rows 
function brkColumn(data, col) {
var data_ = []
data.forEach(d => {
    var vals = d[col].split(',')
    vals.forEach(v => {
    d[col] = v
    data_.push(JSON.parse(JSON.stringify(d)))
    }) 
})
return data_
}
// for color_by
rstColor = function (dim, clr) {
    if (parcoords.dimensions()[dim].type == 'number') {
        colors = d3.scale.linear()
        colors.domain(dRG(parcoords.data(), dim))
        if (clr != undefined) {
            colors.range(clr);
        }
        colors.interpolate(d3.interpolateLab);
    } else {
        // colors = d3.scale.ordinal()  //d3.scale.category10()
        // colors.domain(dRG(parcoords.data(),dim))
        // if (clr != undefined) {
        //   colors.range(clr);
        // }
        colors = d3.scale.category10();
    }

    // colors.domain(dRG(parcoords.data(),dim));
    // if (clr != undefined) {
    // 	colors.range(clr);
    // }
    var color = function (d) { return colors(d[dim]); }
    parcoords.color(color)
    parcoords.render()
}
function updColor(clr,p) {
	// if p == 1 {
	// 	clrT = clr;
	// } else {
	// 	clrB = clr;
	// }
	clrT = d3.select("#colorT").style("background-color");
	clrB = d3.select("#colorB").style("background-color");
	if (p!=0) {
		rstColor(clrBy,[clrB,clrT]);
	}
}
function clrBY(obj) {
	clrBy = obj.value;
	clrT = d3.select("#colorT").style("background-color");
	clrB = d3.select("#colorB").style("background-color");
  rstColor(clrBy,[clrB,clrT]);
  if (parcoords.dimensions()[clrBy].type == 'number') {
    d3.select('#colorT')[0][0].hidden = false;
    d3.select('#colorB')[0][0].hidden = false;
  } else {
    d3.select('#colorT')[0][0].hidden = true;
    d3.select('#colorB')[0][0].hidden = true;
  }

}
// end for color_by

function aTag(info) {
    if (info.includes('http**********')) {
        // var wrapper= document.createElement('div');
        // wrapper.innerHTML= '<div><a href="#"></a><span></span></div>';
        // var aUrl= wrapper.firstChild;
        // // aUrl = info.replaceAll(/(http[^ ]*)/g, "<a href='$1'>$1</a>")
    } else {
        aUrl = info
    }
    return aUrl
}

refresh_pc()
//=================== resize vizPC
var _pc = {
  h: $("#vizPC").height(),
  w: $("#vizPC").width()
}
function resize_pc() {
  if (_pc.h == $("#vizPC").height() && _pc.w == $("#vizPC").width() ) return // no size change
  _pc = {
    h: $("#vizPC").height(),
    w: $("#vizPC").width()
  }
  refresh_pc()
  // parcoords.resize()
}
//=================== resize vizPC