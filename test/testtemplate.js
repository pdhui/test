describe("A suite of basic functions", function() {
    var name,
        exp;
    it("getDirectiveName", function() {
        name = "ng-repeat";
        exp = "ngRepeat";
        expect(exp).toEqual(getDirectiveName(name));
        name = "vif";
        exp = "vif";
        expect(exp).toEqual(getDirectiveName(name));
        name = "ng-when-case";
        exp = "ngWhenCase";
        expect(exp).toEqual(getDirectiveName(name));
    });
    it("seen has bug parse", function() {
        var value1 = "ff.ii",
            value2 = "eo.ljlj",
            exp1 = value1.split("."),
            exp2 = value2.split("."),
            res1, res2, data1, data2;
        res1 = parse_bug(value1,1);
        res2 = parse_bug(value2,2);
        data1 = res1();
        data2 = res2();
        expect(exp1).toEqual(data1);
        expect(exp2).toEqual(data2);  
        
         
    });
    it("template service test",function(){
        var templatefn = $.fn.template,
            customerService = templatefn.service("customer");
        var result = customerService("Panda");
        var exp = "hello Panda";
        expect(exp).toEqual(result);
        console.log(result);
        console.info(customerService("gh"));
    });
});