"""DEMO pack ``demo-2``: synthetic "statistical practice" content (DEC-045, DEC-051, DEC-052). Local and ci only.

Why: pack ``demo-1`` (ten arithmetic items) only proves the pipeline. Phase C needs content that reads like
competency evidence for statistical work, so learners and reviewers can judge the product experience.

What it is (every item synthetic, labelled DEMO, never official):
- one ``draft`` functional framework ``DEMO-STAT-PRACTICE`` with four provisional levels that carry plain-language
  descriptions;
- eight competencies with descriptions of what they cover and why they matter in statistical work;
- three job roles, each requiring four competencies, each with a published baseline assessment of 20 items
  (5 per competency, so evidence reaches the "medium" band);
- forty scenario-style single-answer questions with explanations; all figures are invented;
- twelve internal courses with descriptive difficulty and learning objectives (DEC-051) and approved mappings.

Approvals are made by the seed on behalf of the synthetic competency admin: not human review (DEC-045).
The pack is additive: running it again creates only what is missing.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.modules.assessment.models import Assessment, AssessmentQuestion, Question, QuestionOption, QuestionVersion
from app.modules.competency.models import Competency, CompetencyFramework, CompetencyLevel, RoleCompetency
from app.modules.identity.models import User
from app.modules.organization.models import JobRole, Organization
from app.modules.recommendation.models import Course, CourseCompetency
from app.seed.canonical import SeedRefused
from app.seed.demo_content import content_hash
from app.seed.demo_users import demo_email

ALLOWED_ENVS = {AppEnv.local, AppEnv.ci}
FRAMEWORK_CODE = "DEMO-STAT-PRACTICE"
ITEM_NOTE = "DEMO item: synthetic scenario for local testing, not an official assessment question."

LEVELS = (
    (1, "Level 1 - Foundation", Decimal("0.00000"),
     "Recognises the basic ideas and can follow a worked example with guidance."),
    (2, "Level 2 - Working", Decimal("0.40000"),
     "Applies routine methods correctly to familiar data and spots obvious errors."),
    (3, "Level 3 - Proficient", Decimal("0.60000"),
     "Chooses appropriate methods independently, checks results and explains them to colleagues."),
    (4, "Level 4 - Advanced", Decimal("0.80000"),
     "Handles unusual cases, explains limitations clearly and reviews the work of others."),
)

# (code, name, description)
COMPETENCIES = (
    ("DEMO-SP-DESC", "Descriptive statistics",
     "Summarising data with suitable measures of centre and spread. Nearly every table, bulletin and review note "
     "starts with a summary, and the wrong measure can misrepresent what is typical."),
    ("DEMO-SP-TABLES", "Reading statistical tables",
     "Extracting and comparing figures from tables correctly, including units, footnotes, rounding and "
     "denominators. Misread tables are one of the most common sources of wrong conclusions."),
    ("DEMO-SP-RATES", "Rates, ratios and percentage change",
     "Computing and describing rates, proportions, percentage changes and percentage points. Headline "
     "indicators are almost always rates, and small wording errors change their meaning."),
    ("DEMO-SP-DIST", "Distributions and variability",
     "Understanding the shape and spread of data, skewness and outliers. Averages alone hide the variation that "
     "matters for planning and fairness."),
    ("DEMO-SP-SAMPLING", "Sampling and survey design",
     "Knowing how samples are selected, what sampling error means and where bias comes from. Survey estimates are "
     "only as good as the design behind them."),
    ("DEMO-SP-QUALITY", "Data quality and validation",
     "Checking data for errors, inconsistencies, non-response and breaks in series before analysis. Quality "
     "checks protect the credibility of every published figure."),
    ("DEMO-SP-INDEX", "Index numbers",
     "Interpreting and computing index numbers, weights and base years. Price and production indices are core "
     "outputs of official statistics."),
    ("DEMO-SP-COMM", "Communicating statistics",
     "Presenting figures, charts and caveats so that users understand them correctly. Clear communication "
     "prevents misuse and builds trust in statistics."),
)

ROLES = (
    ("DEMO-ROLE-JSO", "DEMO - Junior Statistical Officer (synthetic role)",
     "Synthetic role: compiles tables and short statistical notes from routine data. Not an official role definition.",
     (("DEMO-SP-DESC", 3), ("DEMO-SP-TABLES", 3), ("DEMO-SP-RATES", 3), ("DEMO-SP-QUALITY", 2))),
    ("DEMO-ROLE-SURVEY", "DEMO - Survey Operations Analyst (synthetic role)",
     "Synthetic role: supports sample surveys from design to validated estimates. Not an official role definition.",
     (("DEMO-SP-SAMPLING", 3), ("DEMO-SP-QUALITY", 3), ("DEMO-SP-TABLES", 2), ("DEMO-SP-DIST", 2))),
    ("DEMO-ROLE-PRICES", "DEMO - Price Statistics Analyst (synthetic role)",
     "Synthetic role: maintains price indices and explains their movements. Not an official role definition.",
     (("DEMO-SP-INDEX", 3), ("DEMO-SP-RATES", 3), ("DEMO-SP-DIST", 2), ("DEMO-SP-COMM", 2))),
)

# (competency code, difficulty, stem, [options], index of correct option, explanation). All figures are invented.
ITEMS = (
    # --- Descriptive statistics
    ("DEMO-SP-DESC", "foundational",
     "A block office recorded new business registrations over six months: 12, 15, 11, 40, 14 and 13. The 40 came "
     "from a one-off registration camp. Which figure best describes a typical month?",
     ["The mean, 17.5", "The median, 13.5", "The maximum, 40", "The range, 29"], 1,
     "Sorted: 11, 12, 13, 14, 15, 40. The median is (13 + 14) / 2 = 13.5. The mean (17.5) is pulled up by the "
     "one-off value, so the median better describes a typical month."),
    ("DEMO-SP-DESC", "foundational",
     "An analyst adds one very large value to a set of 50 household incomes. Which summary measure is likely to "
     "change the most?",
     ["The median", "The mode", "The mean", "The interquartile range"], 2,
     "The mean uses every value, so one extreme value can move it a lot. The median, mode and interquartile range "
     "are resistant to a single outlier."),
    ("DEMO-SP-DESC", "intermediate",
     "Block A reports an average monthly household expenditure of Rs 18,000 from 50 households. Block B reports "
     "Rs 24,000 from 150 households. What is the average for all 200 households?",
     ["Rs 21,000", "Rs 22,500", "Rs 24,000", "Rs 42,000"], 1,
     "Use a weighted mean: (50 x 18,000 + 150 x 24,000) / 200 = 4,500,000 / 200 = Rs 22,500. Averaging the two "
     "block means (Rs 21,000) ignores that Block B has three times as many households."),
    ("DEMO-SP-DESC", "intermediate",
     "A draft note says: 'The average daily wage rose from Rs 400 to Rs 420, so every worker earned more.' What is "
     "wrong with this conclusion?",
     ["Nothing; a higher average means everyone gained",
      "An average can rise even if some workers earned less",
      "Averages cannot be compared across periods",
      "The increase is too small to be meaningful"], 1,
     "An average summarises the whole group. It can rise because some wages rose a lot while others fell, so it "
     "says nothing about every individual."),
    ("DEMO-SP-DESC", "advanced",
     "Monthly incomes in a survey sample are strongly right-skewed. A table shows both the mean and the median. "
     "Which statement is most accurate?",
     ["The mean and median will be about equal",
      "The median will usually be above the mean",
      "The mean will usually be above the median, and the median better represents a typical income",
      "The mean is always the better measure because it uses all values"], 2,
     "In a right-skewed distribution a few high incomes pull the mean upwards, so the mean exceeds the median. The "
     "median is closer to what a typical household earns."),

    # --- Reading statistical tables
    ("DEMO-SP-TABLES", "foundational",
     "A synthetic table shows literacy rates. District P: male 84.1%, female 72.0%. District Q: male 85.0%, female "
     "77.9%. Which district has the smaller gap between male and female literacy?",
     ["District P, with a gap of 12.1 points", "District Q, with a gap of 7.1 points",
      "Both have the same gap", "It cannot be told without population figures"], 1,
     "Gap = male rate - female rate. P: 84.1 - 72.0 = 12.1 points. Q: 85.0 - 77.9 = 7.1 points. District Q's gap "
     "is smaller."),
    ("DEMO-SP-TABLES", "foundational",
     "A table heading says 'Persons employed (in thousands)'. One cell shows 2,450. How many persons does this "
     "represent?",
     ["2,450", "24,500", "245,000", "2,450,000"], 3,
     "The unit is thousands, so 2,450 thousand = 2,450 x 1,000 = 2,450,000 persons. Always read the unit line and "
     "footnotes before quoting a figure."),
    ("DEMO-SP-TABLES", "intermediate",
     "A table shows an unemployment rate of 6.0% in 2023 and 5.4% in 2024. A draft note says 'unemployment fell by "
     "0.6%'. What is the correct description?",
     ["It fell by 0.6 percentage points, a relative fall of 10%",
      "It fell by 0.6%, which is the same as 0.6 percentage points",
      "It fell by 6%", "It fell by 11%"], 0,
     "The difference between two rates is measured in percentage points: 6.0 - 5.4 = 0.6 points. The relative "
     "change is 0.6 / 6.0 = 10%. Saying '0.6%' confuses the two."),
    ("DEMO-SP-TABLES", "intermediate",
     "In a published table the column total is 1 more than the sum of the rows. The footnote says 'Totals may not "
     "add up due to rounding.' What should the analyst do?",
     ["Correct the total so it matches the rows",
      "Treat the difference as rounding and use the published figures as they are",
      "Report the table as containing an error",
      "Drop the total row from the analysis"], 1,
     "Each figure is rounded independently, so small differences between totals and the sum of rounded parts are "
     "expected. The footnote documents this; the published figures should not be altered."),
    ("DEMO-SP-TABLES", "advanced",
     "One table lists hospital beds by state and another lists state populations. You need to compare access to "
     "beds across states fairly. Which indicator should you compute?",
     ["Total beds per state", "Beds per 1,000 population", "Share of all beds held by each state",
      "Population per state"], 1,
     "States differ in size, so totals mislead. A rate such as beds per 1,000 population puts states on a "
     "comparable basis."),

    # --- Rates, ratios and percentage change
    ("DEMO-SP-RATES", "foundational",
     "A monthly bulletin reports that registered vehicles in a district rose from 250 thousand to 300 thousand in a "
     "year. What is the percentage increase?",
     ["16.7%", "20%", "50%", "83.3%"], 1,
     "Percentage change = (new - old) / old x 100 = (300 - 250) / 250 x 100 = 20%. Dividing by the new value "
     "(16.7%) is a common mistake."),
    ("DEMO-SP-RATES", "foundational",
     "In a sample survey, 180 of the 600 households interviewed own a two-wheeler. What share of households is "
     "this?",
     ["18%", "30%", "33%", "60%"], 1,
     "Share = 180 / 600 = 0.30, which is 30% of interviewed households."),
    ("DEMO-SP-RATES", "intermediate",
     "Average rents rose 10% in the first year and a further 10% in the second year. What is the total increase "
     "over the two years?",
     ["20%", "21%", "11%", "100%"], 1,
     "Changes compound: 1.10 x 1.10 = 1.21, a 21% increase. Adding the two rates (20%) ignores that the second "
     "rise applies to an already higher level."),
    ("DEMO-SP-RATES", "intermediate",
     "District A recorded 1,200 births with a population of 80,000. District B recorded 1,800 births with a "
     "population of 150,000. Which has the higher crude birth rate per 1,000 population?",
     ["District A, 15 per 1,000", "District B, 12 per 1,000", "Both are equal",
      "District B, because it has more births"], 0,
     "A: 1,200 / 80,000 x 1,000 = 15. B: 1,800 / 150,000 x 1,000 = 12. District A's rate is higher even though "
     "B has more births in total."),
    ("DEMO-SP-RATES", "advanced",
     "Coverage of a scheme rose from 40% of eligible households to 50%. One note says coverage 'increased by 25%', "
     "another says it 'increased by 10%'. Which is right?",
     ["Only 25% is right", "Only 10% is right",
      "Both can be right: a 10 percentage point rise is a 25% relative increase, so the note must say which it means",
      "Neither is right; the increase is 5%"], 2,
     "50 - 40 = 10 percentage points; 10 / 40 = 25% relative increase. Both numbers are correct descriptions of "
     "different things, which is why the unit must be stated."),

    # --- Distributions and variability
    ("DEMO-SP-DIST", "foundational",
     "Two districts have the same average monthly rainfall, but District X's monthly figures vary much more. Which "
     "measure would show this difference?",
     ["The mean", "The median", "The standard deviation", "The total annual rainfall"], 2,
     "The mean and median describe the centre, which is the same. The standard deviation measures spread, which "
     "is where the districts differ."),
    ("DEMO-SP-DIST", "foundational",
     "Which chart best shows the shape of the distribution of household incomes from a survey?",
     ["A pie chart", "A histogram", "A line chart over time", "A single bar for the mean"], 1,
     "A histogram groups values into intervals and shows how many fall in each, revealing skewness, peaks and "
     "outliers."),
    ("DEMO-SP-DIST", "intermediate",
     "Scores in a training batch are roughly normally distributed with a mean of 60 and a standard deviation of "
     "10. About what share of trainees scored between 50 and 70?",
     ["About 50%", "About 68%", "About 95%", "About 99.7%"], 1,
     "50 to 70 is within one standard deviation of the mean. For a normal distribution about 68% of values lie "
     "within one standard deviation."),
    ("DEMO-SP-DIST", "intermediate",
     "The interquartile range of daily arrivals at a wholesale market runs from 40 to 70. What does this tell you?",
     ["Every day had between 40 and 70 arrivals",
      "The middle half of days had between 40 and 70 arrivals",
      "The average was 55 arrivals",
      "No day had more than 70 arrivals"], 1,
     "The interquartile range spans the 25th to the 75th percentile, so it contains the middle 50% of days. "
     "Other days fall outside it."),
    ("DEMO-SP-DIST", "advanced",
     "Farm sizes in a district have a long right tail because of a few very large farms. You need a measure of "
     "spread that is not distorted by those farms. Which is most suitable?",
     ["The range", "The standard deviation", "The interquartile range", "The mean absolute value"], 2,
     "The range and the standard deviation are strongly affected by extreme values. The interquartile range uses "
     "only the middle half of the data."),

    # --- Sampling and survey design
    ("DEMO-SP-SAMPLING", "foundational",
     "From a complete list of village households, a survey selects every 10th household after a random start. "
     "What type of sampling is this?",
     ["Simple random sampling", "Systematic sampling", "Quota sampling", "Convenience sampling"], 1,
     "Selecting at a fixed interval after a random start is systematic sampling."),
    ("DEMO-SP-SAMPLING", "foundational",
     "What is the main reason for selecting survey units at random?",
     ["To reduce the cost of fieldwork",
      "To give every unit a known chance of selection, so results can be generalised with measurable error",
      "To make sure the sample contains only typical households",
      "To avoid having to calculate weights"], 1,
     "Random selection with known probabilities is what allows estimates and their sampling error to be computed "
     "for the whole population."),
    ("DEMO-SP-SAMPLING", "intermediate",
     "A state is divided into rural and urban areas, and a separate sample is drawn from each so that both are "
     "adequately represented. What design is this?",
     ["Cluster sampling", "Stratified sampling", "Snowball sampling", "Multi-round sampling"], 1,
     "Dividing the population into groups (strata) and sampling within each is stratified sampling. It ensures "
     "each group is represented and usually improves precision."),
    ("DEMO-SP-SAMPLING", "intermediate",
     "Under simple random sampling, the sample size for a proportion is increased from 400 to 1,600 households. "
     "Roughly what happens to the standard error?",
     ["It is halved", "It falls to a quarter", "It stays the same", "It doubles"], 0,
     "The standard error is proportional to 1 / square root of n. Quadrupling n divides the standard error by the "
     "square root of 4, which is 2."),
    ("DEMO-SP-SAMPLING", "advanced",
     "A telephone survey on internet use reaches only households with a phone. Its internet-use estimate is much "
     "higher than an earlier household visit survey. What is the most likely explanation?",
     ["Sampling error from a small sample", "Coverage bias: households without phones were excluded",
      "Rounding in the published tables", "A seasonal effect"], 1,
     "Households without phones are more likely to lack internet access. Leaving them out of the frame biases "
     "the estimate upwards, regardless of sample size."),

    # --- Data quality and validation
    ("DEMO-SP-QUALITY", "foundational",
     "During data entry, a household record shows the head of household's age as 7 years. What is the best first "
     "step?",
     ["Delete the record", "Change the age to 70",
      "Flag the record and check it against the questionnaire before analysis", "Leave it; one error will not matter"], 2,
     "Implausible values should be flagged and verified at source. Guessing a correction or deleting records can "
     "introduce new errors."),
    ("DEMO-SP-QUALITY", "foundational",
     "Which of these is a consistency check?",
     ["Checking that the number of children in a household is not greater than household size",
      "Checking that the file opens", "Counting the number of records", "Sorting records by district"], 0,
     "A consistency check compares related fields for logical agreement, such as children not exceeding the "
     "total number of household members."),
    ("DEMO-SP-QUALITY", "intermediate",
     "Of 30 districts submitting monthly reports, 3 report exactly the same figures as last month for every item. "
     "What does this most likely indicate?",
     ["Stable conditions in those districts", "Possible carry-forward of old data; the reports should be verified",
      "A rounding convention", "Better data quality than other districts"], 1,
     "Identical figures on every item month after month are a classic sign of copied or carried-forward data and "
     "should be queried with the reporting unit."),
    ("DEMO-SP-QUALITY", "intermediate",
     "A survey's response rate fell from 92% to 71%. Why does this matter for the estimates?",
     ["It does not matter if the sample is still large",
      "Estimates may be biased if people who did not respond differ from those who did",
      "It only affects the cost of the survey",
      "It makes the estimates more precise"], 1,
     "Non-response bias depends on how non-respondents differ, not just on how many there are. A large fall in "
     "response needs investigation and possibly adjustment."),
    ("DEMO-SP-QUALITY", "advanced",
     "Registered enterprises in an administrative dataset jump 35% in one quarter, the same quarter a new online "
     "registration portal opened. How should this be treated in a time series?",
     ["As real growth in enterprises",
      "As a possible break in series: document it and do not interpret the jump as growth without checks",
      "Remove the quarter from the series", "Average it with the previous quarter"], 1,
     "A change in the collection process can create an artificial jump. It should be documented as a potential "
     "series break and investigated before drawing conclusions."),

    # --- Index numbers
    ("DEMO-SP-INDEX", "foundational",
     "A synthetic price index with base year 2020 = 100 stands at 125 in 2025. What does this mean?",
     ["Prices of the basket are on average 25% higher than in 2020", "Prices rose 125% since 2020",
      "Prices rose by 25 rupees", "Every item costs 25% more"], 0,
     "An index of 125 against a base of 100 means the basket costs 25% more on average than in the base year. "
     "Individual items can rise or fall by different amounts."),
    ("DEMO-SP-INDEX", "foundational",
     "Why are weights used in a consumer price index?",
     ["To make the index easier to calculate",
      "So that items taking a larger share of spending influence the index more",
      "To keep the index at 100", "To remove seasonal effects"], 1,
     "Weights reflect expenditure shares, so a price rise in a major item (such as food) affects the index more "
     "than the same rise in a minor item."),
    ("DEMO-SP-INDEX", "intermediate",
     "An index rose from 120 to 132. What is the percentage change?",
     ["12%", "10%", "9.1%", "32%"], 1,
     "(132 - 120) / 120 x 100 = 10%. The 12-point difference is not a 12% change because the base is 120, not "
     "100."),
    ("DEMO-SP-INDEX", "intermediate",
     "A two-group basket has food (weight 60) with an index of 150 and non-food (weight 40) with an index of 110. "
     "What is the combined index?",
     ["130", "134", "140", "260"], 1,
     "Weighted average: (60 x 150 + 40 x 110) / 100 = (9,000 + 4,400) / 100 = 134. A simple average (130) ignores "
     "that food has the larger weight."),
    ("DEMO-SP-INDEX", "advanced",
     "A series is rebased from 2012 = 100 to 2020 = 100. On the old base, 2020 was 150 and 2024 was 180. What is "
     "2024 on the new base?",
     ["120", "130", "180", "270"], 0,
     "Divide by the new base year's old value: 180 / 150 x 100 = 120. Rebasing changes the reference point, not "
     "the relative movement between years."),

    # --- Communicating statistics
    ("DEMO-SP-COMM", "foundational",
     "Which chart title is most useful in a statistical bulletin?",
     ["Chart 3", "Water",
      "Share of households with piped drinking water, by district, 2024 (%)", "Important data"], 2,
     "A good title states what is measured, for whom, where, when and in what unit, so the chart can be understood "
     "on its own."),
    ("DEMO-SP-COMM", "foundational",
     "A district-level figure is based on a very small number of sample households. What is the responsible way to "
     "handle it?",
     ["Publish it without comment", "Round it to look more stable",
      "Publish it with a reliability caution, or suppress it if the release rules require", "Replace it with the state average"], 2,
     "Estimates from very small samples are unreliable. Users must be warned, or the figure withheld under the "
     "agreed release rules."),
    ("DEMO-SP-COMM", "intermediate",
     "A bar chart compares values of 92 and 95, but its vertical axis starts at 90. What is the risk?",
     ["The chart will be hard to print", "It exaggerates the difference between the two values",
      "It hides the difference", "There is no risk"], 1,
     "Starting the axis at 90 makes a 3-point difference look like a bar two and a half times taller. Bar charts "
     "should normally start at zero."),
    ("DEMO-SP-COMM", "intermediate",
     "A news report compares the total number of road accidents in two districts with very different populations. "
     "What should a statistical clarification point out?",
     ["Totals are the best comparison", "Rates per population (or per vehicle) are needed for a fair comparison",
      "Accidents cannot be compared across districts", "The larger district must be safer"], 1,
     "Larger populations produce more events. A rate such as accidents per 100,000 population makes the "
     "comparison meaningful."),
    ("DEMO-SP-COMM", "advanced",
     "Across districts, the correlation between the number of mobile towers and the literacy rate is 0.8 "
     "(synthetic). How should this be described?",
     ["Mobile towers increase literacy",
      "There is a strong association, but it does not show cause; factors such as urbanisation may drive both",
      "The relationship is weak", "Literacy causes towers to be built"], 1,
     "A correlation of 0.8 is a strong association. Correlation alone cannot establish causation, and a common "
     "factor may explain both."),
)

# (external_ref, title, difficulty, days, description, objectives, [(competency code, relevance)])
COURSES = (
    ("DEMO-C2-01", "DEMO - Summarising data with confidence (synthetic course)", "foundational", 2,
     "Choose between mean, median and mode, describe spread, and write summaries that represent a typical case.",
     ["Choose a suitable measure of centre for skewed and symmetric data",
      "Compute weighted means from grouped figures",
      "Describe spread using range, interquartile range and standard deviation",
      "Write a one-paragraph summary that avoids misleading averages"],
     [("DEMO-SP-DESC", "primary"), ("DEMO-SP-DIST", "secondary")]),
    ("DEMO-C2-02", "DEMO - Reading statistical tables critically (synthetic course)", "foundational", 1,
     "Read units, footnotes and denominators before quoting a figure, and compare rows and columns correctly.",
     ["Identify units, reference periods and footnotes in a table",
      "Compare figures using suitable denominators",
      "Recognise rounding effects in totals",
      "Quote a table figure accurately in a note"],
     [("DEMO-SP-TABLES", "primary"), ("DEMO-SP-COMM", "secondary")]),
    ("DEMO-C2-03", "DEMO - Rates, ratios and percentage change in practice (synthetic course)", "foundational", 2,
     "Compute and describe rates, percentage change and percentage points without the common wording mistakes.",
     ["Distinguish percentage change from percentage points",
      "Compute compound changes over several periods",
      "Convert counts into rates per 1,000 or 100,000",
      "Describe changes in indicators precisely"],
     [("DEMO-SP-RATES", "primary"), ("DEMO-SP-TABLES", "secondary")]),
    ("DEMO-C2-04", "DEMO - Understanding variability and distributions (synthetic course)", "intermediate", 3,
     "See beyond the average: shapes of distributions, outliers, percentiles and the normal distribution.",
     ["Recognise skewness and outliers in histograms",
      "Interpret percentiles and the interquartile range",
      "Apply the 68-95-99.7 rule to roughly normal data",
      "Choose robust measures for skewed data"],
     [("DEMO-SP-DIST", "primary"), ("DEMO-SP-DESC", "secondary")]),
    ("DEMO-C2-05", "DEMO - Survey sampling essentials (synthetic course)", "intermediate", 3,
     "How probability samples work, what sampling error is and where bias comes from.",
     ["Describe simple random, systematic, stratified and cluster sampling",
      "Explain sampling error and how sample size affects it",
      "Identify coverage and selection bias",
      "Read a survey's design notes critically"],
     [("DEMO-SP-SAMPLING", "primary")]),
    ("DEMO-C2-06", "DEMO - Planning and running a sample survey (synthetic course)", "advanced", 5,
     "From frame to estimates: design choices, fieldwork monitoring, non-response and weighting.",
     ["Choose a design and allocate a sample across strata",
      "Monitor fieldwork quality and response rates",
      "Understand the purpose of design and non-response weights",
      "Document limitations of survey estimates"],
     [("DEMO-SP-SAMPLING", "primary"), ("DEMO-SP-QUALITY", "secondary")]),
    ("DEMO-C2-07", "DEMO - Data validation and quality checks (synthetic course)", "intermediate", 2,
     "Build range, consistency and trend checks, and decide what to do when a check fails.",
     ["Design range and consistency checks",
      "Spot carried-forward and duplicated reports",
      "Assess the effect of non-response",
      "Record and communicate data quality issues"],
     [("DEMO-SP-QUALITY", "primary"), ("DEMO-SP-SAMPLING", "secondary")]),
    ("DEMO-C2-08", "DEMO - Index numbers from first principles (synthetic course)", "intermediate", 3,
     "What an index measures, how weights work, and how to compute and interpret index changes.",
     ["Interpret an index relative to its base year",
      "Compute a weighted index from group indices",
      "Compute percentage change between index values",
      "Explain why weights matter"],
     [("DEMO-SP-INDEX", "primary"), ("DEMO-SP-RATES", "secondary")]),
    ("DEMO-C2-09", "DEMO - Price statistics: weights, rebasing and linking (synthetic course)", "advanced", 4,
     "Maintain a price index over time: updating weights, rebasing and linking old and new series.",
     ["Rebase an index to a new reference year",
      "Link two series with an overlap period",
      "Explain the effect of weight updates",
      "Describe index movements for non-specialist users"],
     [("DEMO-SP-INDEX", "primary")]),
    ("DEMO-C2-10", "DEMO - Communicating statistics clearly (synthetic course)", "foundational", 2,
     "Titles, charts, caveats and plain-language notes that help users read figures correctly.",
     ["Write informative chart and table titles",
      "Choose chart types and axes that do not mislead",
      "Add reliability cautions where needed",
      "Explain association versus causation"],
     [("DEMO-SP-COMM", "primary"), ("DEMO-SP-TABLES", "secondary")]),
    ("DEMO-C2-11", "DEMO - Avoiding common statistical pitfalls (synthetic course)", "intermediate", 1,
     "A short clinic on the errors that most often reach draft notes: averages, percentages and comparisons.",
     ["Recognise misleading averages",
      "Avoid percentage-point confusion",
      "Compare groups of different sizes fairly",
      "Check a draft note for common errors"],
     [("DEMO-SP-DESC", "secondary"), ("DEMO-SP-RATES", "secondary"), ("DEMO-SP-COMM", "secondary")]),
    ("DEMO-C2-12", "DEMO - Working with administrative data (synthetic course)", "intermediate", 2,
     "Use registration and scheme data responsibly: coverage, definitions, process changes and series breaks.",
     ["Assess coverage and definitions of administrative sources",
      "Detect breaks in series caused by process changes",
      "Combine administrative figures with population data",
      "Document limitations for users"],
     [("DEMO-SP-QUALITY", "secondary"), ("DEMO-SP-TABLES", "secondary")]),
)


def seed_demo_pack_2(session: Session, org: Organization, app_env: AppEnv) -> Counter:
    """Additive: creates whatever part of pack demo-2 is missing for this organisation."""
    if app_env not in ALLOWED_ENVS:
        raise SeedRefused(f"DEMO content is not allowed in {app_env.value}")
    admin = session.scalar(select(User).where(User.organization_id == org.id, User.email == demo_email("competency_admin")))
    if admin is None:
        raise SeedRefused("DEMO content needs the synthetic demo users; run with --demo-users")
    created: Counter = Counter()
    now = datetime.now(timezone.utc)

    framework = session.scalar(select(CompetencyFramework).where(
        CompetencyFramework.organization_id == org.id, CompetencyFramework.code == FRAMEWORK_CODE))
    if framework is None:
        framework = CompetencyFramework(
            organization_id=org.id, name="DEMO - Statistical practice framework (synthetic, not official)",
            code=FRAMEWORK_CODE, framework_type="functional", publisher="DEMO (synthetic, local development only)",
            version_label="demo-2", status="draft", definitions_restricted=False, created_by=admin.id)
        session.add(framework)
        session.flush()
        for number, label, min_score, description in LEVELS:
            session.add(CompetencyLevel(organization_id=org.id, framework_id=framework.id, level_number=number,
                                        label=label, description=description, min_score=min_score,
                                        threshold_status="provisional", created_by=admin.id))
        created.update(competency_frameworks=1, competency_levels=len(LEVELS))
        session.flush()

    competencies: dict[str, Competency] = {
        c.code: c for c in session.scalars(select(Competency).where(Competency.framework_id == framework.id))}
    for code, name, description in COMPETENCIES:
        if code not in competencies:
            competencies[code] = Competency(organization_id=org.id, framework_id=framework.id, code=code,
                                            name=f"DEMO - {name} (synthetic)", data_status="ASSUMED",
                                            description=f"{description} (Synthetic demo competency, not an official definition.)",
                                            created_by=admin.id)
            session.add(competencies[code])
            created["competencies"] += 1
    session.flush()

    versions_by_competency: dict[str, list[QuestionVersion]] = {code: [] for code, _, _ in COMPETENCIES}
    for code, difficulty, stem, options, correct, explanation in ITEMS:
        digest = content_hash(stem, options)
        version = session.scalar(select(QuestionVersion).where(QuestionVersion.organization_id == org.id,
                                                               QuestionVersion.content_hash == digest))
        if version is None:
            question = Question(organization_id=org.id, origin="demo_seed", status="pending_validation", created_by=admin.id)
            session.add(question)
            session.flush()
            version = QuestionVersion(organization_id=org.id, question_id=question.id, version_number=1, stem=stem,
                                      explanation=f"{explanation} ({ITEM_NOTE})", difficulty=difficulty,
                                      difficulty_confirmed=False, competency_id=competencies[code].id,
                                      content_hash=digest, created_by=admin.id)
            session.add(version)
            session.flush()
            for position, (label, text) in enumerate(zip("ABCD", options, strict=True), start=1):
                session.add(QuestionOption(organization_id=org.id, question_version_id=version.id, label=label,
                                           text=text, is_correct=position - 1 == correct, position=position))
            question.current_version_id = version.id
            question.approved_version_id = version.id
            question.status = "approved"
            created["questions"] += 1
        versions_by_competency[code].append(version)
    session.flush()

    for role_code, role_name, role_description, requirements in ROLES:
        role = session.scalar(select(JobRole).where(JobRole.organization_id == org.id, JobRole.code == role_code))
        if role is None:
            role = JobRole(organization_id=org.id, name=role_name, code=role_code, description=role_description,
                           created_by=admin.id)
            session.add(role)
            session.flush()
            created["job_roles"] += 1
        existing = {m.competency_id for m in session.scalars(select(RoleCompetency).where(
            RoleCompetency.job_role_id == role.id, RoleCompetency.status == "approved"))}
        for competency_code, required in requirements:
            if competencies[competency_code].id not in existing:
                session.add(RoleCompetency(organization_id=org.id, job_role_id=role.id,
                                           competency_id=competencies[competency_code].id,
                                           required_level_number=required, status="approved", approved_by=admin.id,
                                           approved_at=now, created_by=admin.id))
                created["role_competencies"] += 1
        session.flush()

        assessment = session.scalar(select(Assessment).where(Assessment.job_role_id == role.id, Assessment.purpose == "pre",
                                                             Assessment.status == "published"))
        if assessment is None:
            assessment = Assessment(
                organization_id=org.id,
                title=f"DEMO - Baseline assessment: {role_name.removeprefix('DEMO - ').removesuffix(' (synthetic role)')} (synthetic)",
                purpose="pre", job_role_id=role.id, feedback_policy="correctness_and_explanations", status="published",
                published_at=now, published_by=admin.id, created_by=admin.id,
                blueprint={"demo_seed": True, "pack": "demo-2", "competencies": [c for c, _ in requirements],
                           "min_items_per_competency": 5})
            session.add(assessment)
            session.flush()
            for competency_code, _ in requirements:
                for version in versions_by_competency[competency_code]:
                    session.add(AssessmentQuestion(organization_id=org.id, assessment_id=assessment.id,
                                                   question_version_id=version.id, created_by=admin.id))
            created["assessments"] += 1
    session.flush()

    for ref, title, difficulty, days, description, objectives, mappings in COURSES:
        course = session.scalar(select(Course).where(Course.organization_id == org.id, Course.external_ref == ref))
        if course is None:
            course = Course(organization_id=org.id, course_type="internal", title=title,
                            provider_organisation="DEMO provider (synthetic)",
                            description=f"{description} Synthetic course for local testing; not a real training programme.",
                            duration_days=days, difficulty=difficulty, learning_objectives=objectives, external_ref=ref,
                            data_status="ASSUMED", review_status="approved", status="active", created_by=admin.id)
            session.add(course)
            session.flush()
            for competency_code, relevance in mappings:
                session.add(CourseCompetency(organization_id=org.id, course_id=course.id,
                                             competency_id=competencies[competency_code].id, relevance=relevance,
                                             method="demo_seed", status="approved", approved_by=admin.id,
                                             approved_at=now, created_by=admin.id))
                created["course_competencies"] += 1
            created["courses"] += 1
    session.flush()
    return created
