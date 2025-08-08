from fastapi import HTTPException
from Services.lead_overall_service import get_users_stats, get_slots_by_month, get_scores_by_month, get_feedback_by_month, get_booking_stats_by_month
from Models.lead_overall_schema import input, output


async def get_lead_overall_statistics(data: input.GetLeadOverallStatistics) -> output.GetLeadOverallStatistics:
    month = data.month

    users_statistics = await get_users_stats()
    calender_bookings = await get_booking_stats_by_month(month)
    feedbacks = await get_feedback_by_month(month)
    meet_slots = await get_slots_by_month(month)
    scores = await get_scores_by_month(month)

    if (
        users_statistics is None or
        calender_bookings is None or
        feedbacks is None or
        meet_slots is None or
        scores is None
    ):
        raise HTTPException(status_code=404, detail="Details not Found")

    return output.GetLeadOverallStatistics(
        users_statistics=users_statistics,
        calender_bookings=calender_bookings["bookings_by_section"],
        feedbacks=feedbacks["feedbacks"],
        meet_slots=meet_slots["slots"],
        scores=scores["scores"]
    )
