% prolog implementation of three gods puzzle
% -- remove_begin -- %
% NOTE: the lines below are removed for the LLM so it does not see the gods names.
god(c, true_god).
god(a, false_god).
god(b, random_god).
% -- remove_end -- %
% Gods are a, b, and c; we do not know which role each holds.

answer(true_god, Proposition, da) :- call(Proposition).
answer(true_god, Proposition, ja) :- \+ call(Proposition).

answer(false_god, Proposition, da) :- \+ call(Proposition).
answer(false_god, Proposition, ja) :- call(Proposition).

answer(random_god, _Proposition, Answer) :- 
    random_between(0, 1, X), (X =:= 1 -> Answer = da ; Answer = ja).

% single question to god
ask(God, Proposition, Answer) :-
    god(God, Kind), answer(Kind, Proposition, Answer).

% meta question to god: if I asked you X would you say da?
meta_ask(God, Proposition, Answer) :-
    ( ask(God, Proposition, ja) -> Answer = ja ; Answer = da).

% example query:
% meta_ask(a, (c = random_god), Answer).
