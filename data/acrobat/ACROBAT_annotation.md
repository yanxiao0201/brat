#ACROBAT
##Typing ontology v1.0 and annotation guidelines for “brat”.


###**Entities**

 - Demographics
  - Age
  - Gender
  - Ethnicity
  - Occupation

 - Lab

  - Chemicals
e.g. “carbon dioxide”

  - Genes_moleculars
e.g. “DNA”

 - Medication
e.g. “drug”

 - Procedure
  - Diagnostic
e.g. “electrocardiogram (ECG)”
  - Therapeutic
e.g. “surgery”

 - Sign_symptom
e.g. “peripheral oxygen saturation”

 - Disease_disorder
e.g. “diabetes”

 - Metadata
  - Organization
  - Author

 - Activity 
e.g. “smoker”, “admission”, “discharge”

 - Concept_ideas

  - Qualitative_concept
e.g. “high”

  - Quantitative_concept
e.g. “50%”

 - Temporal_expression
  - Date 
e.g. “Sept.3”, “now”, “the third hospital day”, “last year”, “past month” 

  - Time 
e.g. “5 p.m.”, “lunch”, “the night”, “the end of the day”, “12 hours after”

  - Duration 
e.g. “for 2 months”, “for several days”, “overnight”

  - Frequency
e.g. “170 per minute”, “2 times every second day”

 - Anatomical_structure
e.g. “blood vessel”

###**Relations**

- &lt;TEMP_COMPARABLE&gt;=Lab|Medication|Procedure|Sign_symptom|Disease_disorder|Activity|Date|Time|Duration|Frequency
- BEFORE	Arg1:<TEMP_COMPARABLE>, Arg2:<TEMP_COMPARABLE>
- AFTER	Arg1:<TEMP_COMPARABLE>, Arg2:<TEMP_COMPARABLE>
- OVERLAP	Arg1:<TEMP_COMPARABLE>, Arg2:<TEMP_COMPARABLE>, <REL-TYPE>:symmetric-transitive
- MODIFIER	Arg1:<ENTITY>, Arg2:<ENTITY>

Our purpose is to guarantee that every case report can be described as a continuous time series. Here is a list of rules to help you:

1. Annotate adjacent entities.  For example, for the following sentences, “A happens. B happens. C happens.” We only need to annotate (A before B) and (B before C), even if there is no explicit temporal relation between A and B. We assume the time progresses continuously across sentences. Do NOT annotate (A before C) since it is unnecessary;

2. A time expression should be connected with only one entity, because ideally all the events are placed in a continuous time series, there will be duplicates if a time expression is connected to two entities;

3. Only activity, sign symptom, disease disorder, procedure, medication, and lab should be considered when annotating temporal relations, because it doesn’t make sense to compare demographics, anatomical structure, etc. with each other or a time expression;

4. The direction of arrows for temporal relations should be forward, i.e. from a previous entity to a later one. Note it doesn’t apply to the relation of modifier.

###**Attributes**

- POLARITY	Arg:<ENTITY>, Value:POS|NEG

###**Instructions**

We have set up our typing ontology version 1.0, which is above and available on Github along with the annotation tool “brat” (https://github.com/yunshengb/brat). **_We hope you can annotate a very short example to help us improve. We highly appreciate your work and greatly value your opinions._** Please follow the instructions below:

0. Prerequisite: Mac OS X or Linux. “brat” has not been tested on Windows.

1. Open your terminal, `cd` to a directory where you want to install “brat”, and clone the repo `git clone https://github.com/yunshengb/brat.git`.

2. `cd brat`, then `./install`. Enter your name, password, and email, and if requested, your sudo password.

3. Type `python2.7 standalone.py` in the terminal. You should see “Serving brat at http://127.0.0.1:8001”. Open your web browser, and visit “http://127.0.0.1:8001”.

4. You should see a welcome window. Find and select the document “data/acrobat/example.txt”.

5. Login using the name and password you entered in step 1. The login button is at the top right corner.

6. Read our typing ontology online “https://github.com/yunshengb/brat/blob/master/data/acrobat/annotation.conf”.

7. We already annotated some entities, but please correct any mistakes you found, write down any confusion and comment you have, and, most importantly, annotate the rest of the document.

8. After you are done, shut down “brat”: Please switch to the terminal, and press `ctrl+\` to kill the process. Please don’t forget to do this each time you finish to release the port.

9. The annotated text will be saved automatically to `data/acrobat/example.ann`. **_Please send it to us through Slack or email, along with your comments or suggestions on how to improve the ontology and your annotating experience._**

If you encounter any technical issues, feel free to either Slack or find us in 3551 Boelter (9:00 -- 5:00 M-F).

