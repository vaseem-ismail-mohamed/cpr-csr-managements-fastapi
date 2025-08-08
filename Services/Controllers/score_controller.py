from fastapi import HTTPException
from Models.score_schema import input, output
from Services.score_service import UpdateStudentData, FindScores, Current_Month


async def add_scores(data: input.AddScores) -> output.AddScores:
    success = await UpdateStudentData(data.email, data.scores, data.section, data.month)
    if not success:
        raise HTTPException(status_code=404, detail="Update not Found Error")

    month = await Current_Month()
    return output.AddScores(message=f"Scores added for {data.email} in section {data.section} for the month of {month}")


async def get_section_scores(data: input.GetSectionScores) -> output.GetSectionScores:
    if data.section not in ["A", "B", "C"]:
        raise HTTPException(status_code=400, detail="Invalid section. Valid sections are A, B, and C.")

    data_dict = {"month": data.month} if data.month else {}
    scores = await FindScores(data_dict, data.section)
    if not scores:
        return {"message": "No scores found for the specified criteria"}
    return output.GetSectionScores(scores = scores)


async def get_student_scores(email: str, section: str, month: str) -> output.GetStudentScores:
    print(email, section, month)
    if not email or not section or not month:
        raise HTTPException(status_code=400, detail="Email, section, and month are required")

    data_dict = {"email": email, "month": month}
    student_scores = await FindScores(data_dict, section)
    if not student_scores:
        raise HTTPException(status_code=404, detail="Scores not available")

    return output.GetStudentScores(scores = student_scores[0]["scores"]) 


async def get_scores_by_month(section: str, month: str) -> output.GetScoresByMonth:
    if not section or not month:
        raise HTTPException(status_code=400, detail="Section and month are required")

    scores = await FindScores({"month": month}, section)
    if not scores:
        raise HTTPException(status_code=404, detail=f"No scores found for section {section} in {month}")

    return output.GetScoresByMonth(scores = scores)
