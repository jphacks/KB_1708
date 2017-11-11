
var check_all = function (classname) {
    var element = document.getElementsByClassName(classname)

    for(var i=0;i<element.length;i++){
        element[i].checked= true;
    }
};

var decheck_all = function (classname) {
    var element = document.getElementsByClassName(classname)

    for(var i=0;i<element.length;i++){
        element[i].checked= false;
    }
};


