from app.models.file import extracted_info_collection
from fastapi import HTTPException
from app.prompts.prompts import question_prompt_template ,advice_template
from app.config.llm import llm
from app.utility.formatoutput import format_generated_questions
from app.models.file import generated_question_collection
from typing import List
from typing import Dict

async def generate_interview_questions():
    # Retrieve extracted information from MongoDB
    document = await extracted_info_collection.find_one()
    if not document or not document.get("content"):
        raise HTTPException(status_code=404, detail="No extracted information found.")
    
    extracted_info = document.get("content")
    
    # Format the prompt with extracted information
    question_prompt = question_prompt_template.format(**extracted_info)
    
    try:
        # Generate interview questions using LLM
        question_output =  llm.invoke(question_prompt)  # Ensure this is awaited if it's an async call
        print("Raw question output:", question_output)
        return {"questions": question_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {str(e)}")


    

async def get_answers_to_questions(questions: List[str]) -> List[str]:
    answers = []
    for question in questions:
        answer_prompt = f"Please provide a detailed answer to the following question:\n{question}"
        try:
            answer_output =  llm.invoke(answer_prompt)  # Ensure this is awaited if it's an async call
            answers.append(answer_output)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting answer for question '{question}': {str(e)}")
    return answers

async def generate_answers(questions: List[str]):
    try:
        answers = await get_answers_to_questions(questions)
        return {
            "questions": questions,
            "answers": answers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answers: {str(e)}")

async def generate_advices():
    # Retrieve extracted information from MongoDB
    document = await extracted_info_collection.find_one()
    if not document or not document.get("content"):
        raise HTTPException(status_code=404, detail="No extracted information found.")
    
    extracted_info = document.get("content")
    
    # Format resume details for prompt
    resume_details = "\n".join([f"{key}: {value}" for key, value in extracted_info.items()])
    
    # Create the prompt for the LLM
    
    
    advice_prompt = advice_template.format(
        resume_details=resume_details
    )
    
    try:
        # Invoke LLM to perform the comparison
        comparison_output = llm.invoke(advice_prompt )
        return {"advice_results": comparison_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advices : {str(e)}")

