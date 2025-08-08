from fastapi import APIRouter, Header
from Models.score_schema import input, output
from Controllers.score_controller import add_scores, get_student_scores, get_section_scores, get_scores_by_month

router = APIRouter(prefix="/scores", tags=["Scores"])

@router.post("/add_scores",response_model=output.AddScores) #AdminScoresRole
async def Route_Add_Score(data: input.AddScores):
    return await add_scores(data)
    
@router.get("/get_section_scores",response_model=output.GetSectionScores)
async def Route_Get_Section_Scores(data: input.GetSectionScores):
    return await get_section_scores( data)
    
@router.get("/get_student_scores",response_model=output.GetStudentScores) #StudentScoreRole
async def Route_Get_Student_Scores(email: str = Header(...), section: str = Header(...), month: str = Header(...)):
    return await get_student_scores(email, section, month)
    
@router.get("/get_scores_by_month",response_model=output.GetScoresByMonth) #LeadScoresRole
async def Route_Get_Scores_By_Month(section: str = Header(...), month: str = Header(...)):
    return await get_scores_by_month(section, month)