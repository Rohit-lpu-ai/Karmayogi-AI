"""Lesson content for pack ``demo-3`` (synthetic, written for product evaluation; every figure is invented).

Structure: course external_ref -> modules -> lessons. Each lesson is (title, lesson_type, minutes, Markdown body).
Lesson types: ``reading`` (explanation), ``worked_example`` (a solved case), ``practice_check`` (questions with the
answers below them). Bodies use plain Markdown only: headings, lists, tables, emphasis. No HTML, no links.
"""

from __future__ import annotations

Lesson = tuple[str, str, int, str]
Module = tuple[str, str, tuple[Lesson, ...]]

CONTENT: dict[str, tuple[Module, ...]] = {
    "DEMO-C2-01": (
        ("Measures of centre", "Choose the summary that represents a typical case.", (
            ("Mean, median and mode", "reading", 8, """
A summary figure answers one question: *what is typical?* Three measures answer it differently.

- **Mean**: the total divided by the count. It uses every value, so one very large value pulls it upward.
- **Median**: the middle value once the data are sorted. Half the values lie below it and half above.
- **Mode**: the most frequent value. Useful for categories such as the most common household size.

## Which one to use

| Data shape | Prefer | Why |
|---|---|---|
| Roughly symmetric, no extreme values | Mean | Uses all the information |
| Skewed (incomes, farm sizes, travel times) | Median | Not pulled by a few extreme values |
| Categories or discrete counts | Mode | "Most common" is the natural question |

## A quick signal

If the mean is well above the median, a few large values are stretching the distribution to the right. Report the
median as "typical" and mention the mean only with that explanation.
"""),
            ("Worked example: a skewed district table", "worked_example", 10, """
A district office reports monthly household spending for nine sampled households (invented figures, in rupees):

`8,200  8,900  9,100  9,400  9,800  10,300  10,900  11,500  64,000`

## Step 1 - compute both measures

- Sum = 1,42,100, so the **mean** = 1,42,100 / 9 = **15,789**.
- Sorted, the fifth value is the **median** = **9,800**.

## Step 2 - look at the gap

The mean is about 61% higher than the median. One household at 64,000 explains almost all of the difference.

## Step 3 - write the summary

> Typical monthly spending in the sample was about Rs 9,800 (median). The mean, Rs 15,789, is raised by one
> household with unusually high spending.

## What to take away

Never report "average spending" from skewed data without saying which average you used.
"""),
        )),
        ("Spread and summaries", "Describe how far values vary, then write a fair summary.", (
            ("Range, IQR and standard deviation", "reading", 9, """
A centre without a spread hides half the story. Two districts can share a median of 40 and still differ widely.

- **Range** = largest minus smallest. Simple, but driven entirely by the two extremes.
- **Interquartile range (IQR)** = third quartile minus first quartile. It covers the middle half of the data and
  ignores extremes, so it pairs naturally with the median.
- **Standard deviation** measures the typical distance from the mean. It pairs with the mean and is sensitive to
  extreme values in the same way.

## Pairing rule

| If you report | Report spread as |
|---|---|
| Median | IQR (or the quartiles themselves) |
| Mean | Standard deviation |

## Weighted means

When figures come grouped - for example average scores for blocks of different sizes - weight each group mean by
its count. An unweighted mean of group means treats a block of 20 people the same as a block of 2,000.
"""),
            ("Practice check: choose and describe", "practice_check", 8, """
Try each question before reading the answers below.

1. Waiting times at a clinic (minutes): 5, 6, 6, 7, 8, 9, 55. Which measure of centre should a note use?
2. Block A has 200 staff with an average of 12 training hours; block B has 50 staff with an average of 20 hours.
   What is the combined average?
3. A note says "spread was low (SD = 2.1)" next to a median. What is wrong?

---

## Answers

1. **Median (7 minutes).** The value 55 makes the mean (13.7) unrepresentative.
2. **13.6 hours.** (200 x 12 + 50 x 20) / 250 = 3,400 / 250. The unweighted answer, 16, is wrong.
3. **Mismatched pair.** A median should be paired with quartiles or the IQR; SD belongs with the mean.
"""),
        )),
    ),
    "DEMO-C2-02": (
        ("Before you quote a figure", "Units, periods and footnotes decide what a number means.", (
            ("The anatomy of a statistical table", "reading", 7, """
Read a table in this order before quoting anything from it:

1. **Title** - what is measured, where and when.
2. **Unit** - numbers, thousands, lakh, percent, per 1,000. Often in the title or a column header.
3. **Reference period** - calendar year, financial year, a survey round, or a single date.
4. **Column and row headers** - which groups are compared.
5. **Footnotes and symbols** - provisional figures, revised series, suppressed cells, changes in coverage.
6. **Source line** - who produced the figures and from which collection.

## The three most common errors

- Quoting "4,512" when the unit is **thousands** (so 45.12 lakh).
- Mixing **provisional** and **final** figures in one comparison.
- Comparing **percentages with different bases** (for example percent of households versus percent of persons).
"""),
            ("Worked example: reading an enrolment table", "worked_example", 10, """
An invented table: *Enrolment in training centres, by region (thousands), 2024-25 (P)*

| Region | Men | Women | Total |
|---|---|---|---|
| North | 41.2 | 36.8 | 78.1 |
| South | 29.5 | 33.4 | 62.9 |
| **All** | 70.7 | 70.2 | 141.0 |

Footnote: *P = provisional. Totals may not add because of rounding.*

## Reading it correctly

- North total: 41.2 + 36.8 = 78.0, but the table shows **78.1**. That is rounding, not an error.
- The figures are **thousands**: North enrolled about 78,100 people.
- They are **provisional**; a note should say so.

## A correct sentence

> Provisional figures show about 1.41 lakh enrolments in 2024-25, with women slightly outnumbering men in the South.
"""),
        )),
        ("Comparing correctly", "Choose the right denominator and quote accurately.", (
            ("Denominators and fair comparisons", "reading", 8, """
Counts are rarely comparable on their own. A region with more people will usually have more of everything.

## Ask: per what?

| Question | Suitable denominator |
|---|---|
| Is training reaching more people? | Eligible population |
| Is a service busier? | Service points or staff |
| Has the share of women risen? | Total enrolment in the same group |

## Check that the denominator matches

A share of women among **enrolled** people and a share of women among **eligible** people answer different questions.
Say which one you report.

## Rounding and totals

Components may not add to totals after rounding. Do not "correct" published totals; quote them as published and
keep the footnote.
"""),
            ("Practice check: table reading", "practice_check", 7, """
Use the enrolment table from the worked example.

1. What was total enrolment in the South, in people?
2. A draft says "North had 15.2 more enrolments than the South." What is wrong?
3. Can you conclude that training reaches a larger share of people in the North?

---

## Answers

1. **About 62,900 people** (62.9 thousand).
2. **Missing unit.** The difference is 15.2 *thousand*, and the figures are provisional.
3. **No.** You need the eligible population of each region to compare shares; counts alone cannot show reach.
"""),
        )),
    ),
    "DEMO-C2-03": (
        ("Rates and percentages", "Turn counts into comparable rates.", (
            ("Rates, ratios and proportions", "reading", 8, """
- A **proportion** is a part of a whole: 180 of 600 trainees completed a course, a proportion of 0.30 or 30%.
- A **ratio** compares two quantities: 450 women to 500 men is a ratio of 0.9 : 1.
- A **rate** relates events to a population over time: 12 incidents per 1,000 workers per year.

## Choosing the multiplier

Pick the multiplier that avoids tiny decimals: per 100 (percent), per 1,000, or per 1,00,000 for rare events.

## Worked conversion

96 cases in a population of 4,80,000:

`96 / 4,80,000 x 1,00,000 = 20 per lakh population`
"""),
            ("Percentage change versus percentage points", "reading", 9, """
This is the single most common wording error in statistical notes.

- **Percentage change** compares a new value with an old one: (new - old) / old x 100.
- **Percentage points** are the simple difference between two percentages.

## Example

A completion rate rises from **40%** to **50%**.

- The change is **10 percentage points**.
- The percentage change is (50 - 40) / 40 x 100 = **25%**.

Both statements are true; they answer different questions. Writing "increased by 10%" is wrong.

## Compound changes

Changes over several periods multiply, they do not add. +10% then +10% is 1.10 x 1.10 = 1.21, a **21%** increase.
"""),
        )),
        ("Describing change precisely", "Write sentences that cannot be misread.", (
            ("Worked example: an indicator note", "worked_example", 10, """
Invented figures for a skills indicator:

| Year | Trained workers | Workforce | Rate (per 1,000) |
|---|---|---|---|
| 2023 | 5,520 | 4,60,000 | 12.0 |
| 2024 | 6,440 | 4,90,000 | 13.1 |

## Step 1 - the count

(6,440 - 5,520) / 5,520 x 100 = **16.7%** more trained workers.

## Step 2 - the rate

The rate rose from 12.0 to 13.1 per 1,000: an increase of **1.1 per 1,000**, or a rise of about **9%** in the rate.

## Step 3 - the sentence

> The number of trained workers rose by 16.7%. Because the workforce also grew, the rate rose less, from 12.0 to
> 13.1 per 1,000 workers.
"""),
            ("Practice check: rates and change", "practice_check", 8, """
1. Unemployment falls from 8% to 6%. Give the change in percentage points and as a percentage change.
2. Prices rise 5% one year and 5% the next. What is the two-year increase?
3. 42 accidents occur among 2,10,000 workers. Express this per lakh workers.

---

## Answers

1. **2 percentage points**; a percentage change of **-25%** ((6 - 8) / 8).
2. **10.25%** (1.05 x 1.05 = 1.1025), not 10%.
3. **20 per lakh workers** (42 / 2,10,000 x 1,00,000).
"""),
        )),
    ),
    "DEMO-C2-04": (
        ("Shapes of distributions", "See what the average hides.", (
            ("Skewness and outliers", "reading", 9, """
A histogram shows how values are spread. Three shapes cover most practical cases:

- **Symmetric**: mean and median are close. Heights or measurement errors often look like this.
- **Right-skewed**: a long tail of large values; mean above median. Incomes, landholdings, waiting times.
- **Left-skewed**: a long tail of small values; mean below median. Scores on an easy test.

## Outliers

An outlier is a value far from the rest. Common rule: a value more than 1.5 x IQR below the first quartile or above
the third quartile deserves a check.

An outlier is a **question, not a verdict**. It may be an error (an extra zero) or a real, important case.
Investigate before removing anything, and document the decision.
"""),
            ("Percentiles and the IQR", "worked_example", 10, """
Invented daily output for 11 units, sorted: `12 14 15 15 16 18 19 21 22 24 41`

## Quartiles

- Median (6th value) = **18**
- First quartile (median of the lower five) = **15**
- Third quartile (median of the upper five) = **22**
- IQR = 22 - 15 = **7**

## Outlier check

Upper fence = 22 + 1.5 x 7 = 32.5. The value **41** is above it and should be checked.

## Percentiles in words

"The 90th percentile is 24" means 90% of units produced 24 or less. Percentiles describe position without being
distorted by the one unit at 41.
"""),
        )),
        ("Normal and robust summaries", "Use the normal rule carefully and prefer robust measures when data are skewed.", (
            ("The 68-95-99.7 rule", "reading", 8, """
For data that are roughly **normal** (bell-shaped and symmetric):

| Within | Share of values |
|---|---|
| 1 standard deviation of the mean | about 68% |
| 2 standard deviations | about 95% |
| 3 standard deviations | about 99.7% |

## Example

Test scores with mean 60 and SD 8: about 95% of candidates score between 44 and 76.

## When not to use it

The rule fails for skewed data. With incomes, "mean plus two SD" can exceed almost every real value while many
people sit far below the mean. For skewed data, describe the median and the quartiles instead.
"""),
            ("Practice check: variability", "practice_check", 8, """
1. A distribution has mean 52 and median 38. What shape is it likely to have?
2. Quartiles are 30 and 50. Is a value of 85 a possible outlier?
3. Scores are roughly normal with mean 70 and SD 5. About what share scored above 80?

---

## Answers

1. **Right-skewed**: a tail of large values pulls the mean above the median.
2. **Yes.** IQR = 20; upper fence = 50 + 30 = 80, and 85 lies above it. Check it before deciding.
3. **About 2.5%.** 80 is two SD above the mean; 95% lie within two SD, leaving 5% split between both tails.
"""),
        )),
    ),
    "DEMO-C2-05": (
        ("How probability samples work", "Designs and why randomness matters.", (
            ("Four basic designs", "reading", 10, """
In a **probability sample** every unit in the population has a known, non-zero chance of selection. That is what
lets us estimate the population and measure the uncertainty.

| Design | How it works | Typical use |
|---|---|---|
| Simple random | Every unit equally likely | Small, listed populations |
| Systematic | Every k-th unit after a random start | Lists in a natural order |
| Stratified | Separate samples within groups (strata) | Guarantee coverage of regions or groups |
| Cluster | Select groups (villages, blocks), then units within | Spread-out populations, lower travel cost |

## Trade-offs

Stratification usually **improves** precision. Clustering usually **reduces** precision for the same sample size,
because units in a cluster tend to be alike - but it can cut fieldwork cost sharply.
"""),
            ("Sampling error and sample size", "reading", 9, """
Two samples from the same population give slightly different estimates. That variation is **sampling error**.

## What changes it

- **Sample size**: precision improves with the *square root* of the sample size. Quadrupling the sample halves the
  standard error.
- **Variability** in the population: more varied populations need larger samples.
- **Design**: stratification can reduce error; clustering usually increases it.

## Reading a margin of error

"38% plus or minus 3 points" means the survey design gives a range of roughly 35% to 41% at the stated confidence
level. It covers **sampling error only**, not errors from poor questions or non-response.
"""),
        )),
        ("Bias and design notes", "Errors that a bigger sample cannot fix.", (
            ("Worked example: coverage bias", "worked_example", 10, """
A department wants the share of small enterprises using digital payments. It samples from a list of enterprises
**registered for a scheme** (invented scenario).

## The problem

Enterprises that never registered are missing from the frame. They are likely to be smaller and less digital.

## The effect

Even a very large sample from this list will **overestimate** digital payment use for all small enterprises. A larger
sample makes the estimate more precise, not less biased.

## What a good note says

> Estimates refer to enterprises registered for the scheme. Unregistered enterprises are not covered, and their
> use of digital payments may differ.
"""),
            ("Practice check: sampling", "practice_check", 8, """
1. You need reliable estimates for each of five regions. Which design helps most?
2. A survey doubles its sample size. By roughly how much does the standard error fall?
3. A telephone survey reaches only households with phones. Which error is this, and does a bigger sample fix it?

---

## Answers

1. **Stratified sampling** by region, with enough units in each stratum.
2. **By about 29%**: the standard error is multiplied by 1 / square root of 2, about 0.71.
3. **Coverage bias.** A larger sample does not fix it; the frame itself excludes some households.
"""),
        )),
    ),
    "DEMO-C2-06": (
        ("Design and allocation", "From frame to a sample plan.", (
            ("Choosing a design and allocating the sample", "reading", 10, """
A survey plan answers four questions in order:

1. **Frame**: which list or area map represents the population, and what does it miss?
2. **Strata**: which groups need their own reliable estimates?
3. **Stages**: will you select clusters first (villages, enumeration blocks) and then households?
4. **Allocation**: how many units go to each stratum?

## Allocation options

| Method | Rule | Effect |
|---|---|---|
| Proportional | Share of sample = share of population | Good national estimates |
| Equal | Same size in every stratum | Good estimates for small strata |
| Compromise | Between the two | Balances both needs |

Record every choice in the design note; users need it to interpret the estimates.
"""),
            ("Worked example: allocating 1,200 households", "worked_example", 12, """
Three invented strata with household counts: Urban 60,000; Rural plains 30,000; Hill areas 10,000.

## Proportional allocation

Urban 720, Plains 360, Hills **120**. With 120 households, hill estimates will be imprecise.

## Equal allocation

400 each. Hill estimates improve, but national estimates need **weights**, because hill households are now
over-represented (a third of the sample, but a tenth of all households).

## A compromise

Urban 600, Plains 360, Hills 240. Hills get a usable sample; weights correct the national figure.

## Weights

Each sampled household represents (stratum households / stratum sample). Urban: 60,000 / 600 = **100**;
Hills: 10,000 / 240 = about **42**.
"""),
        )),
        ("Fieldwork, non-response and limitations", "Keep quality visible from collection to publication.", (
            ("Monitoring fieldwork and weighting", "reading", 9, """
## During fieldwork

Track by team and area, every week:

- **Response rate** = completed interviews / eligible units contacted.
- **Refusals and non-contacts** separately: they have different fixes.
- **Interview duration**: unusually short interviews can signal skipped sections.
- **Back-checks**: re-contact a small random share of households to verify key answers.

## After fieldwork

- **Design weights** undo unequal selection chances.
- **Non-response adjustments** increase weights of similar responding units. They reduce bias only if responders
  and non-responders within an adjustment group are alike - an assumption to state, not a fact.
"""),
            ("Practice check: running a survey", "practice_check", 9, """
1. Team A reports a 96% response rate and very short average interviews. What should you do?
2. Why do equal allocations require weights for national estimates?
3. Name two limitations a survey note should state.

---

## Answers

1. **Investigate before accepting**: run back-checks and review timings; high response with short interviews can
   indicate incomplete or fabricated interviews.
2. Units in small strata are **over-represented** relative to their population share; weights restore the balance.
3. For example: **frame coverage** (who is missing) and **non-response** (and the adjustment used). Sampling error
   and reference period are also common.
"""),
        )),
    ),
    "DEMO-C2-07": (
        ("Designing checks", "Catch errors before they reach a table.", (
            ("Range, consistency and trend checks", "reading", 9, """
| Check | Question | Example |
|---|---|---|
| Range | Is the value possible? | Age 0-110; percentage 0-100 |
| Consistency | Do related values agree? | Components add to the reported total |
| Trend | Is the change plausible? | A 300% jump in monthly admissions |
| Duplicate | Is the same report counted twice? | Identical rows with one ID |
| Carry-forward | Was last period copied? | The same figures for six months |

## Hard and soft checks

- A **hard** check fails only for impossible values - stop and correct.
- A **soft** check flags unusual values - query the source, then accept or correct with a note.

Every correction needs a record: what changed, who decided and why.
"""),
            ("Worked example: a monthly report that fails checks", "worked_example", 10, """
Invented monthly returns from a block office:

| Month | Registered | Approved | Rejected | Pending |
|---|---|---|---|---|
| Apr | 820 | 610 | 90 | 120 |
| May | 865 | 640 | 95 | 130 |
| Jun | 865 | 640 | 95 | 130 |
| Jul | 910 | 1,020 | 60 | 80 |

## Findings

- **June equals May** in every column: possible carry-forward. Query the office.
- **July approved (1,020) exceeds registered (910)**. Approved + rejected + pending = 1,160, not 910. A consistency
  failure; perhaps approvals include earlier backlog. Ask for the definition.

## Decision

Hold June and July, record both queries, and publish April-May with a note that later months are under verification.
"""),
        )),
        ("Non-response and reporting quality", "Measure what is missing and say so.", (
            ("Non-response and its effects", "reading", 8, """
- **Unit non-response**: a whole return or interview is missing.
- **Item non-response**: some questions are unanswered.

## Why it matters

If non-responders differ from responders, estimates are biased. Offices with the heaviest workload may be the ones
that report late - so an average based on early returns can understate workload.

## What to report

- The **response rate** for the release.
- How missing values were handled: excluded, imputed, or carried forward (and why).
- Any known **differences** between responding and non-responding units.
"""),
            ("Practice check: validation", "practice_check", 8, """
1. A district reports 104% of households covered. Hard or soft check, and what next?
2. Admissions jump from 1,200 to 3,900 in one month. What do you do?
3. Only 70% of offices reported on time. What must the release note say?

---

## Answers

1. **Hard check** (impossible above 100%). Query the numerator and denominator before publishing.
2. **Soft check**: query the source. Accept with a note if there is a real reason (for example a new facility).
3. The **response rate** (70%), how missing offices were treated, and that estimates may change when late returns
   arrive.
"""),
        )),
    ),
    "DEMO-C2-08": (
        ("What an index measures", "Base years and index points.", (
            ("Reading an index", "reading", 8, """
An index expresses a value **relative to a base period** set to 100.

- An index of **128** means the measured quantity is 28% above the base period.
- It does **not** say anything about the level itself - only the change from the base.

## Index points versus percentage change

From 128 to 136 is a rise of **8 index points**, but a percentage change of (136 - 128) / 128 x 100 = **6.25%**.
Report percentage changes between periods; index points depend on how far you are from the base.
"""),
            ("Worked example: a weighted index", "worked_example", 12, """
An invented three-group price index, base year = 100:

| Group | Weight | Index this year |
|---|---|---|
| Food | 0.45 | 132 |
| Housing | 0.30 | 118 |
| Transport | 0.25 | 124 |

## Step 1 - weighted average

0.45 x 132 + 0.30 x 118 + 0.25 x 124 = 59.4 + 35.4 + 31.0 = **125.8**

## Step 2 - interpret

Prices overall are about 25.8% above the base year. Food contributes most, because it has both the largest
weight and the largest rise.

## Step 3 - contribution of food

Food's contribution to the 25.8-point rise = 0.45 x (132 - 100) = **14.4 points**, more than half.
"""),
        )),
        ("Weights and change", "Why weights matter.", (
            ("Why weights matter", "reading", 8, """
Weights represent the **importance** of each item in the basket - usually its share of spending in a reference period.

## Same prices, different weights

If food prices rise 20% and other prices 5%:

| Household type | Food weight | Index change |
|---|---|---|
| Food share 0.60 | 0.60 | 0.60 x 20 + 0.40 x 5 = **14%** |
| Food share 0.30 | 0.30 | 0.30 x 20 + 0.70 x 5 = **9.5%** |

The same price movements mean different things for different households. That is why the weight reference period
and population must be documented.
"""),
            ("Practice check: index numbers", "practice_check", 8, """
1. An index moves from 150 to 159. What is the percentage change?
2. Two groups with weights 0.6 and 0.4 have indices 110 and 130. What is the combined index?
3. A note says "prices rose by 9 points, i.e. 9%". What is wrong?

---

## Answers

1. **6%** ((159 - 150) / 150 x 100).
2. **118** (0.6 x 110 + 0.4 x 130).
3. **Points are not percent** unless the starting index is 100. From 150, 9 points is 6%.
"""),
        )),
    ),
    "DEMO-C2-09": (
        ("Rebasing", "Move an index to a new reference year.", (
            ("Why and how to rebase", "reading", 9, """
Rebasing re-expresses an index so that a **new reference period** equals 100. Movements stay the same; only the
reference changes.

## Formula

`rebased index = old index / old index in new base period x 100`

## Example

Old series (2012 = 100): 2020 = 140, 2024 = 168. Rebased to 2020 = 100:

- 2020: 140 / 140 x 100 = **100**
- 2024: 168 / 140 x 100 = **120**

The percentage change from 2020 to 2024 is 20% in both series.

Rebasing the reference period is different from **updating weights**, which changes the basket itself.
"""),
            ("Worked example: linking two series", "worked_example", 12, """
A new series with updated weights starts in 2022. Both series exist for the **overlap year** 2022 (invented values).

| Year | Old series (2012 = 100) | New series (2022 = 100) |
|---|---|---|
| 2021 | 152 | - |
| 2022 | 160 | 100 |
| 2023 | - | 106 |

## Linking factor

160 / 100 = 1.6

## Express 2023 on the old base

106 x 1.6 = **169.6**, a continuous long series.

## Or express 2021 on the new base

152 / 1.6 = **95.0**

State in the release that the long series is **linked**, and from which year the new weights apply.
"""),
        )),
        ("Explaining index movements", "Updates and plain-language explanations.", (
            ("Weight updates and their effect", "reading", 8, """
Spending patterns change: shares of services and communication grow, some goods shrink. Old weights then
over-represent items people buy less.

## Typical effects of a weight update

- Items with rising shares get more influence on the headline index.
- The headline change for a period can differ slightly between old and new weights.
- Comparisons across the update need the linked series, not the raw old and new indices.

## Explaining to users

Tell users *what changed* (base year, weights, items), *from when*, and *how to compare* (use the linked series).
"""),
            ("Practice check: maintaining an index", "practice_check", 9, """
1. An index is 125 in 2019 and 150 in 2024 (base 2015 = 100). Rebase 2024 to 2019 = 100.
2. The overlap-year values are 180 (old) and 100 (new). The new series shows 108 a year later. What is that on the
   old base?
3. A user compares an old-series value with a new-series value directly. What do you tell them?

---

## Answers

1. **120** (150 / 125 x 100).
2. **194.4** (108 x 1.8).
3. **Use the linked series.** The two series have different reference periods (and weights), so raw values are not
   comparable.
"""),
        )),
    ),
    "DEMO-C2-10": (
        ("Titles, tables and charts", "Help readers find the right number.", (
            ("Titles that answer what, where and when", "reading", 7, """
A good title lets a reader understand the figure without the surrounding text.

| Weak | Better |
|---|---|
| Enrolment | Enrolment in training centres by region, 2024-25 (thousands, provisional) |
| Trend chart | Share of women trainees, 2019-2024 (percent) |

## Checklist

- What is measured, and the **unit**.
- **Where** and **when** (reference period).
- Any **status** (provisional, revised).

## Charts that do not mislead

- Bar charts start at **zero**; truncated bars exaggerate differences.
- Keep the **same scale** when charts are compared side by side.
- Use a line chart for time series, bars for comparing categories.
"""),
            ("Worked example: fixing a draft chart", "worked_example", 10, """
Draft: a bar chart titled "Performance" shows two districts, 71% and 74%, with the vertical axis starting at 70%.
The second bar looks four times taller.

## Problems

1. The title says nothing about the measure, unit or period.
2. The axis starts at 70%, exaggerating a 3-point difference.
3. No note about the sample, so readers cannot judge whether 3 points is meaningful.

## Revised

- Title: *Share of applications processed within 30 days, by district, April-June 2025 (percent)*
- Axis from 0 to 100.
- Note: *Based on all applications received (administrative data). Difference of 3 percentage points.*
"""),
        )),
        ("Caveats and interpretation", "Say what the figures can and cannot show.", (
            ("Reliability cautions and causation", "reading", 8, """
## Reliability

Flag estimates that rest on small samples or have large margins of error, for example:

> Estimate based on fewer than 50 responses; interpret with caution.

## Association is not causation

"Districts with more training centres have higher employment" does not show that centres **cause** employment.
Larger, urban districts may have both. Use neutral verbs:

| Avoid | Prefer |
|---|---|
| led to, caused, drove | was associated with, coincided with |
| proves | is consistent with |
"""),
            ("Practice check: communication", "practice_check", 7, """
1. Rewrite the title "Rates" for a table of accident rates per lakh workers by state in 2024.
2. A chart comparing 48% and 52% starts its axis at 45%. What is the risk?
3. Rewrite: "The new scheme caused a rise in enrolment."

---

## Answers

1. *Accident rate per lakh workers, by state, 2024.*
2. **Exaggerated difference**: the bars suggest a gap far larger than 4 percentage points. Start at zero.
3. For example: *Enrolment rose after the scheme was introduced; other factors may also have contributed.*
"""),
        )),
    ),
    "DEMO-C2-11": (
        ("Averages and percentages", "The two error types that most often reach draft notes.", (
            ("Misleading averages", "reading", 7, """
## Pitfall 1 - the wrong average

A mean from skewed data describes almost nobody. Report the median as typical and explain large gaps.

## Pitfall 2 - averaging averages

Averaging district rates without weighting treats a district of 5,000 people like one of 5,00,000.
Recompute from totals: total events / total population.

## Pitfall 3 - percentage-point confusion

A rise from 20% to 25% is **5 percentage points** and a **25%** relative increase. "Rose by 5%" is wrong.
"""),
            ("Comparing groups fairly", "worked_example", 9, """
Invented figures: two offices processed complaints.

| Office | Complaints | Resolved in 15 days | Share |
|---|---|---|---|
| A | 40 | 36 | 90% |
| B | 1,200 | 960 | 80% |

## Tempting conclusion

"Office A performs better."

## Checks before concluding

- **Size**: 40 cases make A's share volatile; two more late cases would move it by 5 points.
- **Mix**: B may receive more complex complaints.
- **Period**: are both figures for the same months?

## Better sentence

> Office A resolved 90% of 40 complaints within 15 days and Office B 80% of 1,200. A's figure rests on few cases,
> and the offices may handle different types of complaint.
"""),
        )),
        ("Checking a draft", "A final review routine.", (
            ("A checklist for draft notes", "reading", 6, """
Before sending a note, check each item:

1. Every figure has a **unit** and **reference period**.
2. Averages say **which** average; skewed data use the median.
3. Changes in percentages use **percentage points** where appropriate.
4. Rates and shares use the **right denominator**.
5. Comparisons account for **group size** and mix.
6. Provisional figures are **labelled**.
7. Causal verbs are **avoided** unless the design supports them.
8. Totals match the **published** tables.
"""),
            ("Practice check: find the errors", "practice_check", 8, """
Draft sentence (invented figures):

> "Average income rose 8% to Rs 42,000, and the literacy rate increased by 6% from 70% to 76%, which shows that
> the new libraries raised literacy. District X, with 30 respondents, had the best result at 95%."

List at least four problems.

---

## Answers

1. **Which average?** Income is usually skewed; the median may be more representative.
2. **70% to 76% is 6 percentage points**, an 8.6% relative increase.
3. **Causal claim**: the libraries may be associated with the change, but the data do not show cause.
4. **Small sample**: 30 respondents make District X's 95% unreliable; add a caution.
5. **Missing reference periods** and whether figures are provisional.
"""),
        )),
    ),
    "DEMO-C2-12": (
        ("Understanding administrative sources", "Coverage and definitions come from the process.", (
            ("Coverage and definitions", "reading", 8, """
Administrative data are records created to **run a process** - registrations, applications, payments. They are
valuable for statistics, but the process decides what is recorded.

## Ask of every source

| Question | Why it matters |
|---|---|
| Who must register, and who can? | Defines coverage; voluntary registration misses people |
| What does each field mean in practice? | "Active" may mean paid this month, or ever registered |
| When is a record created, changed or closed? | Affects counts at a date versus over a period |
| Has the process changed? | New rules create breaks in series |

Record the answers in a source note before publishing any figure.
"""),
            ("Worked example: a break in series", "worked_example", 10, """
Invented monthly counts of new registrations on a portal:

| Month | New registrations |
|---|---|
| Jan | 4,100 |
| Feb | 4,300 |
| Mar | 9,800 |
| Apr | 10,100 |

## The question

Did demand more than double in March?

## Investigation

The portal changed in March: registration became **mandatory for renewals**, so existing enterprises now create
new records.

## Handling

- Do not report the jump as growth.
- Mark the **break in series** from March.
- If possible, separate *first-time* from *renewal* registrations and publish the comparable series.
"""),
        )),
        ("Combining and documenting", "Rates from records and honest limitations.", (
            ("Combining with population data", "reading", 8, """
Administrative counts often become rates using population estimates.

## Match carefully

- **Same geography**: district boundaries may differ between the source and the population series.
- **Same period**: a financial-year count with a mid-year population estimate.
- **Same group**: registrations of persons aged 18+ divided by the population aged 18+, not total population.

## Example

12,600 registrations of adults in a district with an adult population of 4,20,000:
12,600 / 4,20,000 x 1,000 = **30 per 1,000 adults**.

State the population source and year alongside the rate.
"""),
            ("Practice check: administrative data", "practice_check", 8, """
1. Registration becomes voluntary instead of mandatory. What happens to counts, and what should a release say?
2. A "beneficiaries" field counts anyone who ever received a payment. Why is it a poor measure of current reach?
3. Registrations are counted by the new district boundaries, the population by the old ones. What is the risk?

---

## Answers

1. Counts will likely **fall for process reasons**. Mark a break in series and explain the rule change.
2. It **accumulates**: people who stopped receiving payments are still counted. Use payments in the reference period.
3. **Mismatched numerators and denominators**: rates for changed districts will be wrong until both use the same
   boundaries.
"""),
        )),
    ),
}

# Advisory prerequisites: (course ref, prerequisite ref). The learning path orders them first; nothing is locked.
PREREQUISITES = (
    ("DEMO-C2-04", "DEMO-C2-01"),
    ("DEMO-C2-06", "DEMO-C2-05"),
    ("DEMO-C2-09", "DEMO-C2-08"),
    ("DEMO-C2-11", "DEMO-C2-03"),
)
