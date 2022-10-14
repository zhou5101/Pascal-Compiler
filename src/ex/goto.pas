program gotoEx;

label l2;
var a: integer;


begin
    a := 2;
    
    if a = 2 then
        goto l2;

    a := 9;

l2: 
    writeln('after, jump: ', a);
    
end.
