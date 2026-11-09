# Design Notes — Week 04, Lab 2 (v2)

Standard four-move template. Nothing new is conceptually introduced in
this lab (aggregates + `GROUP BY` were both covered in week 2), so
`predict-before-run` stays fully faded — no predict cell this week.

| Addition | Where | Why |
|---|---|---|
| **Debug it** | Q11 (new) | `COUNT(product)` (= 20, every row) vs `COUNT(DISTINCT product)` (= 5, actual distinct products). No error, just a dramatically wrong number. Verified against real data. `COUNT` vs `COUNT(DISTINCT ...)` is one of the most common real-world analytics mistakes — "how many customers ordered" vs "how many orders" is the same trap. |
| **Explain it** | Q8 | Deliberately **not** about this lab's own content — it's a forward-looking bridge question: "if a region had zero salespeople, would this query show it?" This sets up the exact motivating problem for next session's `LEFT JOIN` lab. Answer key tells the instructor to hold onto this answer and connect it explicitly when introducing `LEFT JOIN`. |
| **Bonus (optional)** | Q12 | `WHERE` + `GROUP BY` + `ORDER BY` together — none of the original 10 questions combine all three. Verified: Premium Z (25,000) → Widget B (3,100). |
| **Exit ticket** | End | Same ritual. |

## Why Q8 is the most important addition this week

This lab and next session's Lab 3 are the two halves of one idea:
"`GROUP BY` on a table can never show you a group that doesn't exist in
that table — you need to start from the table that's guaranteed to have
every group (`regions` / `departments`) and `LEFT JOIN` outward." Q8
plants that question here, unanswered by the tools available in *this*
lab, so next session's `LEFT JOIN` demo lands as "oh, THAT'S how you
answer it" rather than a cold, disconnected new topic.

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
