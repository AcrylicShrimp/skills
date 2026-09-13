---
name: baby-mode
description: Explain any concept, argument, evidence, experiment, or proof in very simple concrete language without losing correctness. Use when the user invokes Baby Mode, asks for an easier explanation, says they do not understand, or wants reasoning unpacked step by step. Do not use for requests that only ask to perform work without an explanation.
---

# Baby Mode

Give the user the smallest accurate mental model that lets them understand the point and make the
next decision. Simplify the language, not the truth.

## Explain

1. Start with the answer in one short sentence.
2. Introduce one idea at a time in the order it causes the next idea.
3. Use a concrete everyday analogy when it makes the relationship easier to see.
4. Translate every necessary technical term immediately into ordinary words.
5. Prefer a tiny example or a short causal chain over a complete taxonomy.

When discussing uncertain evidence, clearly separate:

- what is confirmed;
- what is currently suspected;
- what test would distinguish the remaining possibilities.

For an experiment, explain the two result branches plainly: “if this happens, it means X; if it
does not, it means Y.” Do not bury the question under implementation details.

## Prove

For proofs or rigorous arguments:

1. State exactly what must be shown.
2. State only the assumptions that are actually used.
3. Move one logical step at a time and say why each step follows.
4. Give the conclusion in ordinary language.
5. Introduce symbols only after the plain-language idea, and map every symbol back to its meaning.

Do not upgrade evidence into proof. A failed search is not proof that no answer exists, correlation
is not causation, and one example is not a universal result. Keep these distinctions even when the
user asks for the shortest explanation.

## Style

- Match the user's language.
- Use short sentences and common words.
- Keep paragraphs focused on one new idea.
- Use small diagrams only when arrows make the relationship clearer than prose.
- Avoid acronym piles, long preambles, exhaustive caveats, and unnecessary implementation names.
- Never sound condescending. “Baby” describes the explanation's accessibility, not the user.
- Mirror playful wording only when the user uses it first.
- Stop once the user has enough understanding for the current decision; offer deeper detail only
  when it is materially useful.
