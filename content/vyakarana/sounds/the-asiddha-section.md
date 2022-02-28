{title The {s asiddha} section}

Most of the {cite Aṣṭādhyāyī}'s sandhi rules are in an unusual section of the
text. To understand that section, we must first understand how the Pāṇinian
system works at a high level. We'll then discuss a major problem with its
approach and how Pāṇini solves it.


{h {s prakriyA}}

When we use the {cite Aṣṭādhyāyī}, we start with an incomplete expression.
We then apply one rule at a time. The output of one rule is the input to the
next. And as we keep applying rules, our result gets closer and closer to a
valid Sanskrit expression.

This full process, including the rules we apply and the results we get, is
called a {s-dfn prakriyA} ("procedure", "derivation"). When we use the {cite
Aṣṭādhyāyī}, we must know not only what rules mean but also how to apply them
to generate a correct {s prakriyA}.

What do we mean by a "correct" {s prakriyA}? At each step in the {s prakriyA},
multiple rules could apply, and we must choose which one to use. There are a
few basic principles that help us here. (For example, we should prefer more
specific rules to less specific rules.) And {strong when we can no longer apply
any rules}, the {s prakriyA} is complete.


{h Finishing a {s prakriyA}}

Let's focus on the phrase {em "when we can no longer apply any rules."} What
does this mean? For example, we might have this incomplete expression that has
had no sandhi rules applied:

{ex

te icchanti
They want.

}

If we use rule 6.1.78 from the previous lesson:

{rule

eco 'yavAyAvaH | 6.1.78
ecaH ay-av-Ay-AvaH
An `ec vowel becomes `ay, `av, `Ay, or `Av, respectively [when a vowel follows
in `saMhitA].

}

then we can create a new result:

{ex

te icchanti > tay icchanti

}

But if you know Sanskrit, you know that this isn't the typical result. The {s
e} at the end of a word usually becomes {s a} when it is followed by a vowel.
There is a {s vidhi} rule that makes the appropriate change. And by applying
that rule, we get the correct result:

{ex

tay icchanti > ta icchanti

}


{h A serious problem}

The problem is that the {s prakriyA} is not actually complete, because another
rule can now be applied. Specifically, it's rule 6.1.87, which we saw in the
previous lesson:

{rule

AdguNaH | 6.1.87
At guNaH
`a [and the following vowel] become [a single] `guNa [in `saMhitA].

}

6.1.87 {em can} apply, and there is no other rule that takes priority over it.
So it {em must} and {em will} apply, which gives us a bad result:

{ex

* ta icchanti > tecchanti

}

It is as if a good man and a thief both come to us to ask for food. We want to
give our food to the good man and not to the thief. But if we give our food
to the good man, the thief will beat him and steal it. We must ensure that once
we give our food to the good man, the thief will not be able to take it from
him.


{h Pāṇini's solution}

Pāṇini's solution to this problem is to offer this rule:


{rule

pUrvatrAsiddham | 8.2.1
pUrvatra a-siddham
&hellip; is `asiddha (inert) in the previous [area].

}

Rule 8.2.1 is an {s adhikAra} that lasts until the very end of the {cite
Aṣṭādhyāyī}.  So, all rules that follow rule 8.2.1 will be in its scope. But
what does rule 8.2.1 mean, and what does it do?

{h Understanding rule 8.2.1}

First, let's understand the two words {s pUrvatra} and {s asiddham}.

{s pUrvatra} literally means "in the previous (area)." Here, it refers to all
previous rules in the grammar. Every rule after 8.2.1 will inherit the word {s
pUrvatra}. So for each of these rules, {em every} rule before it is {s
pUrvatra}.

{s asiddham} literally means "not accomplished" or "not enacted." Here, it
essentially means that the rule cannot be used.

We can update our translation like so:

{rule

pUrvatrAsiddham | 8.2.1
pUrvatra a-siddham
&hellip; is disabled with respect to prior rules.

}

What does this mean? Let's return to the example of the good man and the thief.
Once we give our food to the good man, it is as if he becomes invisible. Try as
he might, the thief cannot find him.

But rule 8.2.1 also has an interesting implication: we must apply the rules
of the {s asiddha} section in order. If we have two rules {code A} and {code
B}, and if {code A} comes before {code B}, then once we apply {code A}, we can
no longer apply {code B}.

{aside

{h Rule 8.2.1 for programmers}

If you are familiar with computer programs, rule 8.2.1 is straightforward.  All
prior rules are a kind of {em event-driven programming}, where we select the
rules that best match our current context. Then rule 8.2.2 is the start of an
{em iterative program}, where we apply each rule in sequence.

As far as we can tell, this observation was first made by
{a[href=http://sanskrit.uohyd.ac.in/faculty/amba/] Professor Amba Kulkarni} in
2008, in her presentation titled {cite Pāṇini's Aṣṭādhyāyī: A Computer
Scientist's viewpoint}.

}


{h The practical meaning of rule 8.2.1}

Rules after 8.2.1 should be applied in order, and they should be applied after
all other rules. This means that all of our {s prakriyA}s should have this
structure:

{ol
    {li First, we apply rules before 8.2.1.}
    {li Then, we apply rules after 8.2.1. But these rules must be applied in
    order; we cannot go back and apply an earlier rule.}
}

To return to our example above, the {s vidhi} rule that changes {s te} to {s
ta} is after rule 8.2.1. So once we apply it, we cannot go back and apply
6.1.78 ({s Ad guNaH}). We thus get the result we were aiming for:

{ex

te icchanti > ta icchanti

}

and our {s prakriyA} is complete.

{aside

{h Occasional exceptions to the {s asiddha} section}

A {em very} small number of rules can be applied after the rules in the {s
asiddha} section. How is this possible?

Simply, these are rules that would be purposeless ({s vyartha}) otherwise. As
for why they are stated outside of the {s asiddha} section, that is part of a
much longer discussion about rule inference ({s anuvRtti}) and concision ({s
lAghava}) in the {cite Aṣṭādhyāyī}.

}
