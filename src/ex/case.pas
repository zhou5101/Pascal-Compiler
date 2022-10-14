program caseEx;

var yr: integer;
var grade: char;


begin
    yr := 3;

    case (yr) of
        1 : grade := 'd';
        2 : grade := 'c';
        3 : grade := 'b';
        4 : grade := 'a';
    end;

    writeln(grade);
end.