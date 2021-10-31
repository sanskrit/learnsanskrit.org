{title {s vidhi} rules}

In the previous lessons, we defined a simple, concise, and expressive system
for defining various groups of Sanskrit sounds. But our system is missing
something obvious: a way to use the terms we've defined. It's as if we have a
gourmet kitchen with the finest tools, the freshest ingredients, the most
wonderful patrons -- and no chef.

So in this lesson and the two that follow, we'll apply our system to a real
problem: how to model and describe Sanskrit's sandhi changes. We'll do so by
learning how to apply basic {s vidhi} rules. And by learning how to do this, we
will complete our small system and be ready to examine the rest of the {cite
Aṣṭādhyāyī}.

{s-dfn vidhi} literally means "rule" or "command." Unlike {s saMjJA} rules
that merely assign a label, or {s paribhASA} rules that help us interpret rules
correctly, {s vidhi} rules are the core operations of the grammar. They add,
remove, and modify different terms. And by applying them in the correct
sequence, we create a correct Sanskrit expression.

How do we apply {s vidhi} rules in the correct sequence? This simple question 
is surprisingly deep and profound, and we cannot give a proper answer to it for
some time. A good rule of thumb is that we should apply the most specific rule
we can.

But for now, let's focus on more concrete matters: what {s vidhi} rules are,
how we define them, and how we can use them to define sandhi rules.


{h Conditions for sandhi}

As a reminder, {em sandhi} is the name for Sanskrit's various sound changes.
Sandhi occurs only in specific circumstances:

{rule

paraH saMnikarSaH saMhitA | 1.4.109
_
Close contact [of sounds] is called `saMhitA.

saMhitAyAm | 6.1.72
_
In `saMhitA, &hellip;

}

Rule 1.4.109 is a simple {s saMjJA} rule. But rule 6.1.72 is a new and
different kind of rule. What does this rule do? Simply, it adds extra context
for the rules that follow it. Such rules are called {s-dfn adhikAra}
("government") rules.

How many rules does an {s adhikAra} apply to? Each {s adhikAra} has a specific
scope, which we can usually determine from context or from the rule itself.
When in doubt, we can rely on expert commentaries to help us.

And as a quick note, perhaps you're wondering: how many different rule types
are there? Different authors classify them in different ways, but in this
series, we will use just five basic types: {s vidhi} (operation), {s saMjJA}
(definition), {s adhikAra} (government), {s paribhASA} (interpretation), and a
fifth type called {s atideza} (analogy) that we will use later on.


{h Our first sandhi rule}

Let's start the discussion with some small sandhi changes:

{ex

draupadI azvam icchati > draupadyazvam icchati
Draupadi wants a horse.

madhu asti > madhvasti
There is honey.

}

The basic idea is that if two non-similar vowels are in close contact ({s
saMhitA}), then the first vowel should become a semivowel.

How might we capture this change? Pāṇini offers the following rule, but it is
difficult to understand:

{rule

iko yaNaci | 6.1.77
ikaH yaN aci
Of `ik, there is `yaN in `ac [in `saMhItA].

}

Let's start with what we do know. We know that {s ik}, {s yaN}, and {s ac} are
all {s pratyAhAra}s:

{ul
    {li {s ik} refers to one of the vowels {s i}, {s u}, {s R}, and {s L}, and
    to any vowels similar to these four.}
    {li {s yaN} refers to one of the four semivowels: {s y}, {s v}, {s r}, and
    {s l}.}
    {li {s ac} refers to any vowel.}
}

We also know that Sanskrit words express meanings through {em inflection}. All
three of these {s pratyAhAra}s are Sanskrit nouns, and they express different
{dfn grammatical cases} through different noun endings. (Roughly, a noun's case
is the role it plays in the sentence.) So we have:

{ul
    {li the sixth case ({s ik-aH}), which can be translated as "of."}
    {li the first case ({s yaN}), which is usually the subject of a
    sentence.}
    {li the seventh case ({s ac-i}), which can be translated as "in."}
}

Because we know what the rule {em should} be, we can guess what the rule
is trying to express. But this guesswork doesn't feel satisfying. It feels like
something crucial is missing. 


{h How to interpret cases in formal grammar}  

The solution is to rely on three new {s paribhASA} rules. Together, they
describe how we should interpret these cases in the context of formal grammar:

{rule

SaSThI sthAneyogA | 1.1.49
SaSThI sthAne-yogA
The sixth case can signify `sthAne (in the place of).

tasminniti nirdiSTe pUrvasya | 1.1.66
tasmin iti nirdiSTe pUrvasya
When the seventh case is specified, [substitution is] of the previous.

tasmAdityuttarasya | 1.1.67
tasmAt iti uttarasya
When the fifth case [is specified, substitution is] of the next.

}

What do these rules mean? It's simple. In the context of a substitution:

{ul
  {li the sixth case marks the term that will be replaced}
  {li the fifth case marks the term that must appear before the substitution}
  {li the seventh case marks the term that must appear after it}
}

And by normal Sanskrit semantics, the first case will define the replacement.
With these principles in mind, we can reinterpret the case semantics in rule
6.1.77:

{ul
    {li {s ik} is in the sixth case ({s ikaH}), so it will be replaced.}
    {li {s yaN} in the first case ({s yaN}), so it is the substitute.}
    {li {s ac} in the seventh case ({s aci}), so it follows the substitution.}
}

Now rule 6.1.77 has a clearer meaning:

{rule

iko yaNaci | 6.1.77
ikaH yaN aci
An `ik vowel is replaced with `yaN when a vowel follows [in `saMhItA].

}


{h Substitution with two lists}

There is still a subtle problems with rule 6.1.77 above: which {s yaN} sound do
we use? We know that {s y} is the right choice, but the rule does not say so
explicitly. So it would be legal to do this:

{ex

* draupadI azvam icchati > [draupadrazvam] icchati
Draupadi wants a horse.

}

Our rule is too loose. How do we fix this?

Pāṇini offers several rules for performing a substitution correctly, but just
one is relevant to us here:

{rule

yathAsaMkhyamanudezaH samAnAm | 1.3.10
yathA-saMkhyam anudezaH samAnAm
Substitution of [items with] the same [size] is according to their relative
number.

}

More plainly, rule 1.3.10 states that if a rule says to replace one list (call
it {code A}) with another (call it {code B}) of the same size, what it really
means is that we replace the item 1 of {code A} with item 1 of {code B}, item 2
of {code A} with item 2 of {code B}, and so on for the rest of the list.

Now rule 6.1.77 has a clear, consistent meaning:

{rule

iko yaNaci | 6.1.77
ikaH yaN aci
An `ik vowel is replaced by its respective `yaN sound when a vowel follows [in
`saMhitA].

}

If we return to our original example, we know that {s ik} denotes the four
vowels {s i}, {s u}, {s R}, and {s L}. And we know that {s yaN} denotes the
four semivowels {s y}, {s v}, {s r}, and {s l}. So by rule 1.3.10, we see what
the correct replacements are:

{ex

i > y

u > v

R > r

L > l

}

Therefore, the replacement for {s i} is {s y}, and we get our desired result:

{ex

draupadI azvam icchati > draupadyazvam icchati
Draupadi wants a horse.

}


{h Review}

Understanding rule 6.1.77 took a lot of work and several extra rules. But these
new rules give us a precise and concise way to define different operations. We
will use these rules over and over as we continue to explore the {cite
Aṣṭādhyāyī}.

There's just one small catch: rule 6.1.77 has an important flaw. In the next
lesson, we will fix this flaw and build a basic model for vowel sandhi.
