function getDirectiveName(name){
            if(!name)
                return;
            var names = name.split("-"),
                result = "" + names[0];
            for(var i=1,len=names.length; i < len; i++)
            {
                var item = names[i];
                result += item.charAt(0).toUpperCase() + item.substr(1);
            }
            return result;
}

var templatefn = $.fn.template;
templatefn.service("sayHello",function(){
    return function(value){
        return "hello " + value;
    };
});
templatefn.service("customer",["sayHello",function(say){
    return function(name){
        return say(name) ;
    };
}]);