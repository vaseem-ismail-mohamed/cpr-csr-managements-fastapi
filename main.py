from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Routes.auth_router import router as auth_router
from Routes.calender_router import router as calender_router
from Routes.cpr_admin_router import router as cpr_admin_router
from Routes.feedback_router import router as feedback_router
from Routes.lead_status_router import router as lead_status_router
from Routes.meet_admin_router import router as meet_admin_router
from Routes.meet_student_router import router as meet_student_router
from Routes.personal_router import router as personal_router
from Routes.score_router import router as score_router
from Routes.slot_lead_student_router import router as slot_lead_student_router
from Routes.track_goals_admin_router import router as track_goals_admin_router
from Routes.track_goals_student_router import router as track_goals_student_router
from Routes.ai_router import router as ai_router
from Routes.lead_overall_router import router as lead_overall_router
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(calender_router)
app.include_router(cpr_admin_router)
app.include_router(feedback_router)
app.include_router(lead_status_router)
app.include_router(meet_admin_router)
app.include_router(meet_student_router)
app.include_router(personal_router)
app.include_router(score_router)
app.include_router(slot_lead_student_router)
app.include_router(track_goals_admin_router)
app.include_router(track_goals_student_router)
app.include_router(ai_router)
app.include_router(lead_overall_router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # important for Render to pick correct port
    uvicorn.run("main:app", host="0.0.0.0", port=port)