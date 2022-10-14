program repeatEx;
var x: integer;

begin
    x := 5;

    writeln('initial value of x: ', x);
    repeat
        x := x - 1;
    until x < 1;
    writeln('after repeat statement: ', x);
end.