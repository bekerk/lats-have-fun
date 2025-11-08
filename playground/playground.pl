:- use_module(library(random)).

magicNumber(2).
magicNumber(3).
magicNumber(10).

nearby(X, Y) :- X = Y.
nearby(X, Y) :- Y is X + 1.
nearby(X, Y) :- Y is X - 1.

countTo(X) :- countUpTo(1, X).
countTo2(X) :- forall(between(1, X, Y), writeln(Y)).

countUpTo(Value, Limit) :- Value = Limit, writeln(Value), !.
countUpTo(Value, Limit) :- Value < Limit, writeln(Value),
    NextValue is Value + 1,
    countUpTo(NextValue, Limit).

countUpTo2(Value, Limit) :- writeln(Value),
    Value = Limit -> true ; (
        NextValue is Value + 1,
        countUpTo2(NextValue, Limit)
    ).

god(a, true_god).
god(b, false_god).
god(c, random_god).

answer(true_god, Proposition, da) :- call(Proposition).
answer(true_god, Proposition, ja) :- \+ call(Proposition).

answer(false_god, Proposition, da) :- \+ call(Proposition).
answer(false_god, Proposition, ja) :- call(Proposition).

answer(random_god, _Proposition, Answer) :- 
    random_between(0, 1, X), (X =:= 1 -> Answer = da ; Answer = ja).

ask(God, Proposition, Answer) :-
    god(God, Kind), answer(Kind, Proposition, Answer).

meta_ask(God, Proposition, Answer) :-
    ( ask(God, Proposition, ja) -> Answer = ja ; Answer = da).

% example question:
% ?- meta_ask(a, (c = random_god), Answer).
% Answer = da or ja depending on whether c is random_god and a is true_god, which is not known.
