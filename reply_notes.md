Dear Editor,

Thank you for the opportunity to revise this manuscript following the review. We
appreciate the thoughtful and constructive comments provided by the two
reviewers. We have addressed these comments below and incorporated them into the
manuscript.

# Comments by Referee: 1

> This manuscript proposes a modification to a widely employed evolutionary model, commonly utilized for the study of repeated interactions and direct reciprocity. The authors advocate for the adoption of a discounted expected payoff as the fitness metric for behavioral (or cultural, depending on the definition) transmission. Their argument posits that this approach offers a more realistic constraint, reflecting imperfect individual memory. Despite limited memory, the study demonstrates the feasibility of obtaining results akin to the original model without incorporating discounting.

> I commend the authors for the excellent work and clarity of their article. I believe this work is both relevant and novel and I recommend minor revisions. However, I believe there are a few things that could be improved. 

We thank the reviewer for their kind words. Thank you sincerely for your insightful and constructive review.

> Firstly, there is some redundancy in the arguments, such as the repetition in the abstract regarding the significance of individuals remembering recent payoffs. Similar redundancies exist in the introduction (see the penultimate and last paragraph of the introduction). 

We agree that there are arguments that are repeated. We have made changes
accordingly. Specifically, we removed the last sentence of the abstract and
reworded the last paragraphs of the introduction.

> Also, consider separating the last paragraph of the Discussion into a dedicated Conclusion section for more clarity.

We thank the reviewer for their suggestion. We have now divided the discussion into separate sections for discussion and conclusion.

I slightly disagree with the reviewer's suggestion to only separate the last
paragraph. In my suggestion, I separate the discussion section earlier on.
However, feel free to change it.

> Secondly, I am curious at how much difference there would be in the results between the author's discounted payoff model and interactions in a regular graph where individuals are connected to t neighbors. While intuitively there should be differences, I the difference is bounded.

We thank the reviewer for their comment. It is indeed true that in our model, we assume that a player considers only a certain number of interactions with specific members of the population for calculating their updating payoffs. In this regard, the idea of a structured population follows the same logic. However, in our model, we assume that when the given members are selected, their probability of being chosen among all members of the population is equal. This is where the difference between the two approaches arises. We believe that this is an intriguing idea, but it constitutes a scientific project in its own right. It is a topic we would like to explore in future research endeavors.


> Concerning Figures 2 and 3, acknowledging the stochastic nature of the model and assuming that values are estimations, I suggest incorporating information on uncertainty. For clarity, provide the number of simulations conducted to generate each figure's results. Additionally, in Figure 3, indicate the duration of the simulations and the parameters used, as has been done in Figure 2.

Both comments have been addressed.

> Lastly, I concur with the authors on the importance of balancing the study of direct reciprocity and memory-n strategies (I propose [1] as a good reference for n-memory strategies in EGT).

Thank you for recommending the reference. We have included it to our manuscript.

>  Given that a memory of three interactions appears to be enough to recover results close to the classical model, I would like the authors to explain further why they believe that this theoretical result is crucial for making informed deductions about reciprocity in natural systems. Would it be possible that the effect of memory is also dependent on the game? That is, would the effect be stronger in an iterated snow-drift game than in a iterated prisoner’s dilemma.

We have included a dedicated section on the snowdrift game in the Supplementary Information. We further discuss your comment in the _corresponding_ section.


# Comments by Referee: 2

> It's a wonderfully simple and clever contribution to evolutionary game theory, with a robust supplement to complement a minimalistic analysis in the main text. The authors contend with the reasonable constraint that players may not remember all prior interaction partners, or even all prior rounds of interaction with a given partner (for iterated games), when choosing to learn or imitate strategies. The main result is that longer memories are generally more permissive for cooperative outcomes in evolving populations; but cooperation can still persist (with a more constrained set of strategies) even when memories are short.

