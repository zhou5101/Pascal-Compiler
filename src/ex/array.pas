program arrayEx;
var arr: array[5..10] of integer;

begin
    arr[6] := 12;
    arr[5] := arr[6] - 2;
    writeln(arr[5], ' ', arr[6]);

end.
