from app.models.file import extracted_info_collection
from fastapi import HTTPException
from app.prompts.prompts import question_prompt_template ,advice_template
from app.config.llm import llm
from typing import List
from typing import Dict
from langchain.agents import load_tools, initialize_agent, AgentType

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


def is_satisfactory_answer(answer: str) -> bool:
    return "I do not have access" not in answer and len(answer) > 50  # Example condition

def is_relevant_response(question: str, response: str) -> bool:
    verification_prompt = f"Check if the following response answers the question effectively. If it does, respond with 'Yes', otherwise respond with 'No'.\nQuestion: {question}\nResponse: {response}"
    verification_answer = llm.invoke(verification_prompt)
    return verification_answer.strip().lower() == "yes"

async def get_answers_to_questions(questions: List[str]) -> List[str]:
    tool = load_tools(["serpapi"], serpapi_api_key="dfb620d599c6a56f50d33bac58238613c68658266d617a2506226273b1f1385e", llm=llm)
    agent = initialize_agent(tool, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    answers = []
    for question in questions:
        answer_prompt = f"Please provide a detailed answer to the following question:\n{question}"
        llm_answer = llm.invoke(answer_prompt)
        
        if is_relevant_response(question, llm_answer):
            answers.append(llm_answer)
        else:
            agent_answer = agent.run(answer_prompt)
            answers.append(agent_answer)
    
    return answers

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

