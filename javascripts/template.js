(function(window,$){

    function ng(){
        var directives = {
            "ghRepeat":{
                    "priority" : 1000,
                    "transclude" : "element", 
                    compile:function(transclude){
                        return function (scope,element,attrs){
                            var value, values, itemname, listname, listvalues, childrennode,
                                cusor ;
                            cusor = element = $(element);
                            value = attrs.ghRepeat;
                            values = value.split(" ");
                            if(values.length != 3)
                                throw new Error();
                            itemname = values[0];
                            listname = values[2];
                            listvalues = parse(listname)(scope);

                            if(!listvalues)
                                return;
                            // childrennode = $(element).children();
                            // childrennode.remove();
                            for(var i=0,listlen=listvalues.length; i < listlen; i++)
                            {
                                scope[itemname] = listvalues[i];
                                transclude(scope,function(node){
                                    cusor.after(node);
                                    cusor = node;
                                });

                            }
                        }
                    }   
                    
                } ,
            "ghText":{
                compile:function(transclude){
                    return function(scope,element,attrs){
                        var name = attrs.ghText, value;
                        if(!name)
                            return;
                        value = parse(name)(scope);
                        $(element).text(value);
                    };
                }
            },
            "ghShow":{
                compile:function(transclude){
                    return function(scope,element,attrs){
                        var name = attrs.ghShow, value;
                        if(!name)
                            value = false;
                        else{                            
                            value = parse(name)(scope);
                            if(value == "true")
                                value = true;
                            else if(value == "false")
                                value = false;

                        }
                        value ? $(element).show() : $(element).hide();
                    };
                }
            }
        };
        function isString(str){
            return typeof str == "string"
        }
        function isDefined(val){
            if (typeof val == "undefined")
                return false;
            return true;
        }
        function $getFn(fn,args,context){
            return function(){
                var params = args.concat(arguments)
                fn.apply(context,args);
            }
        }
        $.extend(arguments.callee, {
            services : {},
            directives : directives,
            isString : isString,
            $getFn : $getFn,
            isDefined : isDefined
        });
       
    };
    ng();
    function template(element){
        if(!element && this instanceof $)
            return compile(this);
        return compile(element);

        function compile(element, maxpriority){
            if(element instanceof $)
                element = $(element);
            var composilinkfn = compileNodes(element, maxpriority);
            return function publicLinkfn(scope,clonefn){
                var $element = !clonefn ? element : element.clone();
                if(clonefn && $.isFunction(clonefn)) clonefn($element);
                composilinkfn(scope,$element) 
                return $element;
            }
        }

        function compileNodes(elements, maxpriority){
            var linkfns = [],directive,nodelinkFn,childLinkfn,name, element;
            for(var j=0,elen = elements.length; j < elen; j++)
            {
                element = elements[j];
                nodelinkFn = element.nodeType==8 ? null : applyToDirective(element,maxpriority);    
                childLinkfn = (nodelinkFn && nodelinkFn.terminal) || !element.childNodes.length  ? null : compileNodes(element.childNodes);
                linkfns.push(nodelinkFn);
                linkfns.push(childLinkfn);
            }
            return function composilinkfn(scope,elements){
                applyDirective(scope,linkfns,elements);
                                
            }
        }
        function isDirective(attrname){           
            return ng.directives[attrname] ? true : false;
        }
        function applyToDirective(element,maxpriority){
            var directive ,name,linkfn = [], haslink = false,
                 $attrs={}, value = "", childtransclude,
                 priority, terminal = false, directiveCollection=[],terminalpriority=-Number.MAX_VALUE,
                 TAGNODE = 1, TEXTNODE = 3;
            switch(element.nodeType)
            {
                case TAGNODE:
                    for(var i=0,attrs=element.attributes,attrlen=attrs.length;i<attrlen;i++)
                    {
                        attribute = attrs[i];
                        name = getDirectiveName(attribute.nodeName);
                        if(isDirective(name))
                        {
                            directive = ng.directives[name]; 
                            priority = directive.priority;
                            if(priority >= maxpriority) //递归compile时使用，只收集小于指定最大优先级的指令，因为大于等于指定最大优先级的指令已经被执行过了
                                continue;                                                               
                            $attrs[name]  = $.trim(($.browser.msie && name == 'href')
                                ? decodeURIComponent(element.getAttribute(name, 2))
                                : attribute.value);
                            directive.name = name;  
                            directiveCollection.push(directive) ;                                          
                        }                     
                    }
                    directiveCollection.sort(function(val,nextval){
                        if(val < nextval)
                            return true;
                    });
                    $.each(directiveCollection,function(index, directive){
                        var value = null;
                        if(terminalpriority > directive.priority)//只执行大于“结束优先级”的指令
                            return;
                        if(value = directive.transclude)
                        {
                            if(value == "element")
                            {
                               templatenode = $(element);
                               compilenode = $("<!--" + directive.name + ":" + $attrs[name] +" -->")
                               templatenode.replaceWith(compilenode);
                               childtransclude = compile(templatenode,directive.priority);
                            }
                            terminal = true;
                            terminalpriority = directive.priority;
                        }
                        linkfn.push(directive.compile(childtransclude));
                    });
                    break;
                case TEXTNODE: 
                    var value = $.trim(element.nodeValue),
                        interpolate ,
                        textdirective, textdirectivelink;
                        if(!value)
                            return null;
                    interpolate = template.service("interpolate");
                    textdirective = interpolate(value);
                    if(!ng.isString(textdirective))
                    {
                        textdirectivelink = AddToTextDirective(textdirective);
                        linkfn.push(textdirectivelink.compile());
                    }
                    
            }       
            
            nodeLinkFn.terminal = terminal;
            return linkfn.length > 0 ? nodeLinkFn : null;

            function nodeLinkFn(scope,childlink,element){
                var compilenode,templatenode ;
                $.each(linkfn,function(index,directive){
                    
                    directive.apply(this,[scope,element,$attrs]);
                });
                childlink && childlink(scope,element.childNodes);
            }
        }
        
        function applyDirective(scope,linkfns,elements){
            var ischildexcute = false, element, i=0;

             for(var j=0,elen = elements.length; j < elen; j++)
            {
                element = elements[j];
                nodelinkFn = linkfns[i++];    
                childLinkfn = linkfns[i++];
                if(nodelinkFn)
                    nodelinkFn(scope,childLinkfn,element);
                else if(childLinkfn)
                    childLinkfn(scope, element.childNodes);
            }        
        }
        function AddToTextDirective(stament){
            var newdirective = {
                compile:function(transclude){
                    return function(scope,element,attrs){
                       var result = stament(scope);
                        element.nodeValue = result;
                    }
                }
            };
            return newdirective;
        }
        function getDirectiveName(name){
            if(!name)
                return;
            var names = name.split("-"),
                result = "" + names[0];
            for(var i=1,len=names.length; i < len; i++)
            {
                var item = names[i];
                result += item.charAt(0).toUpperCase() + item.substring(1);
            }
            return result;
        }
    }
    template.service = function(name, service){
        var injectservice, injdectlist = [], cache, injectnames;
        if(name && service)
        {                      
            if($.isFunction(service) || ($.isArray(service) && service.length > 0)){
                ng.services[name] = service;
            }                    
        }
        else if(name && !service)
        {
           cache = ng.serviceCache = ng.serviceCache || {};
           if(cache[name])
                return cache[name];
           else{
                service = ng.services[name];
                if(!service)
                    return;
                if($.isArray(service))
                {
                    if(service.length == 1)
                        service = service[0];
                    else{
                        injectnames = service.slice(0,service.length-1);
                        $.each(injectnames,function(index, value){
                            if(ng.isString(value))
                            {                            
                                if(!(injectservice = cache[value]))
                                {
                                    injectservice = template.service(value);;
                                }
                                injdectlist.push(injectservice);
                            }   
                        });
                        service = service.pop();
                    }                              
                }
                return cache[name] = service.apply(this,injdectlist);
           }  
        }  
    };
    template.directive = function(name, directiveFn){
        ng.directives[name] = directiveFn;
    };
    function parse(expr){
        var value,
            parser = template.service("parser") || stament;
        if(!(value = $.trim(expr)))
            return "";
        exprfn = parser(value);

        return exprfn;

        function stament(value){
            var datas = value.split(".");
            return function(context){
                var result = context;
                for(var i=0,len=datas.length;i<len && ng.isDefined(result);i++){
                    result = result[datas[i]];                  
                }
                return result;         
            }
        }
    }
    template.service("interpolate",function(){
        return function(value){
            var startch = "{", endch = "}",
                startindex = value.indexOf(startch),
                endindex = value.lastIndexOf(endch),
                temp, stament;
            if(startindex >= 0 && endindex > 0 && startindex < endindex)
            {          
                temp = value.substring(startindex + startch.length,endindex);
                stament = parse(temp);
                return function(context){
                    return value.substring(0,startindex) + stament(context) + value.substring(endindex + endch.length);
                }
            }
            else {               
                    return value;                
            }
        };
    });
    template.directive("ghIf",{
        compile:function(transclude){
                    return function(scope,element,attrs){
                        var name = attrs.ghIf, value;
                        if(!name)
                            value = false;
                        else{                            
                            value = parse(name)(scope);
                            if(value == "true")
                                value = true;
                            else if(value == "false")
                                value = false;

                        }
                        value ? null : $(element).remove();
                    };
                }});
    $.fn.extend({"template":template});
    $.template = template;
})(window,$);