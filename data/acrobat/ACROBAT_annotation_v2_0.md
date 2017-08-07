#ACROBAT
##Typing ontology v2.0 and annotation guidelines for “brat”.


###**Entities**

- Metadata
  - Demographics
      - Age
      - Gender
      - Occupation
  - Document_metadata
      - Organization
      - Author
- Concept_ideas
  - Qualitative_concept
		# e.g. “high”
  - Quantitative_concept
		# e.g. “50%”
- Anatomical_structure
	# e.g. “blood vessel”

###**Events**
- Lab
  - Chemicals
		# e.g. “carbon dioxide”
  - Genes_moleculars
		# e.g. “DNA”
- Medication
	# e.g. “drug”
- Diagnostic_procedure
	# e.g. “electrocardiogram (ECG)”
- Therapeutic_procedure
	# e.g. “surgery”
- Sign_symptom
	# e.g. “peripheral oxygen saturation”
- Disease_disorder
	# e.g. “diabetes”
- Temporal_expression
  - Date 
		# e.g. “Sept.3”, “now”, “the third hospital day”, “last year”, “past month” 
  - Time 
		# e.g. “5 p.m.”, “lunch”, “the night”, “the end of the day”, “12 hours after”
  - Duration 
		# e.g. “for 2 months”, “for several days”, “overnight”
  - Frequency
		# e.g. “170 per minute”, “2 times every second day”
- Activity 
	# e.g. “smoker”, “admission”, “discharge”, "falling from a bicycle"


###**Relations**

- BEFORE	Arg1:&lt;EVENT&gt;, Arg2:&lt;EVENT&gt;

- AFTER	Arg1:&lt;EVENT&gt;, Arg2:&lt;EVENT&gt;

- OVERLAP	Arg1:&lt;EVENT&gt;, Arg2:&lt;EVENT&gt;, &lt;REL-TYPE&gt;:symmetric-transitive

- MODIFIER	Arg1:Qualitative_concept|Quantitative_concept|Anatomical_structure, Arg2:&lt;ENTITY&gt;|&lt;EVENT&gt;

- DECREASE_TO	Arg1:&lt;EVENT&gt;, Arg2:Qualitative_concept|Quantitative_concept

- DECREASE_FROM	Arg1:&lt;EVENT&gt;, Arg2:Qualitative_concept|Quantitative_concept

- INCREASE_TO	Arg1:&lt;EVENT&gt;, Arg2:Qualitative_concept|Quantitative_concept

- INCREASE_FROM	Arg1:&lt;EVENT&gt;, Arg2:Qualitative_concept|Quantitative_concept

###**Instructions**

Our purpose is to guarantee that every case report can be described as a continuous time series. Here is a list of rules to help you:

0. Event vs Entity: all events are temporal comparable and entities are not. 

1. Annotate adjacent entities.  For example, for the following sentences, “A happens. B happens. C happens.” We only need to annotate (A before B) and (B before C), even if there is no explicit temporal relation between A and B. We assume the time progresses continuously across sentences. Do NOT annotate (A before C) since it is unnecessary;

2. A time expression should be connected with only one entity, because ideally all the events are placed in a continuous time series, there will be duplicates if a time expression is connected to two entities;

3. Only activity, sign symptom, disease disorder, procedure, medication, and lab should be considered when annotating temporal relations, because it doesn’t make sense to compare demographics, anatomical structure, etc. with each other or a time expression;

4. The direction of arrows for temporal relations should be forward, i.e. from a previous entity to a later one. Note it doesn’t apply to the relation of modifier;

5. Modifiers are only used for compensating the lacking of relations among entities. For example, "the apnea-hypopnea index (AHI) of 71 per hour.", the "71 per hour" is a frequency test result, so we build a modifier between it and "(AHI)". In this example, the full name and abbreviation have overlaping relation since they are both events, and we need a temporal relation to connect them, for which "overlap" is the best here. Then we do not need any modifiers to denote the relation;

6. Modifiers are only used between (concept ideas/anatomical structure) and (other events/entites).


###**Attributes**

- POLARITY	Arg:&lt;EVENT&gt;, Value:POS|MAYBE_POS|MAYBE_NEG|NEG

- TREND		Arg:&lt;EVENT&gt;, Value:DEC|INC


