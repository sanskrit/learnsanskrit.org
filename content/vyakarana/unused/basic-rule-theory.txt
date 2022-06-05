{title Basic rule theory}

Starting from our lesson on the Shiva Sutras, we have slowly built up a small
but useful part of the Pāṇinian system:

{ol
    {li First, we learned about the various devices we use to keep our system
    concise and expressive. These include the {s pratyAhAra}, various groupings
    of {s savarNa} sounds, and {s it} letters.}

    {li Next, we applied these basic devices to define a variety of {s ac}
    sandhi rules. We also saw how the behavior of these rules can be controlled
    and changed through {s adhikAra} rules.}
}

In all, we have seen around 40 rules, or 1 percent of the grammar. Before we
continue onward and expand our knowledge of the system, let's consolidate what
we have learned so far.


{h How we classify rules}

The {cite Aṣṭādhyāyī} uses several distinct kinds of rules. Different authors
classify these rules in various way, but there are five core types we can focus
on.

The most concrete rule is the {s-dfn vidhi} ("operation"). A {s vidhi} states
that some operation should be applied. Usually, the operation is some kind of
substitution:

{rule

iko yaNaci | 6.1.77
ikaH yaN aci
An `ik vowel is replaced by its respective `yaN sound when a vowel follows [in
`saMhitA].

}

Next is the {s-dfn saMjJA} ("designation"), which defines a term:

{rule

tulyAsyaprayatnaM savarNam | 1.1.9
tulya-Asya-prayatnam savarnam
[Sounds with] the same `Asya (place of articulation) and `prayatna
(articulatory effort) are called `savarNa (similar).

}

Third is the {s-dfn atideza} ("extension"), which says that one term is
{em like} another. This is a simple concept, but we haven't seen any examples
of it so far. Here is a common one, which we will return to in a later lesson:

{rule

sthAnivadAdezo 'nalvidhau | 1.1.56
sthAnivat AdezaH an-al-vidhau
An `Adeza (replacement) is [treated] like its `sthAnin (replaced term) [in
terms of the properties it inherits, etc.], excluding rules that concern a
single sound.

}

Fourth is the {s-dfn adhikAra} ("government"), which extends or modifies the
rules within its scope:

{rule

saMhitAyAm | 6.1.72
_
In `saMhitA, &hellip;

}

Fifth is the {s-dfn paribhASA} ("metarule"), which explains how we should
interpret the rules of the grammar:

{rule

SaSThI sthAneyogA | 1.1.49
SaSThI sthAne-yogA
The sixth case can signify `sthAne (in the place of).

}

Any of these rule types may also be restricted in some way. Such restriction
rules are often called {s-dfn niyama} ("restriction"). For example, the rule
below can be seen as a {s niyama} on rule 6.1.77 ({s iko yaN aci}), because it
limits the scope in which 6.1.77 can apply:

{rule

akaH savarNe dIrghaH | 6.1.101
_
`ak and a following `savarNa [vowel] become a `dIrgha (long) [in `saMhitA].

}

Different authors may use a different schema for these rules. Our goal here is
just to point out the basic patterns.


{h How we apply rules}

The {cite Ashtadhayayi} is a system that derives Sanskrit expressions. These
derivations are called {s-dfn prakriyA}s. By applying rules in the correct
way, we create a valid {s prakriyA}, which gives us a valid Sanskrit
expression.

One crucial point is that the {cite Aṣṭādhyāyī} does not apply its rules in
some fixed or linear order. So at any step in the {s prakriyA}, we might have
multiple candidate rules we can choose from, and these candidate rules could
come from nearly anywhere in the {cite Aṣṭādhyāyī}.

Choosing the right rule to apply is a deep theoretical issue, but here are some
simple rules of thumb:

{ul
    {li Prefer exceptions to general rules.}
    {li Prefer later rules to earlier rules.}
    {li If a rule {code A} would affect another rule {code B}, prefer {code A}
    to {code B}.}
}

The {s prakriyA} is complete and valid only when there are no more rules we
could apply.  As long as a rule could still apply, we must apply it.
