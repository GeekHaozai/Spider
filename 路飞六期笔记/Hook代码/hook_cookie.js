(function (){
    var val = "";
    Object.defineProperty(document,"cookie",{
        set(v){
            debugger
            val = v;
        },
        get(){
            return val;
        }
    })
})()