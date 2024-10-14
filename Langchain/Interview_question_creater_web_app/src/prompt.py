
# Define a prompt template for generating questions based on coding materials
prompt_template = '''You are an expert at creating questions based on coding materials and documentation. 
Your goal is to prepare a coder or programmer for their exam and coding interview by asking questions about the text below:

------------------------------------------------------------------------------------------------
{text}  
------------------------------------------------------------------------------------------------

Create questions that will prepare the coders or programmers for their exam, ensuring they do not lose any important information.
Questions:
'''

# Define a template for refining practice questions based on coding materials and documentation
refine_template = ("""
You are an expert at creating practice questions based on coding material and documentation.
Your goal is to help a coder or programmer prepare for a coding test.
We have received some practice questions to a certain extent: {existing_answer}.  # Placeholder for existing questions
We have the option to refine the existing questions or add new ones.  # Indicate that refinement or addition is possible
(only if necessary) with some more context below.  # Clarify that additional context may be provided if needed
------------
{text}  # Placeholder for the additional context to refine the questions
------------

Given the new context, refine the original questions in English.  # Instruction to refine questions based on the provided context
If the context is not helpful, please provide the original questions.  # Instruction to fallback on original questions if context is inadequate
QUESTIONS:
"""
)