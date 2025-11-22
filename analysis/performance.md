Performance Evaluation

From our confusion matrix and our precision recall scores we can make the following conclusions about our taxonomy and the LLM implementation of it.

1. Our sample size is too small. Some of our categories (such as Admissions) only had one entry in our sample of 40 titles. This makes it really hard to draw any conclusions from the machine's handeling of this category. For the one Admission title, the machine mislabeled, and this resulted in "Admissions" scoring 0 for precision and recall. The same could be applied to the Work category which saw low scores but with only a couple examples in the dataset.

2. The "Course" category was used a lot by the LLM while it hardly used "Academic". Many of the Academic titles were labelled as Course related or Work. The LLM of course may not recognize what is and isn't a course code in the same way that a McGill student would. My human gold standard annotators where McGill students who had the contextual knowledge to differentiate Course and Academic that the Machine might not have. The Academic labels had no precsion and recall while these two metrics were high for the Course label (> 0.75).

3. Life & Resources and Leisure and Lifestyle were confusing for the machine. This is more a taxonomy design issue since even the human annotators asked for more clairty about the two categories which both mention "life". A clearer demarcation would help here. As a result, we had strong precision and recall for Leisure and Lifestyle (both around 0.71), at the cost of low metrics for Life and Resources (0.375 Precsion, and 0.5 Recall).

4. Current Events & Activism was handeled very well by the machine. With 0.75 Precsion and 1.0 Recall for our sample.