> Starting first from the simple case of GTFT vs ALLD, the authors analyze what level of generosity makes cooperation stochastically stable, and they find that having a very short memory (of only the last round of play) puts more stringent conditions on a strategy to make cooperation stable. The same basic result is observed in simulations, across the full space of reactive strategies under strong selection and weak mutation.

> The authors also consider regimes that are intermediate to extremely short memories vs infinitely long memories -- such as memory of the last two rounds with a single partner, or the last round with two different partners, or last two rounds of two partners, or all rounds of one partner. The same basic trends hold in these intermediate regimes: cooperation is still possible with these intermediate memory types, but less so than with arbitrary memories.

> Overall it's a nice paper and I recommend publication. I especially like the Discussion section on the mechanistic interpretation of "memory" in this context, and on cognitive constraints during learning.

We thank the reviewer for their kind words. Thank you for your valuable feedback and insightful review.

>  For revision, I have some questions about extending the analysis outside of the strict regimes studies, and also some questions about interpretation:

> 1. (comment) All of the mathematical analysis is constrained to GTFT, whereas simulations are required for studying the full space reactive or all memory-1 strategies. Line 207 should be edited accordingly, because it seems to suggest analytical results for all reactive strategies.

I believe the reviewer is referring to `Beyond reactive strategies`. However,
this section follows the numerical results section where we allow for all
reactive strategies. I'm not sure how to address this comment. Should we
consider renaming it to `Evolutionary dynamics of reciprocity beyond reactive strategies`?

> 2. (extension) What happens when selection is weaker? The entire analysis is done in the limit of strong selection and weak mutation, which makes things simple. But this leads to some pathologies, such as the non-dependence on payoff matrix in the case of a player who only remembers the last rounds of a single opponent. I believe that the simulations are also done in the limit of strong selection (is that correct? please clarify).  Can the authors tell us anything about what happens when selection is not infinitely strong?  What about the opposite limit of weak selection -- where the zeroth-order (in beta) analysis will predict no difference between a long and short memory?

AM

> 3 (comment). The coincidence of the condition for stochastic stability in a scenario with memory of all rounds of the last co-player, with the result for all rounds of all co-players, is presumably not coincidental, but a reflection of the fact that the calculation is made in the N->infinity limit with weak mutation. So a random last opponent is the same the average over all opponents.  The authors should explain this logic (if they agree), or otherwise explain this result intuitively.

CH

> 1. (extension). A very short summary of the main result is: longer memory,  cooperation is more stable.  But what if memory is costly (which it surely is)? Can the authors say anything analytic if there is a fixed cost to having a long memory, even in the simple case of GTFT vs ALLD (but when each strategic type can either pay a cost and have a long memory, or pay no cost and remember only the last round)? Can the authors say anything about the evolution of (costly) memory, especially as it provides for greater expected population mean fitness?

This is a great point raised by the reviewer. We find this extension very
interesting for future work. However, we currently find no straightforward way
to include such a cost in our current model.

_Can we say anything about the evolution of costly memory?_

> 2. (interpretation). The comparison between temporally discounted future rewards vs actual rewards from the past is fascinating. It is mindblowing to realize that the actual payoff from the last round is an unbiased estimator of the expected (normalized) discounted payoff. And this gives a mechanistic reason for imitation based on last-round payoff. Great stuff.

We thank the reviewer for their positive feedback!

But there seems to be a subtle inconsistency in how imitation is implemented in the short-memory case -- meaning, when a player can only remember the very last round. Even in this case, when imitation is based only on the last round, a player can nonetheless imitate the entire strategy of their partner -- which requires knowledge of their entire strategy. But how could a player with one-round memory ever infer their co-player's strategy?  This problem is discussed by authors a bit (lines 291-301), but I don't think they really address or resolve this issue directly. It seems like they assume that a short-memory player can just copy their co-players full strategy, which in principle would require observation and recall all game histories. Can the authors clarify this inconsistency, or at least acknowledge it more clearly?

CH. We agree with this comment by the reviewer. We have added further discussion on this point.